# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing
from datetime import datetime
from enum import IntEnum

import typing_extensions
from google.protobuf.field_mask_pb2 import FieldMask  # type: ignore
from google.protobuf.wrappers_pb2 import DoubleValue  # type: ignore
from protobuf_to_pydantic.customer_validator.v2 import check_one_of
from protobuf_to_pydantic.default_base_model import ProtobufCompatibleBaseModel
from protobuf_to_pydantic.util import datetime_utc_now, timestamp_serializer
from pydantic import ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel
from pydantic.aliases import AliasGenerator
from pydantic.functional_serializers import PlainSerializer


class AfterReferMessage(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    uid: str = Field(default="", alias_priority=1, validation_alias="uid", serialization_alias="uid")
    age: int = Field(default=0, alias_priority=1, validation_alias="age", serialization_alias="age")


class AnOtherMessage(ProtobufCompatibleBaseModel):
    class SubMessage(ProtobufCompatibleBaseModel):
        model_config = ConfigDict(
            ser_json_inf_nan="strings",
            alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
            populate_by_name=True,
            validate_by_alias=True,
            validate_by_name=True,
            serialize_by_alias=True,
        )

        text: str = Field(default="", alias_priority=1, validation_alias="text", serialization_alias="text")

    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    field1: str = Field(default="", alias_priority=1, validation_alias="field1", serialization_alias="field1")
    field2: SubMessage = Field(
        default_factory=SubMessage, alias_priority=1, validation_alias="field2", serialization_alias="field2"
    )


class DemoState(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    paramsDID: int = Field(default=0, alias_priority=1, validation_alias="paramsDID", serialization_alias="paramsDID")


class DemoResp(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    demoState: typing.Dict[int, DemoState] = Field(
        default_factory=dict, alias_priority=1, validation_alias="demoState", serialization_alias="demoState"
    )
    pramsArea: int = Field(default=0, alias_priority=1, validation_alias="pramsArea", serialization_alias="pramsArea")
    paramsSeason: bool = Field(
        default=False, alias_priority=1, validation_alias="paramsSeason", serialization_alias="paramsSeason"
    )


class EmptyMessage(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )


class InvoiceItem2(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    name: str = Field(default="", alias_priority=1, validation_alias="name", serialization_alias="name")
    amount: int = Field(default=0, alias_priority=1, validation_alias="amount", serialization_alias="amount")
    quantity: int = Field(default=0, alias_priority=1, validation_alias="quantity", serialization_alias="quantity")
    items: typing.List["InvoiceItem2"] = Field(
        default_factory=list, alias_priority=1, validation_alias="items", serialization_alias="items"
    )
    invoice: "Invoice3" = Field()


class Invoice3(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    name: str = Field(default="", alias_priority=1, validation_alias="name", serialization_alias="name")
    amount: int = Field(default=0, alias_priority=1, validation_alias="amount", serialization_alias="amount")
    quantity: int = Field(default=0, alias_priority=1, validation_alias="quantity", serialization_alias="quantity")
    items: typing.List[InvoiceItem2] = Field(
        default_factory=list, alias_priority=1, validation_alias="items", serialization_alias="items"
    )


class InvoiceItem(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    name: str = Field(default="", alias_priority=1, validation_alias="name", serialization_alias="name")
    amount: int = Field(default=0, alias_priority=1, validation_alias="amount", serialization_alias="amount")
    quantity: int = Field(default=0, alias_priority=1, validation_alias="quantity", serialization_alias="quantity")
    items: typing.List["InvoiceItem"] = Field(
        default_factory=list, alias_priority=1, validation_alias="items", serialization_alias="items"
    )


class SexType(IntEnum):
    man = 0
    women = 1


class ExampleExampleProtoCommonSingleDemoEnum(IntEnum):
    """Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoEnum protobuf path:example/example_proto/common/single.proto"""

    zero = 0
    one = 1
    two = 3


class ExampleExampleProtoCommonSingleDemoMessage(ProtobufCompatibleBaseModel):
    """Note: The current class does not belong to the package
    ExampleExampleProtoCommonSingleDemoMessage protobuf path:example/example_proto/common/single.proto"""

    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    earth: str = Field(default="", alias_priority=1, validation_alias="earth", serialization_alias="earth")
    mercury: str = Field(default="", alias_priority=1, validation_alias="mercury", serialization_alias="mercury")
    mars: str = Field(default="", alias_priority=1, validation_alias="mars", serialization_alias="mars")


class UserMessage(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        validate_default=True,
        serialize_by_alias=True,
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


class MapMessage(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    user_map: typing.Dict[str, UserMessage] = Field(
        default_factory=dict, alias_priority=1, validation_alias="userMap", serialization_alias="userMap"
    )
    user_flag: typing.Dict[str, bool] = Field(
        default_factory=dict, alias_priority=1, validation_alias="userFlag", serialization_alias="userFlag"
    )


class RepeatedMessage(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
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


class NestedMessage(ProtobufCompatibleBaseModel):
    class UserPayMessage(ProtobufCompatibleBaseModel):
        model_config = ConfigDict(
            ser_json_inf_nan="strings",
            alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
            populate_by_name=True,
            validate_by_alias=True,
            validate_by_name=True,
            serialize_by_alias=True,
        )

        bank_number: str = Field(
            default="", alias_priority=1, validation_alias="bankNumber", serialization_alias="bankNumber"
        )
        exp: typing_extensions.Annotated[
            datetime, PlainSerializer(func=timestamp_serializer, return_type=str, when_used="json")
        ] = Field(default_factory=datetime_utc_now, alias_priority=1, validation_alias="exp", serialization_alias="exp")
        uuid: str = Field(default="", alias_priority=1, validation_alias="uuid", serialization_alias="uuid")

    class IncludeEnum(IntEnum):
        zero = 0
        one = 1
        two = 2

    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        validate_default=True,
        serialize_by_alias=True,
    )

    user_list_map: typing.Dict[str, RepeatedMessage] = Field(
        default_factory=dict, alias_priority=1, validation_alias="userListMap", serialization_alias="userListMap"
    )
    user_map: typing.Dict[str, MapMessage] = Field(
        default_factory=dict, alias_priority=1, validation_alias="userMap", serialization_alias="userMap"
    )
    user_pay: UserPayMessage = Field(
        default_factory=UserPayMessage, alias_priority=1, validation_alias="userPay", serialization_alias="userPay"
    )
    include_enum: IncludeEnum = Field(
        default=0, alias_priority=1, validation_alias="includeEnum", serialization_alias="includeEnum"
    )
    not_enable_user_pay: UserPayMessage = Field(
        default_factory=UserPayMessage,
        alias_priority=1,
        validation_alias="notEnableUserPay",
        serialization_alias="notEnableUserPay",
    )
    empty: typing.Any = Field(alias_priority=1, validation_alias="empty", serialization_alias="empty")
    after_refer: AfterReferMessage = Field(
        default_factory=AfterReferMessage,
        alias_priority=1,
        validation_alias="afterRefer",
        serialization_alias="afterRefer",
    )


class WithOptionalOneofMsgEntry(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    _one_of_dict = {"user.WithOptionalOneofMsgEntry.a": {"fields": {"x", "y"}, "required": False}}

    x: str = Field(default="", alias_priority=1, validation_alias="x", serialization_alias="x")
    y: int = Field(default=0, alias_priority=1, validation_alias="y", serialization_alias="y")

    one_of_validator = model_validator(mode="before")(check_one_of)


class NestedWithOptOneOfEntry(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    x: WithOptionalOneofMsgEntry = Field(
        default_factory=WithOptionalOneofMsgEntry, alias_priority=1, validation_alias="x", serialization_alias="x"
    )


class OptionalMessage(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
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


class OtherMessage(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
        arbitrary_types_allowed=True,
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


class RootMessage(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    field1: str = Field(default="", alias_priority=1, validation_alias="field1", serialization_alias="field1")
    field2: AnOtherMessage = Field(
        default_factory=AnOtherMessage, alias_priority=1, validation_alias="field2", serialization_alias="field2"
    )


class TestSameName0(ProtobufCompatibleBaseModel):
    class Body(ProtobufCompatibleBaseModel):
        model_config = ConfigDict(
            ser_json_inf_nan="strings",
            alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
            populate_by_name=True,
            validate_by_alias=True,
            validate_by_name=True,
            serialize_by_alias=True,
        )

        input_model: str = Field(
            default="", alias_priority=1, validation_alias="inputModel", serialization_alias="inputModel"
        )
        input_info: typing.Dict[str, str] = Field(
            default_factory=dict, alias_priority=1, validation_alias="inputInfo", serialization_alias="inputInfo"
        )

    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    body: Body = Field(default_factory=Body, alias_priority=1, validation_alias="body", serialization_alias="body")


class TestSameName1(ProtobufCompatibleBaseModel):
    class Body(ProtobufCompatibleBaseModel):
        model_config = ConfigDict(
            ser_json_inf_nan="strings",
            alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
            populate_by_name=True,
            validate_by_alias=True,
            validate_by_name=True,
            serialize_by_alias=True,
        )

        output_model: str = Field(
            default="", alias_priority=1, validation_alias="outputModel", serialization_alias="outputModel"
        )
        output_info: typing.Dict[str, str] = Field(
            default_factory=dict, alias_priority=1, validation_alias="outputInfo", serialization_alias="outputInfo"
        )

    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    body: Body = Field(default_factory=Body, alias_priority=1, validation_alias="body", serialization_alias="body")


class OptionalEnum(IntEnum):
    FOO = 0
    BAR = 1
    BAZ = 2


class WithOptionalEnumMsgEntry(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        validate_default=True,
        serialize_by_alias=True,
    )

    enum: typing.Optional[OptionalEnum] = Field(
        default=0, alias_priority=1, validation_alias="enum", serialization_alias="enum"
    )


class Demo1(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )


class ExampleExampleProtoDemoDiffPkgRefer1Demo1(ProtobufCompatibleBaseModel):
    """Note: The current class does not belong to the package
    ExampleExampleProtoDemoDiffPkgRefer1Demo1 protobuf path:example/example_proto/demo/diff_pkg_refer_1.proto"""

    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )


class Demo2(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    myField: typing.Dict[str, ExampleExampleProtoDemoDiffPkgRefer1Demo1] = Field(
        default_factory=dict, alias_priority=1, validation_alias="myField", serialization_alias="myField"
    )
