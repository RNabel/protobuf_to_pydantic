# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing
from datetime import datetime
from enum import IntEnum
from uuid import uuid4

from example.gen_text_comment_code import exp_time
from google.protobuf.field_mask_pb2 import FieldMask  # type: ignore
from google.protobuf.wrappers_pb2 import DoubleValue  # type: ignore
from protobuf_to_pydantic.customer_validator.v2 import check_one_of
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.types import PaymentCardNumber


class AfterReferMessage(BaseModel):
    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", example=18, ge=0)


class AnOtherMessage(BaseModel):
    class SubMessage(BaseModel):
        text: str = Field(default="")

    field1: str = Field(default="")
    field2: SubMessage = Field(default_factory=SubMessage)


class DemoState(BaseModel):
    paramsDID: int = Field(default=0)


class DemoResp(BaseModel):
    demoState: typing.Dict[int, DemoState] = Field(default_factory=dict)
    pramsArea: int = Field(default=0)
    paramsSeason: bool = Field(default=False)


class EmptyMessage(BaseModel):
    pass


class InvoiceItem2(BaseModel):
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem2"] = Field(default_factory=list)
    invoice: "Invoice3" = Field()


class Invoice3(BaseModel):
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List[InvoiceItem2] = Field(default_factory=list)


class InvoiceItem(BaseModel):
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem"] = Field(default_factory=list)


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

    earth: str = Field(default="")
    mercury: str = Field(default="")
    mars: str = Field(default="")


class UserMessage(BaseModel):
    model_config = ConfigDict(validate_default=True)

    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", example=18, ge=0)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", description="user name", example="so1n", min_length=1, max_length=10)
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage, customer_string="c1", customer_int=1
    )


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = Field(default_factory=dict)
    user_flag: typing.Dict[str, bool] = Field(default_factory=dict)


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = Field(default_factory=list, min_length=3, max_length=5)
    int_list: typing.Set[int] = Field(default_factory=set, min_length=1, max_length=5)
    user_list: typing.List[UserMessage] = Field(default_factory=list)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        bank_number: PaymentCardNumber = Field(default="")
        exp: datetime = Field(default_factory=exp_time)
        uuid: str = Field(default_factory=uuid4)

    class IncludeEnum(IntEnum):
        zero = 0
        one = 1
        two = 2

    model_config = ConfigDict(validate_default=True)

    user_list_map: typing.Dict[str, RepeatedMessage] = Field(default_factory=dict)
    user_map: typing.Dict[str, MapMessage] = Field(default_factory=dict)
    user_pay: UserPayMessage = Field(default_factory=UserPayMessage)
    include_enum: IncludeEnum = Field(default=0)
    empty: typing.Any = Field()
    after_refer: AfterReferMessage = Field(default_factory=AfterReferMessage)


class OptionalMessage(BaseModel):
    _one_of_dict = {"user.OptionalMessage.a": {"fields": {"x", "yy"}, "required": False}}

    x: str = Field(default="")
    y: int = Field(default=0, alias="yy", alias_priority=2, title="use age", example=18, ge=0)
    name: typing.Optional[str] = Field(default="")
    age: typing.Optional[int] = Field(default=0)
    item: typing.Optional[InvoiceItem] = Field(default_factory=InvoiceItem)
    str_list: typing.List[str] = Field(default_factory=list)
    int_map: typing.Dict[str, int] = Field(default_factory=dict)
    default_template_test: float = Field(default=1600000000.0)

    one_of_validator = model_validator(mode="before")(check_one_of)


class OtherMessage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    metadata: typing.Dict[str, typing.Any] = Field(default_factory=dict)
    double_value: DoubleValue = Field(default_factory=DoubleValue)
    field_mask: typing.Optional[FieldMask] = Field(default_factory=FieldMask)


class RootMessage(BaseModel):
    field1: str = Field(default="")
    field2: AnOtherMessage = Field(default_factory=AnOtherMessage)


class TestSameName0(BaseModel):
    class Body(BaseModel):
        input_model: str = Field(default="")
        input_info: typing.Dict[str, str] = Field(default_factory=dict)

    body: Body = Field(default_factory=Body)


class TestSameName1(BaseModel):
    class Body(BaseModel):
        output_model: str = Field(default="")
        output_info: typing.Dict[str, str] = Field(default_factory=dict)

    body: Body = Field(default_factory=Body)


class OptionalEnum(IntEnum):
    FOO = 0
    BAR = 1
    BAZ = 2


class WithOptionalEnumMsgEntry(BaseModel):
    model_config = ConfigDict(validate_default=True)

    enum: typing.Optional[OptionalEnum] = Field(default=0)
