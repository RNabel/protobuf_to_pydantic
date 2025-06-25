# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing
from enum import IntEnum
from uuid import uuid4

from google.protobuf.field_mask_pb2 import FieldMask  # type: ignore
from google.protobuf.message import Message  # type: ignore
from google.protobuf.wrappers_pb2 import DoubleValue  # type: ignore
from pydantic import ConfigDict, Field, model_validator
from pydantic.types import PaymentCardNumber

from example.plugin_config import exp_time
from protobuf_to_pydantic.customer_validator.v2 import check_one_of
from protobuf_to_pydantic.default_base_model import ProtobufCompatibleBaseModel
from protobuf_to_pydantic.flexible_enum_mixin import FlexibleEnumMixin
from protobuf_to_pydantic.util import TimestampType

from ..common.single_p2p import DemoEnum, DemoMessage


class SexType(IntEnum, FlexibleEnumMixin):
    man = 0
    women = 1


class UserMessage(ProtobufCompatibleBaseModel):
    """
    user info
    """

    model_config = ConfigDict(validate_default=True)
    uid: typing.Optional[str] = Field(title="UID", description="user union id", example="10086")
    age: typing.Optional[int] = Field(default=0, title="use age", ge=0, example=18)
    height: typing.Optional[float] = Field(default=0.0, ge=0.0, le=2.5)
    sex: typing.Optional[SexType] = Field(default=0)
    demo: typing.Optional[DemoEnum] = Field(default=0)
    is_adult: typing.Optional[bool] = Field(default=False)
    user_name: typing.Optional[str] = Field(
        default="", description="user name", min_length=1, max_length=10, example="so1n"
    )
    demo_message: typing.Optional[DemoMessage] = Field(
        default_factory=DemoMessage, customer_string="c1", customer_int=1
    )


class OtherMessage(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    metadata: typing.Optional[typing.Dict[str, typing.Any]] = Field(default_factory=dict)
    double_value: typing.Optional[DoubleValue] = Field(default_factory=DoubleValue)
    field_mask: typing.Optional[FieldMask] = Field(default_factory=FieldMask)


class MapMessage(ProtobufCompatibleBaseModel):
    """
    test map message and bad message
    """

    user_map: typing.Optional["typing.Dict[str, UserMessage]"] = Field(default_factory=dict)
    user_flag: typing.Optional["typing.Dict[str, bool]"] = Field(default_factory=dict)


class RepeatedMessage(ProtobufCompatibleBaseModel):
    """
    test repeated msg
    """

    str_list: typing.Optional[typing.List[str]] = Field(default_factory=list, min_length=3, max_length=5)
    int_list: typing.Optional[typing.Set[int]] = Field(default_factory=set, min_length=1, max_length=5)
    user_list: typing.Optional[typing.List[UserMessage]] = Field(default_factory=list)


class AfterReferMessage(ProtobufCompatibleBaseModel):
    uid: typing.Optional[str] = Field(title="UID", description="user union id", example="10086")
    age: typing.Optional[int] = Field(default=0, title="use age", ge=0, example=18)


class NestedMessage(ProtobufCompatibleBaseModel):
    """
    test nested message
    """

    class UserPayMessage(ProtobufCompatibleBaseModel):
        bank_number: typing.Optional[PaymentCardNumber] = Field(default="")
        exp: typing.Optional[TimestampType] = Field(default_factory=exp_time)
        uuid: typing.Optional[str] = Field(default_factory=uuid4)

    class IncludeEnum(IntEnum, FlexibleEnumMixin):
        zero = 0
        one = 1
        two = 2

    model_config = ConfigDict(validate_default=True)
    user_list_map: typing.Optional["typing.Dict[str, RepeatedMessage]"] = Field(default_factory=dict)
    user_map: typing.Optional["typing.Dict[str, MapMessage]"] = Field(default_factory=dict)
    user_pay: typing.Optional["NestedMessage.UserPayMessage"] = Field(
        default_factory=lambda: NestedMessage.UserPayMessage()
    )
    include_enum: typing.Optional["NestedMessage.IncludeEnum"] = Field(default=0)
    empty: typing.Optional[None] = Field(default=None)
    after_refer: typing.Optional[AfterReferMessage] = Field(default_factory=AfterReferMessage)


class InvoiceItem(ProtobufCompatibleBaseModel):
    """
        Test self-referencing Messages
    from: https://github.com/so1n/protobuf_to_pydantic/issues/7#issuecomment-1490705932
    """

    name: typing.Optional[str] = Field(default="")
    amount: typing.Optional[int] = Field(default=0)
    quantity: typing.Optional[int] = Field(default=0)
    items: typing.Optional[typing.List["InvoiceItem"]] = Field(default_factory=list)


class EmptyMessage(ProtobufCompatibleBaseModel):
    pass


class OptionalMessage(ProtobufCompatibleBaseModel):
    _one_of_dict = {"OptionalMessage.a": {"fields": {"x", "y"}, "required": True}}
    one_of_validator = model_validator(mode="before")(check_one_of)
    x: typing.Optional[str] = Field(default="")
    y: typing.Optional[int] = Field(default=0, title="use age", ge=0, example=18)
    name: typing.Optional[str] = Field(default="")
    age: typing.Optional[int] = Field(default=0)
    item: typing.Optional[InvoiceItem] = Field(default_factory=InvoiceItem)
    str_list: typing.Optional[typing.List[str]] = Field(default_factory=list)
    int_map: typing.Optional["typing.Dict[str, int]"] = Field(default_factory=dict)
    default_template_test: typing.Optional[float] = Field(default=1600000000.0)


class Invoice3(ProtobufCompatibleBaseModel):
    name: typing.Optional[str] = Field(default="")
    amount: typing.Optional[int] = Field(default=0)
    quantity: typing.Optional[int] = Field(default=0)
    items: typing.Optional[typing.List["InvoiceItem2"]] = Field(default_factory=list)


class InvoiceItem2(ProtobufCompatibleBaseModel):
    """
        Test Circular references
    from: https://github.com/so1n/protobuf_to_pydantic/issues/57
    """

    name: typing.Optional[str] = Field(default="")
    amount: typing.Optional[int] = Field(default=0)
    quantity: typing.Optional[int] = Field(default=0)
    items: typing.Optional[typing.List["InvoiceItem2"]] = Field(default_factory=list)
    invoice: typing.Optional[Invoice3] = Field(default_factory=Invoice3)


class AnOtherMessage(ProtobufCompatibleBaseModel):
    class SubMessage(ProtobufCompatibleBaseModel):
        text: typing.Optional[str] = Field(default="")

    field1: typing.Optional[str] = Field(default="")
    field2: typing.Optional[SubMessage] = Field(default_factory=SubMessage)


class RootMessage(ProtobufCompatibleBaseModel):
    """
        Test Message references
    from: https://github.com/so1n/protobuf_to_pydantic/issues/64
    """

    field1: typing.Optional[str] = Field(default="")
    field2: typing.Optional[AnOtherMessage] = Field(default_factory=AnOtherMessage)
