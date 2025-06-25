import importlib
import inspect
import logging
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Set, Tuple, Type

from mypy_protobuf.main import PYTHON_RESERVED, Descriptors, SourceCodeLocation
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from typing_extensions import TypedDict

from protobuf_to_pydantic import _pydantic_adapter
from protobuf_to_pydantic.constant import (
    protobuf_common_type_dict,
    protobuf_desc_python_type_dict,
    python_type_default_value_dict,
)
from protobuf_to_pydantic.exceptions import WaitingToCompleteException
from protobuf_to_pydantic.field_info_rule.field_info_param import (
    FieldInfoParamModel,
    field_info_param_dict_handle,
    field_info_param_dict_migration_v2_handler,
)
from protobuf_to_pydantic.field_info_rule.protobuf_option_to_field_info.comment import (
    gen_field_rule_info_dict_from_field_comment_dict,
)
from protobuf_to_pydantic.field_info_rule.protobuf_option_to_field_info.desc import (
    gen_field_info_dict_from_field_desc,
)
from protobuf_to_pydantic.field_info_rule.types import (
    FieldInfoTypedDict,
    OneOfTypedDict,
)
from protobuf_to_pydantic.gen_code import BaseP2C, FormatContainer
from protobuf_to_pydantic.grpc_types import (
    AnyMessage,
    DescriptorProto,
    EnumDescriptorProto,
    FieldDescriptorProto,
    FileDescriptorProto,
)
from protobuf_to_pydantic.plugin.my_types import ProtobufTypeModel
from protobuf_to_pydantic.util import (
    camel_to_snake,
    pydantic_allow_validation_field_handler,
)

if TYPE_CHECKING:
    from protobuf_to_pydantic.plugin.config import ConfigModel
pydantic_con_dict = {}

logger: logging.Logger = logging.getLogger(__name__)


class OptionTypedDict(TypedDict):
    is_proto3_optional: bool


def remove_comment_last_n(content: str) -> str:
    return_content = ""
    if content.endswith("\n"):
        return_content = content[:-1]
    if content.endswith("\n#"):
        return_content = content[:-2]
    if return_content.strip() in ("#", "# "):
        return ""
    return return_content


class FileDescriptorProtoToCode(BaseP2C):
    def __init__(
        self, fd: FileDescriptorProto, descriptors: Descriptors, config: "ConfigModel"
    ):
        # Prevent mutable variables from being shared with other configs
        config = config.copy(deep=True)
        super().__init__(
            customer_import_set=config.customer_import_set,
            customer_deque=config.customer_deque,
            module_path=config.module_path,
            code_indent=config.code_indent,
            pyproject_file_path=config.pyproject_file_path,
        )
        self.config = config
        self._fd = fd
        self._descriptors = descriptors
        self._desc_template = config.template_instance
        self._fd_root_desc_dict = {m.name: m for m in self._fd.message_type}
        self.source_code_info_by_scl = {
            tuple(location.path): location for location in fd.source_code_info.location
        }

        if config.base_model_class is BaseModel:
            self._import_set.add("from pydantic import BaseModel")
        else:
            self._add_import_code(
                config.base_model_class.__module__, config.base_model_class.__name__
            )
        self._model_cache: Dict[str, str] = {}
        self._parse_field_descriptor()

    def _add_other_module_pkg(
        self, other_fd: FileDescriptorProto, type_str: str
    ) -> None:
        """
        Generate the corresponding import statement
        e.g:
          fd name:example_proto/demo/demo.proto
          other_fd name: example_proto/common/single.proto
          output: from ..common.single_p2p import DemoMessage
        """
        if other_fd.name == self._fd.name:
            return

        fd_path_list: Tuple[str, ...] = Path(self._fd.name).parts
        message_path_list: Tuple[str, ...] = Path(other_fd.name).parts
        index: int = -1
        for _index in range(min(len(fd_path_list), len(message_path_list))):
            if message_path_list[_index] == fd_path_list[_index]:
                index = _index
        # common/a/name.proto includes common/b/include.proto
        # The basic name: include_p2p
        module_name: str = (
            message_path_list[-1].replace(".proto", "") + self.config.file_name_suffix
        )
        # Add non-shared parts: b.include_p2p
        module_name = ".".join(message_path_list[index + 1 : -1] + (module_name,))

        logger.info((self._fd.name, other_fd.name, index))
        # Add relative parts: ..b.include_p2p
        # Always use relative parts
        module_name = "." * (len(fd_path_list) - (index + 1)) + module_name
        self._add_import_code(module_name, type_str)

    # def _comment_handler(self, leading_comments: str, trailing_comments: str) -> Tuple[dict, str, str]:
    #     comment_info_dict: dict = {}
    #     if self.config.parse_comment:
    #         leading_comments_list: List[str] = []
    #         trailing_comments_list: List[str] = []
    #         for container, comments in (
    #             (leading_comments_list, leading_comments),
    #             (trailing_comments_list, trailing_comments),
    #         ):
    #             for line in comments.split("\n"):
    #                 field_dict = get_dict_from_comment(self.config.comment_prefix, line)
    #                 if not field_dict:
    #                     container.append(line)
    #                 else:
    #                     comment_info_dict.update(field_dict)
    #         leading_comments = "\n".join(leading_comments_list)
    #         trailing_comments = "\n".join(trailing_comments_list)
    #     return comment_info_dict, leading_comments, trailing_comments

    def add_class_desc(
        self, scl_prefix: SourceCodeLocation, indent: int = 0
    ) -> Tuple[dict, str, str]:
        desc_content = ""
        comment_content = ""
        comment_info_dict: dict = {}
        if tuple(scl_prefix) not in self.source_code_info_by_scl:
            return comment_info_dict, desc_content, comment_content

        scl = self.source_code_info_by_scl[tuple(scl_prefix)]
        if scl:
            if self.config.comment_handler:
                comment_info_dict, leading_comments, trailing_comments = (
                    self.config.comment_handler(
                        scl.leading_comments,
                        scl.trailing_comments,
                        self.config,
                    )
                )
            else:
                leading_comments = scl.leading_comments
                trailing_comments = scl.trailing_comments
            if leading_comments:
                desc_content += " " * (indent + self.code_indent) + '"""\n'
                desc_content += " " * (indent + self.code_indent) + leading_comments
                desc_content += " " * (indent + self.code_indent) + '"""\n'
            if trailing_comments:
                comment_content = "# " + remove_comment_last_n(trailing_comments)

        return comment_info_dict, desc_content, comment_content

    def _enum(
        self,
        enums: Iterable[EnumDescriptorProto],
        scl_prefix: SourceCodeLocation,
        indent: int = 0,
    ) -> List[str]:
        """
        e.g:
            enums:
                {
                    "name": "State",
                    [
                        "value": {
                            name: "INACTIVE"
                            number: 0
                        }
                    ]
                }
            python code:
                from enum import IntEnum
                from protobuf_to_pydantic.flexible_enum_mixin import FlexibleEnumMixin

                class State(IntEnum, FlexibleEnumMixin):
                    INACTIVE = 0
        """
        if not enums:
            return []
        self._add_import_code("enum", "IntEnum")
        self._add_import_code(
            "protobuf_to_pydantic.flexible_enum_mixin", "FlexibleEnumMixin"
        )

        content_list = []
        for i, enum in enumerate(enums):
            class_name = (
                enum.name if enum.name not in PYTHON_RESERVED else "_r_" + enum.name
            )

            content = " " * indent + f"class {class_name}(IntEnum, FlexibleEnumMixin):"

            _, desc_content, comment_content = self.add_class_desc(
                scl_prefix + [i], indent
            )
            if comment_content:
                content += comment_content
            content += "\n" + desc_content
            for enum_item in enum.value:
                content += (
                    " " * (self.code_indent + indent)
                    + f"{enum_item.name} = {enum_item.number}\n"
                )
            content_list.append(content)
        return content_list

    def _message_nested_type_handle(
        self,
        desc: DescriptorProto,
        scl_prefix: SourceCodeLocation,
        indent: int,
        nested_message_config_dict: dict,
        this_level_model_cache: Dict[str, str],
        skip_validate_rule: bool,
    ) -> List[str]:
        """Parse the nested information of Message"""
        content_list: List[str] = []
        for index, nested_message in enumerate(desc.nested_type):
            if nested_message.options.map_entry:
                # Some data of Map Entry in nested type array
                continue
            skip_validate_rule = skip_validate_rule or nested_message_config_dict.get(
                nested_message.name, {}
            ).get("skip", False)
            content_list.append(
                self._message(
                    desc=nested_message,
                    root_desc=desc,
                    scl_prefix=scl_prefix + [index],
                    sub_model_cache=this_level_model_cache,
                    indent=indent + self.code_indent,
                    skip_validate_rule=skip_validate_rule,
                )
            )
        return content_list

    # flake8: noqa: C901
    def _message_field_handle(
        self,
        *,
        desc: DescriptorProto,
        root_desc: DescriptorProto,
        field: FieldDescriptorProto,
        indent: int,
        nested_message_config_dict: dict,
        optional_dict: dict,
        one_of_dict: Dict[str, OneOfTypedDict],
        scl_prefix: SourceCodeLocation,
        this_level_model_cache: Dict[str, str],
        pydantic_config_dict: dict,
        skip_validate_rule: bool = False,
    ) -> Optional[Tuple[str, str]]:
        """generate message's field to Pydantic.FieldInfo code

        :param desc: The message to which the field belongs is used to determine whether it is self-referencing
        :param root_desc: field's message or parent message
        :param field:
        :param indent: Indentation configuration of the generated code
        :param nested_message_config_dict:
            message config dict
            e.g: {"{message name}": {"skip": True}}
        :param optional_dict:
            field optional dict
            e.g: {"{field name}": {"is_proto3_optional": True}}
        :param one_of_dict: one of config dict
        :param scl_prefix: source code location
        :param this_level_model_cache:
            The cache of the model generated at this level,
            used to prevent the same model from being generated multiple times
        :param pydantic_config_dict: pydantic config dict: https://docs.pydantic.dev/dev/api/config/
        :param skip_validate_rule: If the value is True, the validation information for the field will not be generated

        :return: validator_handle_content, class_field_content
        """
        field_info_default_value = _pydantic_adapter.PydanticUndefined
        field_info_default_factory_value: Any = None
        field_type = None
        nested_message_name: Optional[str] = None
        use_custom_type = False
        raw_validator_dict = {}
        leading_comments = ""
        trailing_comments = ""

        if tuple(scl_prefix) in self.source_code_info_by_scl:
            scl = self.source_code_info_by_scl[tuple(scl_prefix)]
            if scl and scl.leading_comments:
                leading_comments = "#" + scl.leading_comments.replace("\n", "\n#")
            if scl and scl.trailing_comments:
                trailing_comments = "#" + scl.trailing_comments

        if field.type == 11:
            # message handle
            message = self._descriptors.messages[field.type_name]

            if message.options.map_entry:
                key_msg, value_msg = message.field
                self._add_import_code("typing")
                type_str: str = (
                    f"typing.Dict[{self._get_protobuf_type_model(key_msg).py_type_str},"
                    f" {self._get_protobuf_type_model(value_msg).py_type_str}]"
                )
                # TODO This is not the best solution,
                #  and it should be processed with the same logic as 294, and then optimized
                type_str = '"' + type_str + '"'
                field_info_default_factory_value = dict
                rule_type_str = "map"
            elif field.type_name.startswith(".google.protobuf"):
                protobuf_type_model = self._get_protobuf_type_model(field)
                type_str = protobuf_type_model.py_type_str
                rule_type_str = protobuf_type_model.rule_type_str
                field_info_default_factory_value = protobuf_type_model.type_factory
                use_custom_type = protobuf_type_model.use_custom_type
            else:
                protobuf_type_model = self._get_protobuf_type_model(field)
                type_str = protobuf_type_model.py_type_str
                rule_type_str = protobuf_type_model.rule_type_str
                nested_message_name = type_str
                use_custom_type = protobuf_type_model.use_custom_type
                field_info_default_factory_value = FormatContainer(
                    protobuf_type_model.type_factory
                )

                message_fd: FileDescriptorProto = self._descriptors.message_to_fd[
                    field.type_name
                ]
                self._add_other_module_pkg(message_fd, type_str)
                root_desc_nested_type_name = {i.name for i in root_desc.nested_type}
                desc_nested_type_name = {i.name for i in desc.nested_type}
                if message == desc:
                    # if self-referencing, need use Python type hints postponed annotations
                    field_info_default_factory_value = FormatContainer(
                        f"lambda : {type_str}()"
                    )
                    type_str = f'"{type_str}"'
                elif (
                    message_fd.name == self._fd.name
                    and message.name not in root_desc_nested_type_name
                    and message.name not in desc_nested_type_name
                ):
                    # If the referenced Message is generated later, it needs to be generated in advance
                    scl_prefix = [FileDescriptorProto.MESSAGE_TYPE_FIELD_NUMBER]
                    for index, desc in enumerate(self._fd.message_type):
                        if desc is message:
                            scl_prefix = [
                                FileDescriptorProto.MESSAGE_TYPE_FIELD_NUMBER,
                                index,
                            ]
                    try:
                        self._content_deque.append(
                            self._message(
                                desc=message,
                                root_desc=root_desc,
                                scl_prefix=scl_prefix,
                                sub_model_cache=this_level_model_cache,
                            )
                        )
                    except WaitingToCompleteException:
                        field_info_default_factory_value = FormatContainer(
                            f"lambda : {type_str}()"
                        )
                        type_str = f'"{type_str}"'
                elif type_str in root_desc_nested_type_name:
                    field_info_default_factory_value = FormatContainer(
                        f"lambda : {root_desc.name}.{type_str}()"
                    )
                    # I don't want to maintain complex dependencies, so I'll just use strings type hints here
                    type_str = f'"{root_desc.name}.{type_str}"'
        elif field.type == 14:
            # enum handle
            type_str = field.type_name.split(".")[-1]
            field_info_default_value = 0
            rule_type_str = "enum"
            root_desc_enum_name = {i.name for i in root_desc.enum_type}
            if type_str in root_desc_enum_name:
                # I don't want to maintain complex dependencies, so I'll just use strings type hints here
                type_str = f'"{root_desc.name}.{type_str}"'
            message_fd = self._descriptors.message_to_fd[field.type_name]
            self._add_other_module_pkg(message_fd, type_str)
            pydantic_config_dict["validate_default"] = True
        elif field.type not in protobuf_desc_python_type_dict:
            logger.error(f"Not found {field.type} in type_dict")
            return None
        else:
            field_info_default_value = python_type_default_value_dict[
                protobuf_desc_python_type_dict[field.type]
            ]
            protobuf_type_model = self._get_protobuf_type_model(field)
            use_custom_type = protobuf_type_model.use_custom_type
            type_str = protobuf_type_model.py_type_str
            rule_type_str = protobuf_type_model.rule_type_str

        if field.label == field.LABEL_REPEATED and not field.type_name.endswith(
            "Entry"
        ):
            # repeated support
            self._add_import_code("typing")
            type_str = f"typing.List[{type_str}]"
            field_info_default_value = None
            field_info_default_factory_value = list
            rule_type_str = "repeated"

        field_info_dict: FieldInfoTypedDict = {}  # type: ignore[typeddict-item]
        if self.config.comment_handler:
            comment_field_info_dict, leading_comments, trailing_comments = (
                self.config.comment_handler(
                    leading_comments,
                    trailing_comments,
                    self.config,
                )
            )
        else:
            comment_field_info_dict = {}

        if not skip_validate_rule:
            field_info_dict.update(comment_field_info_dict)  # type: ignore[typeddict-item]
            if len(field.options.ListFields()) != 0 and rule_type_str:
                # protobuf option support
                field_info_dict.update(
                    gen_field_info_dict_from_field_desc(
                        rule_type_str, field.name, field
                    )
                )
                field_info_dict = self._desc_template.handle_template_var(
                    field_info_dict
                )
            elif field_info_dict:
                field_info_dict = self._desc_template.handle_template_var(
                    field_info_dict
                )
                field_info_dict = gen_field_rule_info_dict_from_field_comment_dict(
                    field_info_dict,
                    field,
                    rule_type_str,
                    field.name,  # type: ignore[arg-type]
                )

        if field_info_dict:
            raw_validator_dict = field_info_dict.get("validator", {})

            field_info_dict = FieldInfoParamModel(**field_info_dict).to_dict()  # type: ignore

            skip = field_info_dict.pop("skip", False)
            if nested_message_name:
                if nested_message_name not in nested_message_config_dict:
                    nested_message_config_dict[nested_message_name] = {}
                nested_message_config_dict[nested_message_name]["skip"] = skip

            if not field_info_dict.pop("enable", False):
                return None
            try:
                if type_str.startswith("typing"):
                    import typing  # isort:skip
                field_type = eval(type_str)
            except NameError:
                pass

        is_required = field_info_dict.get("required", None)

        # if rule_type_str == "enum":
        #     enum_default_value = field_info_dict.get("default", MISSING)
        #     if enum_default_value.__class__ == MISSING.__class__:
        #         enum_default_value = field_info_default_value
        #
        #     const_value = field_info_dict.get("const", MISSING)
        #     enable_const = const_value.__class__ != MISSING.__class__
        #     if isinstance(enum_default_value, int):
        #         if "." in type_str:
        #             field_info_default_factory_value = FormatContainer(
        #                 "lambda : " + type_str.strip('"') + "(" + str(enum_default_value) + ")"
        #             )
        #             if enable_const:
        #                 field_info_dict["const"] = field_info_default_factory_value
        #         else:
        #             field_info_default_value = FormatContainer(type_str + "(" + str(enum_default_value) + ")")
        #             if enable_const:
        #                 field_info_dict["const"] = field_info_default_value

        if (
            field_info_dict
            or field_info_default_value is not _pydantic_adapter.PydanticUndefined
            or field_info_default_factory_value is not None
            or field_type is not None
        ):
            field_info_param_dict_handle(
                field_info_dict,  # type: ignore[arg-type]
                field_info_default_value,
                field_info_default_factory_value,
                field_type=field_type,
            )

        validator_handle_content = ""
        field_info_dict.pop("validator", None)
        if raw_validator_dict:
            # use raw validator
            # In Pydantic v2:
            #     field_doc_dict["validatos"] = {
            #       'not_in_test_any_not_in_validator': PydanticDescriptorProxy(
            #             wrapped=<classmethod object at 0x7f28943c8128>,
            #             decorator_info=FieldValidatorDecoratorInfo(fields=('not_in_test',),
            #             mode='after', check_fields=None),
            #             shim=None
            #        )
            #     }
            #  But validator_dict output:
            #   {
            #       'not_in_test_any_not_in_validator': {
            #           'wrapped': <classmethod object at 0x7f28943c8128>,
            #           'decorator_info': {
            #               'fields': ('not_in_test',),
            #               'mode': 'after',
            #               'check_fields': None
            #            },
            #           'shim': None
            #       }
            #   }
            validator_handle_content += self._validator_handle(
                raw_validator_dict, self.code_indent + indent
            )

        # type support
        type_: Any = field_info_dict.pop("type_", None)
        map_type_dict: dict = field_info_dict.pop("map_type", {})
        if type_:
            # Custom types have the highest priority
            if inspect.isclass(type_) and type_.__mro__[1] in pydantic_con_dict:
                type_str = self._get_pydantic_con_type_code(type_)
            else:
                type_str = self._get_value_code(type_)
        elif map_type_dict:
            # For `map type`, the string of type needs to be regenerated
            message = self._descriptors.messages[field.type_name]
            if "keys" in map_type_dict:
                key_type_str = self._get_value_code(map_type_dict["keys"])
            else:
                key_type_str = self._get_protobuf_type_model(
                    message.field[0]
                ).py_type_str
            if "values" in map_type_dict:
                value_type_str = self._get_value_code(map_type_dict["values"])
            else:
                value_type_str = self._get_protobuf_type_model(
                    message.field[1]
                ).py_type_str
            self._add_import_code("typing")
            type_str = f"typing.Dict[{key_type_str}, {value_type_str}]"

        # custom field support
        field_class: Optional[Type[FieldInfo]] = field_info_dict.pop("field", None)
        if field_class:
            field_name: str = self._get_value_code(field_class)
        else:
            field_name = "Field"
            self._add_import_code("pydantic", "Field")

        # pgv or p2p rule no warning required
        field_info_param_dict_migration_v2_handler(field_info_dict, is_warnings=False)  # type: ignore[arg-type]

        # optional handler
        if (
            optional_dict.get(field.name, {}).get("is_proto3_optional", False)
            or self.config.all_field_set_optional
        ):
            self._add_import_code("typing")
            type_str = f"typing.Optional[{type_str}]"
            if (
                is_required is not True
                and field_info_dict.get("default", _pydantic_adapter.PydanticUndefined)
                is _pydantic_adapter.PydanticUndefined
                and not field_info_dict.get("default_factory", None)
            ):
                field_info_dict["default"] = None

        # arranging  field info parameters
        for key in FieldInfo.__slots__:
            value: Any = field_info_dict.get(key, None)
            if value is getattr(FieldInfo(), key):
                field_info_dict.pop(key, None)  # type: ignore[misc]

        if isinstance(field_info_dict.get("json_schema_extra", None), dict):
            # After Pydantic version 2.1, json_schema_extra type may be callable
            for k in list(field_info_dict["json_schema_extra"].keys()):
                if k not in field_info_dict:
                    field_info_dict[k] = field_info_dict["json_schema_extra"].pop(k)  # type: ignore[literal-required]
            if not field_info_dict.get("json_schema_extra", None):
                field_info_dict.pop("json_schema_extra")

        if one_of_dict:
            alias = field_info_dict.get("alias", None)
            model_config_dict = self.config.base_model_class.model_config

            for one_of_name, sub_one_of_dict in one_of_dict.items():
                # Only process fields that are actually part of this oneof
                if field.name in sub_one_of_dict["fields"]:
                    pydantic_allow_validation_field_handler(
                        field.name, alias, sub_one_of_dict["fields"], model_config_dict
                    )

        field_info_str: str = (
            ", ".join(
                [
                    f"{k}={self._get_value_code(v)}"
                    for k, v in field_info_dict.items()
                    if v is not None or k == "default"
                ]
            )
            or ""
        )
        class_field_content: str = (
            " " * (self.code_indent + indent)
            + f"{field.name}: {type_str} = {field_name}({field_info_str})"
        )
        leading_comments = remove_comment_last_n(leading_comments)
        trailing_comments = remove_comment_last_n(trailing_comments)
        if self.config.parse_comment and leading_comments:
            class_field_content = leading_comments + "\n" + class_field_content
        if self.config.parse_comment and trailing_comments:
            class_field_content = class_field_content + trailing_comments
        class_field_content = class_field_content + "\n"

        if use_custom_type:
            pydantic_config_dict["arbitrary_types_allowed"] = use_custom_type
        return validator_handle_content, class_field_content

    def _gen_one_of_dict(
        self,
        desc: DescriptorProto,
        scl_prefix: SourceCodeLocation,
        skip_validate_rule: bool,
    ) -> Tuple[Dict[str, OneOfTypedDict], Dict[str, OptionTypedDict]]:
        """
        protobuf content:
            message OneOfOptionalTest {
              string header = 1;
              oneof id {
                option (p2p_validate.required) = true;
                option (p2p_validate.oneof_extend) = {optional: ["x", "y"]};
                string x = 2;
                int32  y = 3;
              }
              optional string name = 4;
              optional int32 age= 5;
              repeated string str_list =6;
              map<string, int32> int_map = 7;
            }
        desc.field:
            [
                (name: "header" number: 1 label: LABEL_OPTIONAL type: TYPE_STRING json_name: "header" ),
                (name: "x" number: 2 label: LABEL_OPTIONAL type: TYPE_STRING oneof_index: 0 json_name: "x" ),
                (name: "y" number: 3 label: LABEL_OPTIONAL type: TYPE_INT32 oneof_index: 0 json_name: "y" ),
                (
                    name: "name" number: 4 label: LABEL_OPTIONAL type: TYPE_STRING oneof_index: 1 json_name: "name"
                    proto3_optional: true
                ),
                (
                    name: "age" number: 5 label: LABEL_OPTIONAL type: TYPE_INT32 oneof_index: 2 json_name: "age"
                    proto3_optional: true
                ),
                (name: "str_list" number: 6 label: LABEL_REPEATED type: TYPE_STRING json_name: "strList" ),
                (
                    name: "int_map" number: 7 label: LABEL_REPEATED type: TYPE_MESSAGE
                    type_name: ".p2p_validate_test.OneOfOptionalTest.IntMapEntry" json_name: "intMap"
                )
            ]

        desc.oneof_decl:
            [
                name: "id"
                options {
                    [p2p_validate.required]: true
                    [p2p_validate.oneof_extend] {
                        optional: "x"
                        optional: "y"
                    }
                },
                name: "_name",
                name: "_age"
            ]
        return:
            - one_of_dict:
                {'OneOfOptionalTest.id': {'required': True, 'optional': ['x', 'y'], 'fields': {'y', 'x'}}}
            - optional_dict:
                {'name': {'is_proto3_optional': True}, 'age': {'is_proto3_optional': True}}

        """
        one_of_dict: Dict[str, OneOfTypedDict] = {}
        optional_dict: Dict[str, OptionTypedDict] = {}
        index_field_name_dict: Dict[int, Set[str]] = {}

        for field in desc.field:
            if field.proto3_optional:
                optional_dict[field.name] = {"is_proto3_optional": True}
            if field.HasField("oneof_index"):
                if field.oneof_index not in index_field_name_dict:
                    index_field_name_dict[field.oneof_index] = set()
                index_field_name_dict[field.oneof_index].add(field.name)

        if skip_validate_rule:
            return one_of_dict, optional_dict

        for index, one_of_item in enumerate(desc.oneof_decl):
            # if field is proto3_optional, ignore
            if (
                one_of_item.name.startswith("_")
                and one_of_item.name[1:] in optional_dict
            ):
                continue

            option_dict: OneOfTypedDict = {}  # type: ignore[typeddict-item]
            for option_descriptor, option_value in one_of_item.options.ListFields():
                full_name_list = option_descriptor.full_name.split(".")
                pkg, rule_name = full_name_list[-2], full_name_list[-1]
                if not pkg.endswith("validate"):
                    continue
                if rule_name in ("required",):
                    # Now only support `required`
                    option_dict["required"] = option_value
                elif rule_name in ("oneof_extend",):
                    # Now only support `oneof_extend`
                    for (
                        one_of_extend_field_descriptor,
                        result,
                    ) in option_value.ListFields():
                        if one_of_extend_field_descriptor.name == "optional":
                            for one_of_optional_name in result:
                                optional_dict[one_of_optional_name] = {
                                    "is_proto3_optional": True
                                }

            scl = self.source_code_info_by_scl.get(tuple(scl_prefix + [index]))
            if scl and self.config.comment_handler:
                comment_info_dict, leading_comments, trailing_comments = (
                    self.config.comment_handler(
                        scl.leading_comments,
                        scl.trailing_comments,
                        self.config,
                    )
                )
            else:
                comment_info_dict = {}

            for (
                one_of_comment_rule_name,
                one_of_comment_option_value,
            ) in comment_info_dict.items():
                if one_of_comment_rule_name in ("required",):
                    # Now only support `required`
                    option_dict["required"] = one_of_comment_option_value
                elif one_of_comment_rule_name in ("oneof_extend",):
                    for (
                        one_of_extend_key,
                        one_of_extend_value,
                    ) in one_of_comment_option_value.items():
                        if one_of_extend_key == "optional":
                            for one_of_optional_name in one_of_extend_value:
                                optional_dict[one_of_optional_name] = {
                                    "is_proto3_optional": True
                                }
            # if self.config.parse_comment and comment:
            #     for line in comment.leading_comments.split("\n"):
            #         one_of_comment_dict = get_dict_from_comment(self.config.comment_prefix, line)
            #         if not one_of_comment_dict:
            #             continue
            #         for one_of_comment_rule_name, one_of_comment_option_value in one_of_comment_dict.items():
            #             if one_of_comment_rule_name in ("required",):
            #                 # Now only support `required`
            #                 option_dict["required"] = one_of_comment_option_value
            #             elif one_of_comment_rule_name in ("oneof_extend",):
            #                 for one_of_extend_key, one_of_extend_value in one_of_comment_option_value.items():
            #                     if one_of_extend_key == "optional":
            #                         for one_of_optional_name in one_of_extend_value:
            #                             optional_dict[one_of_optional_name] = {"is_proto3_optional": True}

            option_dict["fields"] = index_field_name_dict.get(index, set())
            if option_dict:
                # Only when the rules are used, will the number of fields of one_of be checked to see if they match
                one_of_dict[desc.name + "." + one_of_item.name] = option_dict
        return one_of_dict, optional_dict

    def _generate_discriminated_union_classes(
        self,
        desc: DescriptorProto,
        one_of_dict: Dict[str, OneOfTypedDict],
        optional_dict: Dict[str, OptionTypedDict],
        indent: int,
        field_map: Dict[str, FieldDescriptorProto],
    ) -> Tuple[str, str, Dict[str, Set[str]]]:
        """Generate discriminated union variant classes for oneofs.

        Returns:
            - union_classes_content: The generated variant classes code
            - union_types_content: The union type definitions
            - fields_to_exclude: Map of field names to exclude from main class
        """
        union_classes_content = ""
        union_types_content = ""
        fields_to_exclude: Dict[str, Set[str]] = {}

        # Process each oneof
        for oneof_full_name, oneof_config in one_of_dict.items():
            oneof_name = oneof_full_name.split(".")[-1]  # Get just the oneof name
            discriminator_name = f"{oneof_name}_case"
            fields_to_exclude[oneof_name] = oneof_config["fields"]

            # Identify common fields (fields not in any oneof)
            all_oneof_fields = set()
            for config in one_of_dict.values():
                all_oneof_fields.update(config["fields"])

            # Also exclude the oneof field names themselves (like "id" for the "id" oneof)
            oneof_field_names = {name.split(".")[-1] for name in one_of_dict.keys()}
            all_oneof_fields.update(oneof_field_names)

            # Generate variant classes
            variant_types = []
            for field_name in oneof_config["fields"]:
                if field_name not in field_map:
                    continue

                field = field_map[field_name]
                variant_class_name = (
                    f"{desc.name}{oneof_name.title()}{field_name.title()}"
                )
                variant_content = f"\n{' ' * indent}class {variant_class_name}({self.config.base_model_class.__name__}):\n"
                variant_content += f'{" " * (indent + self.code_indent)}"""Variant when \'{field_name}\' is set in {oneof_name} oneof."""\n'
                variant_content += f'{" " * (indent + self.code_indent)}{discriminator_name}: Literal["{field_name}"] = Field(default="{field_name}", exclude=True)\n'

                # Add the oneof field
                field_type = self._get_field_type_str(field)
                variant_content += (
                    f"{' ' * (indent + self.code_indent)}{field_name}: {field_type}\n"
                )

                union_classes_content += variant_content
                variant_types.append(variant_class_name)

            # Generate None variant if oneof is not required
            if not oneof_config.get("required", False):
                none_variant_name = f"{desc.name}{oneof_name.title()}None"
                none_content = f"\n{' ' * indent}class {none_variant_name}({self.config.base_model_class.__name__}):\n"
                none_content += f'{" " * (indent + self.code_indent)}"""Variant when no field is set in {oneof_name} oneof."""\n'
                none_content += f"{' ' * (indent + self.code_indent)}{discriminator_name}: Literal[None] = None\n"

                union_classes_content += none_content
                variant_types.append(none_variant_name)

            # Generate union type
            union_type_name = f"{desc.name}{oneof_name.title()}Union"
            union_content = f"\n{' ' * indent}{union_type_name} = Annotated[\n"
            union_content += f"{' ' * (indent + self.code_indent)}Union[{', '.join(variant_types)}],\n"
            union_content += f"{' ' * (indent + self.code_indent)}Field(discriminator='{discriminator_name}')\n"
            union_content += f"{' ' * indent}]\n"

            union_types_content += union_content

            # Add required imports
            self._add_import_code("typing", "Literal")
            self._add_import_code("typing", "Union")
            self._add_import_code("typing", "Annotated")
            self._add_import_code("pydantic", "Field")
            self._add_import_code("pydantic", "BaseModel")

        return union_classes_content, union_types_content, fields_to_exclude

    def _get_field_type_str(self, field: FieldDescriptorProto) -> str:
        """Get the Python type string for a field (simplified version)."""
        # This is a simplified implementation - the real one would be more complex
        type_map = {
            FieldDescriptorProto.TYPE_STRING: "str",
            FieldDescriptorProto.TYPE_INT32: "int",
            FieldDescriptorProto.TYPE_INT64: "int",
            FieldDescriptorProto.TYPE_UINT32: "int",
            FieldDescriptorProto.TYPE_UINT64: "int",
            FieldDescriptorProto.TYPE_SINT32: "int",
            FieldDescriptorProto.TYPE_SINT64: "int",
            FieldDescriptorProto.TYPE_FIXED32: "int",
            FieldDescriptorProto.TYPE_FIXED64: "int",
            FieldDescriptorProto.TYPE_SFIXED32: "int",
            FieldDescriptorProto.TYPE_SFIXED64: "int",
            FieldDescriptorProto.TYPE_BOOL: "bool",
            FieldDescriptorProto.TYPE_FLOAT: "float",
            FieldDescriptorProto.TYPE_DOUBLE: "float",
            FieldDescriptorProto.TYPE_BYTES: "bytes",
        }
        result = type_map.get(field.type, "Any")
        if result == "Any":
            # Add Any import when needed
            self._add_import_code("typing", "Any")
        return result

    def _get_default_value(self, field: FieldDescriptorProto) -> str:
        """Get the default value for a field (simplified version)."""
        default_map = {
            FieldDescriptorProto.TYPE_STRING: '""',
            FieldDescriptorProto.TYPE_INT32: "0",
            FieldDescriptorProto.TYPE_INT64: "0",
            FieldDescriptorProto.TYPE_UINT32: "0",
            FieldDescriptorProto.TYPE_UINT64: "0",
            FieldDescriptorProto.TYPE_SINT32: "0",
            FieldDescriptorProto.TYPE_SINT64: "0",
            FieldDescriptorProto.TYPE_FIXED32: "0",
            FieldDescriptorProto.TYPE_FIXED64: "0",
            FieldDescriptorProto.TYPE_SFIXED32: "0",
            FieldDescriptorProto.TYPE_SFIXED64: "0",
            FieldDescriptorProto.TYPE_BOOL: "False",
            FieldDescriptorProto.TYPE_FLOAT: "0.0",
            FieldDescriptorProto.TYPE_DOUBLE: "0.0",
            FieldDescriptorProto.TYPE_BYTES: 'b""',
        }
        return default_map.get(field.type, "None")

    def _message(
        self,
        *,
        desc: DescriptorProto,
        root_desc: DescriptorProto,
        scl_prefix: SourceCodeLocation,
        sub_model_cache: Dict[str, str],
        indent: int = 0,
        skip_validate_rule: bool = False,
    ) -> str:
        class_name = (
            desc.name if desc.name not in PYTHON_RESERVED else "_r_" + desc.name
        )
        if class_name in self._fd_root_desc_dict:
            use_model_cache = self._model_cache
        else:
            use_model_cache = sub_model_cache

        if class_name in use_model_cache:
            if not use_model_cache[class_name]:
                raise WaitingToCompleteException(
                    f"The model:{class_name} is being generated"
                )
            return use_model_cache[class_name]
        else:
            use_model_cache[class_name] = ""

        this_level_model_cache: Dict[str, str] = {}
        self._add_import_code("google.protobuf.message", "Message")
        comment_info_dict, desc_content, comment_content = self.add_class_desc(
            scl_prefix, indent
        )

        # We'll determine base classes after one_of_dict is defined
        class_name_content = None  # Will be set later
        comment_content_to_add = comment_content  # Store for later
        class_var_str_list = []
        class_sub_c_str_list = []
        class_validate_handler_content = ""
        class_field_content = ""
        class_head_content = desc_content if desc_content else ""

        pydantic_config_dict: dict = {}
        one_of_dict, optional_dict, nested_message_config_dict = {}, {}, {}  # type: dict, dict, dict

        if comment_info_dict.get("ignored", False):
            skip_validate_rule = True
        for option_descriptor, option_value in desc.options.ListFields():
            if option_descriptor.full_name.endswith("validate.ignored"):
                skip_validate_rule = option_value

        if desc.oneof_decl:
            one_of_dict, optional_dict = self._gen_one_of_dict(
                desc,
                scl_prefix + [DescriptorProto.ONEOF_DECL_FIELD_NUMBER],
                skip_validate_rule=skip_validate_rule,
            )

        # Generate discriminated union classes if enabled
        union_classes_content = ""
        union_types_content = ""
        fields_to_exclude: Set[str] = set()

        if self.config.use_discriminated_unions_for_oneofs and desc.oneof_decl:
            # Create field map for easy lookup
            field_map = {field.name: field for field in desc.field}

            # If one_of_dict is empty but we have oneofs, create a basic dict
            if not one_of_dict:
                one_of_dict = {}
                for idx, oneof_desc in enumerate(desc.oneof_decl):
                    oneof_key = f"{desc.name}.{oneof_desc.name}"
                    oneof_fields = set()
                    for field in desc.field:
                        if field.HasField("oneof_index") and field.oneof_index == idx:
                            oneof_fields.add(field.name)

                    # Skip proto3 optional synthetic oneofs - these should not be discriminated unions
                    # Proto3 optional fields create synthetic oneofs with a single field that is marked as proto3_optional
                    if len(oneof_fields) == 1:
                        field_name = next(iter(oneof_fields))
                        if optional_dict.get(field_name, {}).get(
                            "is_proto3_optional", False
                        ):
                            continue  # Skip this oneof - it's a proto3 optional synthetic oneof

                    one_of_dict[oneof_key] = {"required": False, "fields": oneof_fields}

            # Also filter out proto3 optional oneofs from existing one_of_dict
            # This handles cases where one_of_dict was populated from protobuf options/comments
            filtered_one_of_dict = {}
            for oneof_key, oneof_config in one_of_dict.items():
                oneof_fields = oneof_config.get("fields", set())
                # Skip proto3 optional synthetic oneofs
                if len(oneof_fields) == 1:
                    field_name = next(iter(oneof_fields))
                    if optional_dict.get(field_name, {}).get(
                        "is_proto3_optional", False
                    ):
                        continue  # Skip this oneof - it's a proto3 optional synthetic oneof
                filtered_one_of_dict[oneof_key] = oneof_config

            union_classes_content, union_types_content, exclude_map = (
                self._generate_discriminated_union_classes(
                    desc, filtered_one_of_dict, optional_dict, indent, field_map
                )
            )

            # Collect all fields to exclude from main class
            for field_set in exclude_map.values():
                fields_to_exclude.update(field_set)

        # Now we can set the class name content with proper base classes
        base_classes = [self.config.base_model_class.__name__]
        if self.config.use_discriminated_unions_for_oneofs and one_of_dict:
            # Add mixin for centralized oneof handling
            base_classes.insert(0, "TaggedUnionMixin")
            self._add_import_code(
                "protobuf_to_pydantic.tagged_union_mixin",
                "TaggedUnionMixin",
            )

        class_name_content = (
            " " * indent + f"class {class_name}({', '.join(base_classes)}):"
        )
        if comment_content_to_add:
            class_name_content += comment_content_to_add

        for idx, field in enumerate(desc.field):
            if field.name in PYTHON_RESERVED:
                continue

            # Skip oneof fields when using discriminated unions
            if (
                self.config.use_discriminated_unions_for_oneofs
                and field.name in fields_to_exclude
            ):
                continue

            _content_tuple = self._message_field_handle(
                desc=desc,
                root_desc=root_desc,
                field=field,
                indent=indent,
                nested_message_config_dict=nested_message_config_dict,
                optional_dict=optional_dict,
                one_of_dict=one_of_dict,
                scl_prefix=scl_prefix + [DescriptorProto.FIELD_FIELD_NUMBER, idx],
                this_level_model_cache=this_level_model_cache,
                pydantic_config_dict=pydantic_config_dict,
                skip_validate_rule=skip_validate_rule,
            )
            if _content_tuple:
                class_validate_handler_content += _content_tuple[0]
                class_field_content += _content_tuple[1]

        if desc.nested_type:
            class_sub_c_str_list.extend(
                self._message_nested_type_handle(
                    desc,
                    scl_prefix + [DescriptorProto.NESTED_TYPE_FIELD_NUMBER],
                    indent,
                    nested_message_config_dict,
                    this_level_model_cache,
                    skip_validate_rule,
                )
            )
        if desc.enum_type:
            class_sub_c_str_list.extend(
                self._enum(
                    desc.enum_type,
                    scl_prefix + [DescriptorProto.ENUM_TYPE_FIELD_NUMBER],
                    indent + self.code_indent,
                )
            )

        if one_of_dict and not self.config.use_discriminated_unions_for_oneofs:
            # Only add the validator if not using discriminated unions
            class_var_str_list.append(
                f"{' ' * (indent + self.code_indent)}_one_of_dict = {self._get_value_code(one_of_dict)}"
            )

            self._add_import_code(
                "protobuf_to_pydantic.customer_validator.v2", "check_one_of"
            )
            class_var_str_list.append(
                f"{' ' * (indent + self.code_indent)}"
                f'one_of_validator = model_validator(mode="before")(check_one_of)'
            )
            self._add_import_code("pydantic", "model_validator")

        if pydantic_config_dict:
            # Pydantic V2 output:
            #   model_config = ConfigDict(arbitrary_types_allowed=False)
            attr_str = ", ".join([f"{k}={v}" for k, v in pydantic_config_dict.items()])
            class_var_str_list.append(
                f"{' ' * (indent + self.code_indent)}model_config = ConfigDict({attr_str})"
            )
            self._add_import_code("pydantic", "ConfigDict")

        class_head_content += "\n".join(class_sub_c_str_list)
        if class_head_content and class_var_str_list:
            class_head_content += "\n"
        class_head_content += "\n".join(class_var_str_list)

        # Assemble content with union classes if using discriminated unions
        if self.config.use_discriminated_unions_for_oneofs and union_classes_content:
            # Add union classes before the main class
            content = union_classes_content + "\n"
            content += union_types_content + "\n"
            content += "\n".join(
                [
                    i
                    for i in [
                        class_name_content,
                        class_head_content,
                        class_field_content,
                        class_validate_handler_content,
                    ]
                    if i
                ]
            )

            # Add fields for union types in the main class
            if one_of_dict:
                union_fields_content = ""
                for oneof_full_name, oneof_config in one_of_dict.items():
                    oneof_name = oneof_full_name.split(".")[-1]
                    union_type_name = f"{desc.name}{oneof_name.title()}Union"
                    # Make the field optional if the oneof is not required
                    if not oneof_config.get("required", False):
                        # Add Optional import
                        self._add_import_code("typing", "Optional")
                        union_fields_content += f"{' ' * (indent + self.code_indent)}{oneof_name}: Optional[{union_type_name}] = Field(default=None)\n"
                    else:
                        union_fields_content += f"{' ' * (indent + self.code_indent)}{oneof_name}: {union_type_name}\n"

                # Insert union fields into the MAIN class only (not base classes)
                if union_fields_content:
                    # Find where to insert the union fields (in the main class only)
                    content_lines = content.split("\n")
                    insertion_point = -1

                    # Find the main class specifically (not base classes which start with "_")
                    main_class_line = f"class {desc.name}("
                    for i, line in enumerate(content_lines):
                        if line.strip().startswith(main_class_line):
                            # Found the main class, now find where to insert union fields
                            j = i + 1
                            while j < len(content_lines):
                                if content_lines[j].strip().startswith(
                                    '"""'
                                ) or content_lines[j].strip().startswith("'''"):
                                    # Skip docstring
                                    quote = (
                                        '"""'
                                        if content_lines[j].strip().startswith('"""')
                                        else "'''"
                                    )
                                    if (
                                        content_lines[j].strip().endswith(quote)
                                        and len(content_lines[j].strip()) > 3
                                    ):
                                        # Single line docstring
                                        j += 1
                                        break
                                    else:
                                        # Multi-line docstring
                                        j += 1
                                        while j < len(
                                            content_lines
                                        ) and not content_lines[j].strip().endswith(
                                            quote
                                        ):
                                            j += 1
                                        j += 1
                                        break
                                elif content_lines[j].strip() and content_lines[
                                    j
                                ].startswith(" " * (indent + self.code_indent)):
                                    # Found a class member, insert before it
                                    break
                                elif content_lines[j].strip() and not content_lines[
                                    j
                                ].startswith(" " * (indent + self.code_indent)):
                                    # Hit something that's not properly indented for class content (next class)
                                    break
                                j += 1
                            insertion_point = j
                            break

                    if insertion_point >= 0:
                        content_lines.insert(
                            insertion_point, union_fields_content.rstrip()
                        )

                        # Add discriminated union field configuration
                        union_fields = {}
                        for oneof_full_name, oneof_config in one_of_dict.items():
                            oneof_name = oneof_full_name.split(".")[-1]
                            fields = sorted(list(oneof_config["fields"]))
                            
                            # Create alias mapping for camelCase support
                            aliases = {}
                            for field in fields:
                                # Always map snake_case to itself
                                aliases[field] = field
                                # Convert to camelCase and map to snake_case
                                # Simple conversion: location_value -> locationValue
                                parts = field.split('_')
                                if len(parts) > 1:
                                    camel_case = parts[0] + ''.join(word.capitalize() for word in parts[1:])
                                    aliases[camel_case] = field
                            
                            union_fields[oneof_name] = {
                                "fields": fields,
                                "aliases": aliases
                            }

                        config_content = f"\n{' ' * (indent + self.code_indent)}_oneof_fields = {self._get_value_code(union_fields)}\n"

                        # No need for validator_content - it's added automatically by __init_subclass__
                        validator_content = ""

                        if config_content or validator_content:
                            # Find the end of the class to add the configuration
                            end_of_class = len(content_lines)
                            for i in range(insertion_point + 1, len(content_lines)):
                                if content_lines[i].strip() and not content_lines[
                                    i
                                ].startswith(" " * indent):
                                    # Found the next class or top-level code
                                    end_of_class = i
                                    break

                            # Insert configuration after union fields
                            if end_of_class > insertion_point:
                                # Insert config first, then validator
                                content_lines.insert(
                                    insertion_point + 1, config_content
                                )
                                content_lines.insert(
                                    insertion_point + 2, validator_content
                                )

                        content = "\n".join(content_lines)
        else:
            content = "\n".join(
                [
                    i
                    for i in [
                        class_name_content,
                        class_head_content,
                        class_field_content,
                        class_validate_handler_content,
                    ]
                    if i
                ]
            )

        if not any([class_head_content, class_field_content]):
            content += "\n" + " " * (indent + self.code_indent) + "pass\n"
        use_model_cache[class_name] = content
        return content

    def _get_protobuf_type_model(
        self, field: FieldDescriptorProto
    ) -> ProtobufTypeModel:
        def _get_type_factory(module_name: str, message_name: str) -> Any:
            try:
                return getattr(importlib.import_module(module_name), message_name)
            except ModuleNotFoundError:
                details = {
                    "field name": field.name,
                    "field type name": field.type_name[1:],
                    "field type": field.type,
                }
                raise ModuleNotFoundError(
                    "Can't find protobuf type module, "
                    "please check that config.protobuf_type_config is configured correctly!"
                    f"  details info: {details}"
                )

        type_factory: Optional[Any] = None
        use_custom_type = False
        if field.type in protobuf_desc_python_type_dict:
            type_factory = protobuf_desc_python_type_dict[field.type]
            return ProtobufTypeModel(
                type_factory=type_factory,
                py_type_str=self._get_value_code(type_factory),
                rule_type_str=protobuf_common_type_dict.get(field.type, ""),
            )
        elif field.type_name.startswith(".google.protobuf"):
            _type_str = field.type_name.split(".")[-1]
            protobuf_type_config_key = field.type_name[1:]
            if protobuf_type_config_key in self.config.protobuf_type_config:
                # Through configuration, users can define the type of Protobuf they want
                rule_type_str = "any"
                use_custom_type = self.config.protobuf_type_config[
                    protobuf_type_config_key
                ].is_custom
                type_module_name = self.config.protobuf_type_config[
                    protobuf_type_config_key
                ].module_name
                _type_str = self.config.protobuf_type_config[
                    protobuf_type_config_key
                ].message_name
                py_type_str = _type_str  # rewrite py_type_str
                type_factory = _get_type_factory(type_module_name, _type_str)
                self._add_import_code(type_module_name, _type_str)
            elif _type_str == "Empty":
                py_type_str = "None"
                rule_type_str = ""
            elif _type_str == "Timestamp":
                py_type_str = "TimestampType"
                rule_type_str = "timestamp"
                type_factory = FormatContainer("datetime_utc_now")
                self._add_import_code("protobuf_to_pydantic.util", "TimestampType")
                self._add_import_code("protobuf_to_pydantic.util", "datetime_utc_now")
            elif _type_str == "Duration":
                rule_type_str = "duration"
                type_factory = timedelta
                py_type_str = "DurationType"

                self._add_import_code("protobuf_to_pydantic.util", "DurationType")
            elif _type_str == "Any":
                py_type_str = "Any"
                rule_type_str = "any"
                type_factory = AnyMessage
                use_custom_type = True
                self._add_import_code("google.protobuf.any_pb2", "Any")
            elif _type_str == "Struct":
                py_type_str = "typing.Dict[str, typing.Any]"
                rule_type_str = "struct"
                type_factory = dict
                self._add_import_code("typing")
            elif _type_str == "Value":
                py_type_str = "ValueType"
                rule_type_str = "any"
                type_factory = None
                self._add_import_code("protobuf_to_pydantic.util", "ValueType")
            elif field.type_name.startswith(".google.protobuf"):
                py_type_str = _type_str
                rule_type_str = "any"
                use_custom_type = True

                if field.type_name in self._descriptors.message_to_fd:
                    message_fd = self._descriptors.message_to_fd[field.type_name]
                    # google/protobuf/wrappers.proto -> google.protobuf.wrappers_pb2
                    type_module_name = (
                        message_fd.name.split(".")[0].replace("/", ".") + "_pb2"
                    )
                else:
                    type_module_name = (
                        "google.protobuf." + camel_to_snake(_type_str) + "_pb2"
                    )

                type_factory = _get_type_factory(type_module_name, _type_str)
                self._add_import_code(type_module_name, _type_str)
            else:
                logger.error(f"Not support type {field.type_name}")
                py_type_str = "Any"
                rule_type_str = "any"
                use_custom_type = True
                type_factory = AnyMessage
                self._add_import_code("google.protobuf.any_pb2", "Any")
            return ProtobufTypeModel(
                type_factory=type_factory,
                rule_type_str=rule_type_str,
                py_type_str=py_type_str,
                use_custom_type=use_custom_type,
            )
        else:
            py_type_str = field.type_name.split(".")[-1]
            if field.type_name in self._descriptors.message_to_fd:
                message_fd = self._descriptors.message_to_fd[field.type_name]
                self._add_other_module_pkg(message_fd, py_type_str)

            return ProtobufTypeModel(
                # When relying on other Messages, it will only be used in the type of pydantic.Model,
                # and the type_ field will not be used at this time
                type_factory=py_type_str,
                rule_type_str="message",
                py_type_str=py_type_str,
            )

    def _parse_field_descriptor(self) -> None:
        # Don't Delete, Can use comment parse debug
        # print(self.source_code_info_by_scl, file=sys.stderr)
        # print(FileDescriptorProto.NAME_FIELD_NUMBER, file=sys.stderr)
        # print(FileDescriptorProto.PACKAGE_FIELD_NUMBER, file=sys.stderr)
        # print(FileDescriptorProto.PUBLIC_DEPENDENCY_FIELD_NUMBER, file=sys.stderr)
        # print(FileDescriptorProto.WEAK_DEPENDENCY_FIELD_NUMBER, file=sys.stderr)
        # print(FileDescriptorProto.MESSAGE_TYPE_FIELD_NUMBER, file=sys.stderr)
        # print(FileDescriptorProto.ENUM_TYPE_FIELD_NUMBER, file=sys.stderr)
        # print(FileDescriptorProto.SERVICE_FIELD_NUMBER, file=sys.stderr)
        # print(FileDescriptorProto.EXTENSION_FIELD_NUMBER, file=sys.stderr)
        # print(FileDescriptorProto.OPTIONS_FIELD_NUMBER, file=sys.stderr)
        # print(FileDescriptorProto.SOURCE_CODE_INFO_FIELD_NUMBER, file=sys.stderr)
        # print(FileDescriptorProto.SYNTAX_FIELD_NUMBER, file=sys.stderr)
        # print(DescriptorProto.NAME_FIELD_NUMBER, file=sys.stderr)
        # print(DescriptorProto.FIELD_FIELD_NUMBER, file=sys.stderr)
        # print(DescriptorProto.EXTENSION_FIELD_NUMBER, file=sys.stderr)
        # print(DescriptorProto.NESTED_TYPE_FIELD_NUMBER, file=sys.stderr)
        # print(DescriptorProto.ENUM_TYPE_FIELD_NUMBER, file=sys.stderr)
        # print(DescriptorProto.EXTENSION_RANGE_FIELD_NUMBER, file=sys.stderr)
        # print(DescriptorProto.ONEOF_DECL_FIELD_NUMBER, file=sys.stderr)
        # print(DescriptorProto.OPTIONS_FIELD_NUMBER, file=sys.stderr)
        # print(DescriptorProto.RESERVED_RANGE_FIELD_NUMBER, file=sys.stderr)
        # print(DescriptorProto.RESERVED_NAME_FIELD_NUMBER, file=sys.stderr)
        self._content_deque.append(
            "\n\n".join(
                self._enum(
                    self._fd.enum_type, [FileDescriptorProto.ENUM_TYPE_FIELD_NUMBER]
                )
            )
        )
        for index, desc in enumerate(self._fd.message_type):
            self._content_deque.append(
                self._message(
                    desc=desc,
                    root_desc=desc,
                    scl_prefix=[FileDescriptorProto.MESSAGE_TYPE_FIELD_NUMBER, index],
                    sub_model_cache=self._model_cache,
                )
            )
