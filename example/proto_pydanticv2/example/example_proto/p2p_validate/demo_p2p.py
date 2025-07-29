# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing
from datetime import datetime, timedelta
from enum import IntEnum
from ipaddress import IPv4Address, IPv6Address
from typing import Annotated, Literal, Optional, Union
from uuid import UUID, uuid4

import typing_extensions
from annotated_types import Ge, Gt, Interval, Le, Lt, MaxLen, MinLen
from google.protobuf.any_pb2 import Any  # type: ignore
from google.protobuf.message import Message  # type: ignore
from pydantic import ConfigDict, Field, field_validator
from pydantic.networks import AnyUrl, EmailStr, IPvAnyAddress
from pydantic.types import StringConstraints

from example.plugin_config import CustomerField, customer_any
from protobuf_to_pydantic.customer_con_type.v2 import DatetimeType, TimedeltaType, gt_now, t_gt, t_lt
from protobuf_to_pydantic.customer_validator.v2 import (
    any_in_validator,
    any_not_in_validator,
    contains_validator,
    duration_const_validator,
    duration_ge_validator,
    duration_gt_validator,
    duration_in_validator,
    duration_le_validator,
    duration_lt_validator,
    duration_not_in_validator,
    in_validator,
    len_validator,
    map_max_pairs_validator,
    map_min_pairs_validator,
    not_contains_validator,
    not_in_validator,
    prefix_validator,
    suffix_validator,
    timestamp_const_validator,
    timestamp_ge_validator,
    timestamp_gt_now_validator,
    timestamp_gt_validator,
    timestamp_le_validator,
    timestamp_lt_now_validator,
    timestamp_lt_validator,
    timestamp_within_validator,
)
from protobuf_to_pydantic.default_base_model import ProtobufCompatibleBaseModel
from protobuf_to_pydantic.field_info_rule.protobuf_option_to_field_info.types import HostNameStr, UriRefStr
from protobuf_to_pydantic.flexible_enum_mixin import FlexibleEnumMixin
from protobuf_to_pydantic.util import DurationType, TimestampType, datetime_utc_now


class State(IntEnum, FlexibleEnumMixin):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class FloatTest(ProtobufCompatibleBaseModel):
    const_test: typing.Literal[1.0] = Field(default=0.0)
    range_e_test: float = Field(default=0.0, ge=1.0, le=10.0)
    range_test: float = Field(default=0.0, gt=1.0, lt=10.0)
    in_test: float = Field(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = Field(default=0.0, not_in=[1.0, 2.0, 3.0])
    default_test: float = Field(default=1.0)
    default_template_test: float = Field(default=1600000000)
    default_factory_test: float = Field(default_factory=float)
    required_test: float = Field()
    alias_test: float = Field(default=0.0, alias="alias")
    desc_test: float = Field(default=0.0, description="test desc")
    multiple_of_test: float = Field(default=0.0, multiple_of=3)
    example_test: float = Field(default=0.0, example=1.0)
    example_factory: float = Field(default=0.0, example=float)
    field_test: float = CustomerField(default=0.0)
    type_test: typing_extensions.Annotated[float, None, Interval(), None, None] = Field(default=0.0)
    title_test: float = Field(default=0.0, title="title_test")
    extra_test: float = Field(default=0.0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class DoubleTest(ProtobufCompatibleBaseModel):
    const_test: typing.Literal[1.0] = Field(default=0.0)
    range_e_test: float = Field(default=0.0, ge=1.0, le=10.0)
    range_test: float = Field(default=0.0, gt=1.0, lt=10.0)
    in_test: float = Field(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = Field(default=0.0, not_in=[1.0, 2.0, 3.0])
    default_test: float = Field(default=1.0)
    default_template_test: float = Field(default=1600000000)
    default_factory_test: float = Field(default_factory=float)
    required_test: float = Field()
    alias_test: float = Field(default=0.0, alias="alias")
    desc_test: float = Field(default=0.0, description="test desc")
    multiple_of_test: float = Field(default=0.0, multiple_of=3)
    example_test: float = Field(default=0.0, example=1.0)
    example_factory: float = Field(default=0.0, example=float)
    field_test: float = CustomerField(default=0.0)
    type_test: typing_extensions.Annotated[float, None, Interval(), None, None] = Field(default=0.0)
    title_test: float = Field(default=0.0, title="title_test")
    extra_test: float = Field(default=0.0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Int32Test(ProtobufCompatibleBaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_template_test: int = Field(default=1600000000)
    default_factory_test: int = Field(default_factory=int)
    required_test: int = Field()
    alias_test: int = Field(default=0, alias="alias")
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: typing_extensions.Annotated[float, None, Interval(), None, None] = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Int64Test(ProtobufCompatibleBaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_template_test: int = Field(default=1600000000)
    default_factory_test: int = Field(default_factory=int)
    required_test: int = Field()
    alias_test: int = Field(default=0, alias="alias")
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: typing_extensions.Annotated[float, None, Interval(), None, None] = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Uint32Test(ProtobufCompatibleBaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_template_test: int = Field(default=1600000000)
    default_factory_test: int = Field(default_factory=int)
    required_test: int = Field()
    alias_test: int = Field(default=0, alias="alias")
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: typing_extensions.Annotated[int, None, Interval(), None] = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Sint32Test(ProtobufCompatibleBaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_template_test: int = Field(default=1600000000)
    default_factory_test: int = Field(default_factory=int)
    required_test: int = Field()
    alias_test: int = Field(default=0, alias="alias")
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: typing_extensions.Annotated[int, None, Interval(), None] = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Uint64Test(ProtobufCompatibleBaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_template_test: int = Field(default=1600000000)
    default_factory_test: int = Field(default_factory=int)
    required_test: int = Field()
    alias_test: int = Field(default=0, alias="alias")
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: typing_extensions.Annotated[int, None, Interval(), None] = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Sint64Test(ProtobufCompatibleBaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_template_test: int = Field(default=1600000000)
    default_factory_test: int = Field(default_factory=int)
    required_test: int = Field()
    alias_test: int = Field(default=0, alias="alias")
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: typing_extensions.Annotated[int, None, Interval(), None] = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Fixed32Test(ProtobufCompatibleBaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_template_test: int = Field(default=1600000000)
    default_factory_test: int = Field(default_factory=float)
    required_test: int = Field()
    alias_test: int = Field(default=0, alias="alias")
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=float)
    field_test: int = CustomerField(default=0)
    type_test: typing_extensions.Annotated[float, None, Interval(), None, None] = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Fixed64Test(ProtobufCompatibleBaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_template_test: int = Field(default=1600000000)
    default_factory_test: int = Field(default_factory=float)
    required_test: int = Field()
    alias_test: int = Field(default=0, alias="alias")
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=float)
    field_test: int = CustomerField(default=0)
    type_test: typing_extensions.Annotated[float, None, Interval(), None, None] = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Sfixed32Test(ProtobufCompatibleBaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_template_test: int = Field(default=1600000000)
    default_factory_test: int = Field(default_factory=float)
    required_test: int = Field()
    alias_test: int = Field(default=0, alias="alias")
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=float)
    field_test: int = CustomerField(default=0)
    type_test: typing_extensions.Annotated[float, None, Interval(), None, None] = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Sfixed64Test(ProtobufCompatibleBaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_template_test: int = Field(default=1600000000)
    default_factory_test: int = Field(default_factory=float)
    required_test: int = Field()
    alias_test: int = Field(default=0, alias="alias")
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=float)
    field_test: int = CustomerField(default=0)
    type_test: typing_extensions.Annotated[float, None, Interval(), None, None] = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class BoolTest(ProtobufCompatibleBaseModel):
    bool_1_test: typing.Literal[True] = Field(default=False)
    bool_2_test: typing.Literal[False] = Field(default=False)
    default_test: bool = Field(default=True)
    required_test: bool = Field()
    alias_test: bool = Field(default=False, alias="alias")
    desc_test: bool = Field(default=False, description="test desc")
    example_test: bool = Field(default=False, example=True)
    field_test: bool = CustomerField(default=False)
    title_test: bool = Field(default=False, title="title_test")
    extra_test: bool = Field(default=False, customer_string="c1", customer_int=1)


class StringTest(ProtobufCompatibleBaseModel):
    const_test: typing.Literal["aaa"] = Field(default="")
    len_test: str = Field(default="", len=3)
    s_range_len_test: str = Field(default="", min_length=1, max_length=3)
    pattern_test: str = Field(default="", pattern="^test")
    prefix_test: str = Field(default="", prefix="prefix")
    suffix_test: str = Field(default="", suffix="suffix")
    contains_test: str = Field(default="", contains="contains")
    not_contains_test: str = Field(default="", not_contains="not_contains")
    in_test: str = Field(default="", in_=["a", "b", "c"])
    not_in_test: str = Field(default="", not_in=["a", "b", "c"])
    email_test: EmailStr = Field(default="")
    hostname_test: HostNameStr = Field(default="")
    ip_test: IPvAnyAddress = Field(default="")
    ipv4_test: IPv4Address = Field(default="")
    ipv6_test: IPv6Address = Field(default="")
    uri_test: AnyUrl = Field(default="")
    uri_ref_test: UriRefStr = Field(default="")
    address_test: IPvAnyAddress = Field(default="")
    uuid_test: UUID = Field(default="")
    pydantic_type_test: str = Field(default="")
    default_test: str = Field(default="default")
    default_factory_test: str = Field(default_factory=uuid4)
    required_test: str = Field()
    alias_test: str = Field(default="", alias="alias")
    desc_test: str = Field(default="", description="test desc")
    example_test: str = Field(default="", example="example")
    example_factory_test: str = Field(default="", example=uuid4)
    field_test: str = CustomerField(default="")
    title_test: str = Field(default="", title="title_test")
    type_test: typing_extensions.Annotated[str, StringConstraints()] = Field(default="")
    extra_test: str = Field(default="", customer_string="c1", customer_int=1)

    len_test_len_validator = field_validator("len_test", mode="after", check_fields=None)(len_validator)
    prefix_test_prefix_validator = field_validator("prefix_test", mode="after", check_fields=None)(prefix_validator)
    suffix_test_suffix_validator = field_validator("suffix_test", mode="after", check_fields=None)(suffix_validator)
    contains_test_contains_validator = field_validator("contains_test", mode="after", check_fields=None)(
        contains_validator
    )
    not_contains_test_not_contains_validator = field_validator("not_contains_test", mode="after", check_fields=None)(
        not_contains_validator
    )
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class BytesTest(ProtobufCompatibleBaseModel):
    const_test: typing.Literal[b"demo"] = Field(default=b"")
    range_len_test: bytes = Field(default=b"", min_length=1, max_length=4)
    prefix_test: bytes = Field(default=b"", prefix=b"prefix")
    suffix_test: bytes = Field(default=b"", suffix=b"suffix")
    contains_test: bytes = Field(default=b"", contains=b"contains")
    in_test: bytes = Field(default=b"", in_=[b"a", b"b", b"c"])
    not_in_test: bytes = Field(default=b"", not_in=[b"a", b"b", b"c"])
    default_test: bytes = Field(default=b"default")
    default_factory_test: bytes = Field(default_factory=bytes)
    required_test: bytes = Field()
    alias_test: bytes = Field(default=b"", alias="alias")
    desc_test: bytes = Field(default=b"", description="test desc")
    example_test: bytes = Field(default=b"", example=b"example")
    example_factory_test: bytes = Field(default=b"", example=bytes)
    field_test: bytes = CustomerField(default=b"")
    title_test: bytes = Field(default=b"", title="title_test")
    type_test: typing_extensions.Annotated[str, StringConstraints()] = Field(default=b"")
    extra_test: bytes = Field(default=b"", customer_string="c1", customer_int=1)

    prefix_test_prefix_validator = field_validator("prefix_test", mode="after", check_fields=None)(prefix_validator)
    suffix_test_suffix_validator = field_validator("suffix_test", mode="after", check_fields=None)(suffix_validator)
    contains_test_contains_validator = field_validator("contains_test", mode="after", check_fields=None)(
        contains_validator
    )
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class EnumTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(validate_default=True)
    const_test: typing.Literal[2] = Field(default=0)
    in_test: State = Field(default=0, in_=[0, 2])
    not_in_test: State = Field(default=0, not_in=[0, 2])
    default_test: State = Field(default=1)
    required_test: State = Field()
    alias_test: State = Field(default=0, alias="alias")
    desc_test: State = Field(default=0, description="test desc")
    example_test: State = Field(default=0, example=2)
    field_test: State = CustomerField(default=0)
    title_test: State = Field(default=0, title="title_test")
    extra_test: State = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class MapTest(ProtobufCompatibleBaseModel):
    pair_test: "typing.Dict[str, int]" = Field(default_factory=dict, map_min_pairs=1, map_max_pairs=5)
    keys_test: typing.Dict[typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)], int] = Field(
        default_factory=dict
    )
    values_test: typing.Dict[str, typing_extensions.Annotated[int, Ge(ge=5), Le(le=5)]] = Field(default_factory=dict)
    keys_values_test: typing.Dict[
        typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)],
        typing_extensions.Annotated[DatetimeType, gt_now(True)],
    ] = Field(default_factory=dict)
    default_factory_test: "typing.Dict[str, int]" = Field(default_factory=dict)
    required_test: "typing.Dict[str, int]" = Field()
    alias_test: "typing.Dict[str, int]" = Field(default_factory=dict, alias="alias")
    desc_test: "typing.Dict[str, int]" = Field(default_factory=dict, description="test desc")
    example_factory_test: "typing.Dict[str, int]" = Field(default_factory=dict, example=dict)
    field_test: "typing.Dict[str, int]" = CustomerField(default_factory=dict)
    title_test: "typing.Dict[str, int]" = Field(default_factory=dict, title="title_test")
    type_test: dict = Field(default_factory=dict)
    extra_test: "typing.Dict[str, int]" = Field(default_factory=dict, customer_string="c1", customer_int=1)

    pair_test_map_min_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_min_pairs_validator
    )
    pair_test_map_max_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_max_pairs_validator
    )


class MessageTest(ProtobufCompatibleBaseModel):
    skip_test: str = Field(default="")
    required_test: str = Field()
    extra_test: str = Field(default="", customer_string="c1", customer_int=1)


class RepeatedTest(ProtobufCompatibleBaseModel):
    range_test: typing.List[str] = Field(default_factory=list, min_length=1, max_length=5)
    unique_test: typing.Set[str] = Field(default_factory=set)
    items_string_test: typing.List[typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)]] = (
        Field(default_factory=list, min_length=1, max_length=5)
    )
    items_double_test: typing.List[typing_extensions.Annotated[float, Gt(gt=1.0), Lt(lt=5.0)]] = Field(
        default_factory=list, min_length=1, max_length=5
    )
    items_int32_test: typing.List[typing_extensions.Annotated[int, Gt(gt=1), Lt(lt=5)]] = Field(
        default_factory=list, min_length=1, max_length=5
    )
    items_timestamp_test: typing.List[
        typing_extensions.Annotated[DatetimeType, t_gt(1600000000.0), t_lt(1600000010.0)]
    ] = Field(default_factory=list, min_length=1, max_length=5)
    items_duration_test: typing.List[
        typing_extensions.Annotated[TimedeltaType, Ge(ge=timedelta(seconds=10)), Le(le=timedelta(seconds=10))]
    ] = Field(default_factory=list, min_length=1, max_length=5)
    items_bytes_test: typing.List[typing_extensions.Annotated[bytes, MinLen(min_length=1), MaxLen(max_length=5)]] = (
        Field(default_factory=list, min_length=1, max_length=5)
    )
    default_factory_test: typing.List[str] = Field(default_factory=list)
    required_test: typing.List[str] = Field()
    alias_test: typing.List[str] = Field(default_factory=list, alias="alias")
    desc_test: typing.List[str] = Field(default_factory=list, description="test desc")
    example_factory_test: typing.List[str] = Field(default_factory=list, example=list)
    field_test: typing.List[str] = CustomerField(default_factory=list)
    title_test: typing.List[str] = Field(default_factory=list, title="title_test")
    type_test: list = Field(default_factory=list)
    extra_test: typing.List[str] = Field(default_factory=list, customer_string="c1", customer_int=1)


class AnyTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    required_test: Any = Field()
    not_in_test: Any = Field(
        default_factory=Any,
        any_not_in=["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"],
    )
    in_test: Any = Field(
        default_factory=Any,
        any_in=[
            Any(type_url="type.googleapis.com/google.protobuf.Duration"),
            "type.googleapis.com/google.protobuf.Timestamp",
        ],
    )
    default_test: Any = Field(default=Any(type_url="type.googleapis.com/google.protobuf.Duration"))
    default_factory_test: Any = Field(default_factory=customer_any)
    alias_test: Any = Field(default_factory=Any, alias="alias")
    desc_test: Any = Field(default_factory=Any, description="test desc")
    example_test: Any = Field(default_factory=Any, example="type.googleapis.com/google.protobuf.Duration")
    example_factory_test: Any = Field(default_factory=Any, example=customer_any)
    field_test: Any = CustomerField(default_factory=Any)
    title_test: Any = Field(default_factory=Any, title="title_test")
    extra_test: Any = Field(default_factory=Any, customer_string="c1", customer_int=1)

    not_in_test_any_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(
        any_not_in_validator
    )
    in_test_any_in_validator = field_validator("in_test", mode="after", check_fields=None)(any_in_validator)


class DurationTest(ProtobufCompatibleBaseModel):
    const_test: DurationType = Field(
        default_factory=timedelta, duration_const=timedelta(seconds=1, microseconds=500000)
    )
    range_test: DurationType = Field(
        default_factory=timedelta,
        duration_lt=timedelta(seconds=10, microseconds=500000),
        duration_gt=timedelta(seconds=5, microseconds=500000),
    )
    range_e_test: DurationType = Field(
        default_factory=timedelta,
        duration_le=timedelta(seconds=10, microseconds=500000),
        duration_ge=timedelta(seconds=5, microseconds=500000),
    )
    in_test: DurationType = Field(
        default_factory=timedelta,
        duration_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )
    not_in_test: DurationType = Field(
        default_factory=timedelta,
        duration_not_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )
    default_test: DurationType = Field(default=timedelta(seconds=1, microseconds=500000))
    default_factory_test: DurationType = Field(default_factory=timedelta)
    required_test: DurationType = Field()
    alias_test: DurationType = Field(default_factory=timedelta, alias="alias")
    desc_test: DurationType = Field(default_factory=timedelta, description="test desc")
    example_test: DurationType = Field(default_factory=timedelta, example=timedelta(seconds=1, microseconds=500000))
    example_factory_test: DurationType = Field(default_factory=timedelta, example=timedelta)
    field_test: DurationType = CustomerField(default_factory=timedelta)
    title_test: DurationType = Field(default_factory=timedelta, title="title_test")
    type_test: timedelta = Field(default_factory=timedelta)
    extra_test: DurationType = Field(default_factory=timedelta, customer_string="c1", customer_int=1)

    const_test_duration_const_validator = field_validator("const_test", mode="after", check_fields=None)(
        duration_const_validator
    )
    range_test_duration_lt_validator = field_validator("range_test", mode="after", check_fields=None)(
        duration_lt_validator
    )
    range_test_duration_gt_validator = field_validator("range_test", mode="after", check_fields=None)(
        duration_gt_validator
    )
    range_e_test_duration_le_validator = field_validator("range_e_test", mode="after", check_fields=None)(
        duration_le_validator
    )
    range_e_test_duration_ge_validator = field_validator("range_e_test", mode="after", check_fields=None)(
        duration_ge_validator
    )
    in_test_duration_in_validator = field_validator("in_test", mode="after", check_fields=None)(duration_in_validator)
    not_in_test_duration_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(
        duration_not_in_validator
    )


class TimestampTest(ProtobufCompatibleBaseModel):
    const_test: TimestampType = Field(default_factory=datetime_utc_now, timestamp_const=1600000000.0)
    range_test: TimestampType = Field(
        default_factory=datetime_utc_now, timestamp_lt=1600000010.0, timestamp_gt=1600000000.0
    )
    range_e_test: TimestampType = Field(
        default_factory=datetime_utc_now, timestamp_le=1600000010.0, timestamp_ge=1600000000.0
    )
    lt_now_test: TimestampType = Field(default_factory=datetime_utc_now, timestamp_lt_now=True)
    gt_now_test: TimestampType = Field(default_factory=datetime_utc_now, timestamp_gt_now=True)
    within_test: TimestampType = Field(default_factory=datetime_utc_now, timestamp_within=timedelta(seconds=1))
    within_and_gt_now_test: TimestampType = Field(
        default_factory=datetime_utc_now, timestamp_gt_now=True, timestamp_within=timedelta(seconds=3600)
    )
    default_test: TimestampType = Field(default=1.5)
    default_factory_test: TimestampType = Field(default_factory=datetime.now)
    required_test: TimestampType = Field()
    alias_test: TimestampType = Field(default_factory=datetime_utc_now, alias="alias")
    desc_test: TimestampType = Field(default_factory=datetime_utc_now, description="test desc")
    example_test: TimestampType = Field(default_factory=datetime_utc_now, example=1.5)
    example_factory_test: TimestampType = Field(default_factory=datetime_utc_now, example=datetime.now)
    field_test: TimestampType = CustomerField(default_factory=datetime_utc_now)
    title_test: TimestampType = Field(default_factory=datetime_utc_now, title="title_test")
    type_test: datetime = Field(default_factory=datetime_utc_now)
    extra_test: TimestampType = Field(default_factory=datetime_utc_now, customer_string="c1", customer_int=1)

    const_test_timestamp_const_validator = field_validator("const_test", mode="after", check_fields=None)(
        timestamp_const_validator
    )
    range_test_timestamp_lt_validator = field_validator("range_test", mode="after", check_fields=None)(
        timestamp_lt_validator
    )
    range_test_timestamp_gt_validator = field_validator("range_test", mode="after", check_fields=None)(
        timestamp_gt_validator
    )
    range_e_test_timestamp_le_validator = field_validator("range_e_test", mode="after", check_fields=None)(
        timestamp_le_validator
    )
    range_e_test_timestamp_ge_validator = field_validator("range_e_test", mode="after", check_fields=None)(
        timestamp_ge_validator
    )
    lt_now_test_timestamp_lt_now_validator = field_validator("lt_now_test", mode="after", check_fields=None)(
        timestamp_lt_now_validator
    )
    gt_now_test_timestamp_gt_now_validator = field_validator("gt_now_test", mode="after", check_fields=None)(
        timestamp_gt_now_validator
    )
    within_test_timestamp_within_validator = field_validator("within_test", mode="after", check_fields=None)(
        timestamp_within_validator
    )
    within_and_gt_now_test_timestamp_gt_now_validator = field_validator(
        "within_and_gt_now_test", mode="after", check_fields=None
    )(timestamp_gt_now_validator)
    within_and_gt_now_test_timestamp_within_validator = field_validator(
        "within_and_gt_now_test", mode="after", check_fields=None
    )(timestamp_within_validator)


class MessageIgnoredTest(ProtobufCompatibleBaseModel):
    const_test: int = Field(default=0)
    range_e_test: int = Field(default=0)
    range_test: int = Field(default=0)


class OneOfTestIdX(ProtobufCompatibleBaseModel):
    """Variant when 'x' is set in id oneof."""

    id_case: Literal["x"] = Field(default="x", exclude=True)
    x: str


class OneOfTestIdY(ProtobufCompatibleBaseModel):
    """Variant when 'y' is set in id oneof."""

    id_case: Literal["y"] = Field(default="y", exclude=True)
    y: int


OneOfTestIdUnion = Annotated[Union[OneOfTestIdX, OneOfTestIdY], Field(discriminator="id_case")]


class OneOfTest(ProtobufCompatibleBaseModel):
    id: OneOfTestIdUnion

    _oneof_fields = {"id": {"aliases": {"x": "x", "y": "y"}, "fields": ["x", "y"]}}

    header: str = Field(default="")


class OneOfNotTestIdX(ProtobufCompatibleBaseModel):
    """Variant when 'x' is set in id oneof."""

    id_case: Literal["x"] = Field(default="x", exclude=True)
    x: str


class OneOfNotTestIdY(ProtobufCompatibleBaseModel):
    """Variant when 'y' is set in id oneof."""

    id_case: Literal["y"] = Field(default="y", exclude=True)
    y: int


class OneOfNotTestIdNone(ProtobufCompatibleBaseModel):
    """Variant when no field is set in id oneof."""

    id_case: Literal[None] = None


OneOfNotTestIdUnion = Annotated[
    Union[OneOfNotTestIdX, OneOfNotTestIdY, OneOfNotTestIdNone], Field(discriminator="id_case")
]


class OneOfNotTest(ProtobufCompatibleBaseModel):
    id: Optional[OneOfNotTestIdUnion] = Field(default=None)

    _oneof_fields = {"id": {"aliases": {"x": "x", "y": "y"}, "fields": ["x", "y"]}}

    header: str = Field(default="")


class OneOfOptionalTestIdX(ProtobufCompatibleBaseModel):
    """Variant when 'x' is set in id oneof."""

    id_case: Literal["x"] = Field(default="x", exclude=True)
    x: str


class OneOfOptionalTestIdY(ProtobufCompatibleBaseModel):
    """Variant when 'y' is set in id oneof."""

    id_case: Literal["y"] = Field(default="y", exclude=True)
    y: int


class OneOfOptionalTestIdZ(ProtobufCompatibleBaseModel):
    """Variant when 'z' is set in id oneof."""

    id_case: Literal["z"] = Field(default="z", exclude=True)
    z: bool


OneOfOptionalTestIdUnion = Annotated[
    Union[OneOfOptionalTestIdX, OneOfOptionalTestIdY, OneOfOptionalTestIdZ], Field(discriminator="id_case")
]


class OneOfOptionalTest(ProtobufCompatibleBaseModel):
    id: OneOfOptionalTestIdUnion

    _oneof_fields = {"id": {"aliases": {"x": "x", "y": "y", "z": "z"}, "fields": ["x", "y", "z"]}}

    header: str = Field(default="")
    name: typing.Optional[str] = Field(default=None)
    age: typing.Optional[int] = Field(default=None)
    str_list: typing.List[str] = Field(default_factory=list)
    int_map: "typing.Dict[str, int]" = Field(default_factory=dict)


class AfterReferMessage(ProtobufCompatibleBaseModel):
    uid: str = Field(default="", title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", ge=0, example=18.0)


class NestedMessage(ProtobufCompatibleBaseModel):
    """
    test nested message
    """

    class UserPayMessage(ProtobufCompatibleBaseModel):
        bank_number: str = Field(default="", min_length=13, max_length=19)
        exp: TimestampType = Field(default_factory=datetime_utc_now, timestamp_gt_now=True)
        uuid: UUID = Field(default="")

        exp_timestamp_gt_now_validator = field_validator("exp", mode="after", check_fields=None)(
            timestamp_gt_now_validator
        )

    class NotEnableUserPayMessage(ProtobufCompatibleBaseModel):
        bank_number: str = Field(default="")
        exp: TimestampType = Field(default_factory=datetime_utc_now)
        uuid: str = Field(default="")

    string_in_map_test: "typing.Dict[str, StringTest]" = Field(default_factory=dict)
    map_in_map_test: "typing.Dict[str, MapTest]" = Field(default_factory=dict)
    user_pay: "NestedMessage.UserPayMessage" = Field(default_factory=lambda: NestedMessage.UserPayMessage())
    not_enable_user_pay: "NestedMessage.NotEnableUserPayMessage" = Field(
        default_factory=lambda: NestedMessage.NotEnableUserPayMessage()
    )
    empty: None = Field()
    after_refer: AfterReferMessage = Field(default_factory=AfterReferMessage)


class OptionalMessage(ProtobufCompatibleBaseModel):
    # fix https://github.com/so1n/protobuf_to_pydantic/issues/82
    my_message1: typing.Optional[MessageIgnoredTest] = Field()
    # fix https://github.com/so1n/protobuf_to_pydantic/issues/85
    my_message2: typing.Optional[MessageIgnoredTest] = Field(default=None)
    my_message3: MessageIgnoredTest = Field()
    my_message4: MessageIgnoredTest = Field(default_factory=MessageIgnoredTest)
    my_message_5: typing.Optional[MessageIgnoredTest] = Field(default=None)
