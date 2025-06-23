from typing import Any

from expecttest import assert_expected_inline
from google.protobuf import __version__

from tests.test_gen_code.test_helper import P2CNoHeader

if __version__ > "4.0.0":
    from example.proto_pydanticv2.example.example_proto.demo import (
        demo_pb2,
        diff_pkg_refer_2_pb2,
    )
else:
    from example.proto_3_20_pydanticv2.example.example_proto.demo import (
        demo_pb2,
        diff_pkg_refer_2_pb2,
    )

from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_code
from protobuf_to_pydantic.gen_model import clear_create_model_cache


class TestSimpleTest:
    @staticmethod
    def _model_output(msg: Any) -> str:
        # Make sure that the cache pool is clean before each build
        clear_create_model_cache()
        return pydantic_model_to_py_code(
            msg_to_pydantic_model(msg, parse_msg_desc_method="ignore"),
            p2c_class=P2CNoHeader,
        )

    def test_empty_message(self) -> None:
        output = self._model_output(demo_pb2.EmptyMessage)  # type: ignore
        assert_expected_inline(
            output,
            """\
class EmptyMessage(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )
""",
        )

    def test_user_message(self) -> None:
        output = self._model_output(demo_pb2.UserMessage)  # type: ignore
        assert_expected_inline(
            output,
            """\
class SexType(IntEnum):
    man = 0
    women = 1


class ExampleExampleProtoCommonSingleDemoEnum(IntEnum):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoEnum protobuf path:example/example_proto/common/single.proto\"\"\"

    zero = 0
    one = 1
    two = 3


class ExampleExampleProtoCommonSingleDemoMessage(BaseModel):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoMessage protobuf path:example/example_proto/common/single.proto\"\"\"

    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    earth: str = Field(default="", alias_priority=1, validation_alias="earth", serialization_alias="earth")
    mercury: str = Field(default="", alias_priority=1, validation_alias="mercury", serialization_alias="mercury")
    mars: str = Field(default="", alias_priority=1, validation_alias="mars", serialization_alias="mars")


class UserMessage(BaseModel):
    model_config = ConfigDict(
        validate_default=True,
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    uid: str = Field(default="", alias_priority=1, validation_alias="uid", serialization_alias="uid")
    age: int = Field(default=0, alias_priority=1, validation_alias="age", serialization_alias="age")
    height: float = Field(default=0.0, alias_priority=1, validation_alias="height", serialization_alias="height")
    sex: SexType = Field(default=0, alias_priority=1, validation_alias="sex", serialization_alias="sex")
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(
        default=0, alias_priority=1, validation_alias="demo", serialization_alias="demo"
    )
    is_adult: bool = Field(default=False, alias_priority=1, validation_alias="isAdult", serialization_alias="isAdult")
    user_name: str = Field(default="", alias_priority=1, validation_alias="userName", serialization_alias="userName")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage,
        alias_priority=1,
        validation_alias="demoMessage",
        serialization_alias="demoMessage",
    )
""",
        )

    def test_other_message(self) -> None:
        output = self._model_output(demo_pb2.OtherMessage)  # type: ignore
        assert_expected_inline(
            output,
            """\
class OtherMessage(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        arbitrary_types_allowed=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    metadata: typing.Dict[str, typing.Any] = Field(
        default_factory=dict, alias_priority=1, validation_alias="metadata", serialization_alias="metadata"
    )
    double_value: DoubleValue = Field(
        default_factory=DoubleValue, alias_priority=1, validation_alias="doubleValue", serialization_alias="doubleValue"
    )
    field_mask: typing.Optional[FieldMask] = Field(
        default_factory=FieldMask, alias_priority=1, validation_alias="fieldMask", serialization_alias="fieldMask"
    )
""",
        )

    def test_map_message(self) -> None:
        output = self._model_output(demo_pb2.MapMessage)  # type: ignore
        assert_expected_inline(
            output,
            """\
class SexType(IntEnum):
    man = 0
    women = 1


class ExampleExampleProtoCommonSingleDemoEnum(IntEnum):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoEnum protobuf path:example/example_proto/common/single.proto\"\"\"

    zero = 0
    one = 1
    two = 3


class ExampleExampleProtoCommonSingleDemoMessage(BaseModel):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoMessage protobuf path:example/example_proto/common/single.proto\"\"\"

    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    earth: str = Field(default="", alias_priority=1, validation_alias="earth", serialization_alias="earth")
    mercury: str = Field(default="", alias_priority=1, validation_alias="mercury", serialization_alias="mercury")
    mars: str = Field(default="", alias_priority=1, validation_alias="mars", serialization_alias="mars")


class UserMessage(BaseModel):
    model_config = ConfigDict(
        validate_default=True,
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    uid: str = Field(default="", alias_priority=1, validation_alias="uid", serialization_alias="uid")
    age: int = Field(default=0, alias_priority=1, validation_alias="age", serialization_alias="age")
    height: float = Field(default=0.0, alias_priority=1, validation_alias="height", serialization_alias="height")
    sex: SexType = Field(default=0, alias_priority=1, validation_alias="sex", serialization_alias="sex")
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(
        default=0, alias_priority=1, validation_alias="demo", serialization_alias="demo"
    )
    is_adult: bool = Field(default=False, alias_priority=1, validation_alias="isAdult", serialization_alias="isAdult")
    user_name: str = Field(default="", alias_priority=1, validation_alias="userName", serialization_alias="userName")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage,
        alias_priority=1,
        validation_alias="demoMessage",
        serialization_alias="demoMessage",
    )


class MapMessage(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    user_map: typing.Dict[str, UserMessage] = Field(
        default_factory=dict, alias_priority=1, validation_alias="userMap", serialization_alias="userMap"
    )
    user_flag: typing.Dict[str, bool] = Field(
        default_factory=dict, alias_priority=1, validation_alias="userFlag", serialization_alias="userFlag"
    )
""",
        )

    def test_repeated_message(self) -> None:
        output = self._model_output(demo_pb2.RepeatedMessage)  # type: ignore
        assert_expected_inline(
            output,
            """\
class SexType(IntEnum):
    man = 0
    women = 1


class ExampleExampleProtoCommonSingleDemoEnum(IntEnum):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoEnum protobuf path:example/example_proto/common/single.proto\"\"\"

    zero = 0
    one = 1
    two = 3


class ExampleExampleProtoCommonSingleDemoMessage(BaseModel):
    \"\"\"Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoMessage protobuf path:example/example_proto/common/single.proto\"\"\"

    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    earth: str = Field(default="", alias_priority=1, validation_alias="earth", serialization_alias="earth")
    mercury: str = Field(default="", alias_priority=1, validation_alias="mercury", serialization_alias="mercury")
    mars: str = Field(default="", alias_priority=1, validation_alias="mars", serialization_alias="mars")


class UserMessage(BaseModel):
    model_config = ConfigDict(
        validate_default=True,
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    uid: str = Field(default="", alias_priority=1, validation_alias="uid", serialization_alias="uid")
    age: int = Field(default=0, alias_priority=1, validation_alias="age", serialization_alias="age")
    height: float = Field(default=0.0, alias_priority=1, validation_alias="height", serialization_alias="height")
    sex: SexType = Field(default=0, alias_priority=1, validation_alias="sex", serialization_alias="sex")
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(
        default=0, alias_priority=1, validation_alias="demo", serialization_alias="demo"
    )
    is_adult: bool = Field(default=False, alias_priority=1, validation_alias="isAdult", serialization_alias="isAdult")
    user_name: str = Field(default="", alias_priority=1, validation_alias="userName", serialization_alias="userName")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage,
        alias_priority=1,
        validation_alias="demoMessage",
        serialization_alias="demoMessage",
    )


class RepeatedMessage(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    str_list: typing.List[str] = Field(
        default_factory=list, alias_priority=1, validation_alias="strList", serialization_alias="strList"
    )
    int_list: typing.List[int] = Field(
        default_factory=list, alias_priority=1, validation_alias="intList", serialization_alias="intList"
    )
    user_list: typing.List[UserMessage] = Field(
        default_factory=list, alias_priority=1, validation_alias="userList", serialization_alias="userList"
    )
""",
        )

    def test_nested_message(self) -> None:
        output = self._model_output(demo_pb2.NestedMessage)
        assert_expected_inline(
            output,
            '''\
class SexType(IntEnum):
    man = 0
    women = 1


class ExampleExampleProtoCommonSingleDemoEnum(IntEnum):
    """Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoEnum protobuf path:example/example_proto/common/single.proto"""

    zero = 0
    one = 1
    two = 3


class ExampleExampleProtoCommonSingleDemoMessage(BaseModel):
    """Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoMessage protobuf path:example/example_proto/common/single.proto"""

    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    earth: str = Field(default="", alias_priority=1, validation_alias="earth", serialization_alias="earth")
    mercury: str = Field(default="", alias_priority=1, validation_alias="mercury", serialization_alias="mercury")
    mars: str = Field(default="", alias_priority=1, validation_alias="mars", serialization_alias="mars")


class UserMessage(BaseModel):
    model_config = ConfigDict(
        validate_default=True,
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    uid: str = Field(default="", alias_priority=1, validation_alias="uid", serialization_alias="uid")
    age: int = Field(default=0, alias_priority=1, validation_alias="age", serialization_alias="age")
    height: float = Field(default=0.0, alias_priority=1, validation_alias="height", serialization_alias="height")
    sex: SexType = Field(default=0, alias_priority=1, validation_alias="sex", serialization_alias="sex")
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(
        default=0, alias_priority=1, validation_alias="demo", serialization_alias="demo"
    )
    is_adult: bool = Field(default=False, alias_priority=1, validation_alias="isAdult", serialization_alias="isAdult")
    user_name: str = Field(default="", alias_priority=1, validation_alias="userName", serialization_alias="userName")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage,
        alias_priority=1,
        validation_alias="demoMessage",
        serialization_alias="demoMessage",
    )


class RepeatedMessage(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    str_list: typing.List[str] = Field(
        default_factory=list, alias_priority=1, validation_alias="strList", serialization_alias="strList"
    )
    int_list: typing.List[int] = Field(
        default_factory=list, alias_priority=1, validation_alias="intList", serialization_alias="intList"
    )
    user_list: typing.List[UserMessage] = Field(
        default_factory=list, alias_priority=1, validation_alias="userList", serialization_alias="userList"
    )


class MapMessage(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    user_map: typing.Dict[str, UserMessage] = Field(
        default_factory=dict, alias_priority=1, validation_alias="userMap", serialization_alias="userMap"
    )
    user_flag: typing.Dict[str, bool] = Field(
        default_factory=dict, alias_priority=1, validation_alias="userFlag", serialization_alias="userFlag"
    )


class AfterReferMessage(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    uid: str = Field(default="", alias_priority=1, validation_alias="uid", serialization_alias="uid")
    age: int = Field(default=0, alias_priority=1, validation_alias="age", serialization_alias="age")


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        model_config = ConfigDict(
            alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
            populate_by_name=True,
            serialize_by_alias=True,
            validate_by_alias=True,
            validate_by_name=True,
        )

        bank_number: str = Field(
            default="", alias_priority=1, validation_alias="bankNumber", serialization_alias="bankNumber"
        )
        exp: datetime = Field(
            default_factory=datetime.now, alias_priority=1, validation_alias="exp", serialization_alias="exp"
        )
        uuid: str = Field(default="", alias_priority=1, validation_alias="uuid", serialization_alias="uuid")

    class IncludeEnum(IntEnum):
        zero = 0
        one = 1
        two = 2

    model_config = ConfigDict(validate_default=True)

    user_list_map: typing.Dict[str, RepeatedMessage] = Field(default_factory=dict)
    user_map: typing.Dict[str, MapMessage] = Field(default_factory=dict)
    user_pay: UserPayMessage = Field(default_factory=UserPayMessage)
    include_enum: IncludeEnum = Field(default=0)
    not_enable_user_pay: UserPayMessage = Field(default_factory=UserPayMessage)
    empty: typing.Any = Field()
    after_refer: AfterReferMessage = Field(default_factory=AfterReferMessage)
''',
        )

    def test_invoice_item(self) -> None:
        output = self._model_output(demo_pb2.InvoiceItem)
        assert_expected_inline(
            output,
            """\
class InvoiceItem(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    name: str = Field(default="", alias_priority=1, validation_alias="name", serialization_alias="name")
    amount: int = Field(default=0, alias_priority=1, validation_alias="amount", serialization_alias="amount")
    quantity: int = Field(default=0, alias_priority=1, validation_alias="quantity", serialization_alias="quantity")
    items: typing.List["InvoiceItem"] = Field(
        default_factory=list, alias_priority=1, validation_alias="items", serialization_alias="items"
    )
""",
        )

    def test_self_referencing(self) -> None:
        output = self._model_output(demo_pb2.OptionalMessage)
        assert_expected_inline(
            output,
            """\
class InvoiceItem(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    name: str = Field(default="", alias_priority=1, validation_alias="name", serialization_alias="name")
    amount: int = Field(default=0, alias_priority=1, validation_alias="amount", serialization_alias="amount")
    quantity: int = Field(default=0, alias_priority=1, validation_alias="quantity", serialization_alias="quantity")
    items: typing.List["InvoiceItem"] = Field(
        default_factory=list, alias_priority=1, validation_alias="items", serialization_alias="items"
    )


class OptionalMessage(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    _one_of_dict = {"user.OptionalMessage.a": {"fields": {"x", "y"}, "required": False}}

    x: str = Field(default="", alias_priority=1, validation_alias="x", serialization_alias="x")
    y: int = Field(default=0, alias_priority=1, validation_alias="y", serialization_alias="y")
    name: typing.Optional[str] = Field(
        default="", alias_priority=1, validation_alias="name", serialization_alias="name"
    )
    age: typing.Optional[int] = Field(default=0, alias_priority=1, validation_alias="age", serialization_alias="age")
    item: typing.Optional[InvoiceItem] = Field(
        default_factory=InvoiceItem, alias_priority=1, validation_alias="item", serialization_alias="item"
    )
    str_list: typing.List[str] = Field(
        default_factory=list, alias_priority=1, validation_alias="strList", serialization_alias="strList"
    )
    int_map: typing.Dict[str, int] = Field(
        default_factory=dict, alias_priority=1, validation_alias="intMap", serialization_alias="intMap"
    )
    default_template_test: float = Field(
        default=0.0, alias_priority=1, validation_alias="defaultTemplateTest", serialization_alias="defaultTemplateTest"
    )

    one_of_validator = model_validator(mode="before")(check_one_of)
""",
        )

    def test_circular_references(self) -> None:
        output = self._model_output(demo_pb2.InvoiceItem2)
        assert_expected_inline(
            output,
            """\
class Invoice3(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    name: str = Field(default="", alias_priority=1, validation_alias="name", serialization_alias="name")
    amount: int = Field(default=0, alias_priority=1, validation_alias="amount", serialization_alias="amount")
    quantity: int = Field(default=0, alias_priority=1, validation_alias="quantity", serialization_alias="quantity")
    items: typing.List["InvoiceItem2"] = Field(default_factory=list)


class InvoiceItem2(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    name: str = Field(default="", alias_priority=1, validation_alias="name", serialization_alias="name")
    amount: int = Field(default=0, alias_priority=1, validation_alias="amount", serialization_alias="amount")
    quantity: int = Field(default=0, alias_priority=1, validation_alias="quantity", serialization_alias="quantity")
    items: typing.List["InvoiceItem2"] = Field(
        default_factory=list, alias_priority=1, validation_alias="items", serialization_alias="items"
    )
    invoice: Invoice3 = Field(
        default_factory=Invoice3, alias_priority=1, validation_alias="invoice", serialization_alias="invoice"
    )
""",
        )

    def test_message_reference(self) -> None:
        output = self._model_output(demo_pb2.RootMessage)
        assert_expected_inline(
            output,
            """\
class AnOtherMessage(BaseModel):
    class SubMessage(BaseModel):
        model_config = ConfigDict(
            alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
            populate_by_name=True,
            serialize_by_alias=True,
            validate_by_alias=True,
            validate_by_name=True,
        )

        text: str = Field(default="", alias_priority=1, validation_alias="text", serialization_alias="text")

    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    field1: str = Field(default="", alias_priority=1, validation_alias="field1", serialization_alias="field1")
    field2: SubMessage = Field(
        default_factory=SubMessage, alias_priority=1, validation_alias="field2", serialization_alias="field2"
    )


class RootMessage(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    field1: str = Field(default="", alias_priority=1, validation_alias="field1", serialization_alias="field1")
    field2: AnOtherMessage = Field(
        default_factory=AnOtherMessage, alias_priority=1, validation_alias="field2", serialization_alias="field2"
    )
""",
        )

    def test_same_bane_inline_structure(self) -> None:
        output = self._model_output(demo_pb2.TestSameName0)
        assert_expected_inline(
            output,
            """\
class TestSameName0(BaseModel):
    class Body(BaseModel):
        model_config = ConfigDict(
            alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
            populate_by_name=True,
            serialize_by_alias=True,
            validate_by_alias=True,
            validate_by_name=True,
        )

        input_model: str = Field(
            default="", alias_priority=1, validation_alias="inputModel", serialization_alias="inputModel"
        )
        input_info: typing.Dict[str, str] = Field(
            default_factory=dict, alias_priority=1, validation_alias="inputInfo", serialization_alias="inputInfo"
        )

    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    body: Body = Field(default_factory=Body, alias_priority=1, validation_alias="body", serialization_alias="body")
""",
        )

        output = self._model_output(demo_pb2.TestSameName1)
        assert_expected_inline(
            output,
            """\
class TestSameName1(BaseModel):
    class Body(BaseModel):
        model_config = ConfigDict(
            alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
            populate_by_name=True,
            serialize_by_alias=True,
            validate_by_alias=True,
            validate_by_name=True,
        )

        output_model: str = Field(
            default="", alias_priority=1, validation_alias="outputModel", serialization_alias="outputModel"
        )
        output_info: typing.Dict[str, str] = Field(
            default_factory=dict, alias_priority=1, validation_alias="outputInfo", serialization_alias="outputInfo"
        )

    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    body: Body = Field(default_factory=Body, alias_priority=1, validation_alias="body", serialization_alias="body")
""",
        )

    def test_diff_pkg_refer(self) -> None:
        output = self._model_output(diff_pkg_refer_2_pb2.Demo2)
        assert_expected_inline(
            output,
            '''class ExampleExampleProtoDemoDiffPkgRefer1Demo1(BaseModel):
    """Note: The current class does not belong to the package
    ExampleExampleProtoDemoDiffPkgRefer1Demo1 protobuf path:example/example_proto/demo/diff_pkg_refer_1.proto"""


class Demo2(BaseModel):
    myField: typing.Dict[str, ExampleExampleProtoDemoDiffPkgRefer1Demo1] = Field(default_factory=dict)
''',
        )

    def test_optional_enum(self) -> None:
        output = self._model_output(demo_pb2.WithOptionalEnumMsgEntry)
        assert_expected_inline(
            output,
            """class OptionalEnum(IntEnum):
    FOO = 0
    BAR = 1
    BAZ = 2


class WithOptionalEnumMsgEntry(BaseModel):
    model_config = ConfigDict(
        validate_default=True,
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    enum: typing.Optional[OptionalEnum] = Field(
        default=0, alias_priority=1, validation_alias="enum", serialization_alias="enum"
    )
""",
        )
