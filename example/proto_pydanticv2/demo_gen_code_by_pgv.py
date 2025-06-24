# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing
from datetime import datetime, timedelta
from enum import IntEnum
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID

import typing_extensions
from annotated_types import Ge, Gt, Le, Lt, MaxLen, MinLen
from google.protobuf.any_pb2 import Any  # type: ignore
from protobuf_to_pydantic.customer_con_type.v2 import DatetimeType, TimedeltaType, gt_now, t_gt, t_lt
from protobuf_to_pydantic.customer_validator.v2 import (
    any_in_validator,
    any_not_in_validator,
    check_one_of,
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
from protobuf_to_pydantic.util import Timedelta, datetime_utc_now, duration_serializer, timestamp_serializer
from pydantic import ConfigDict, Field, field_validator, model_validator
from pydantic.alias_generators import to_camel
from pydantic.aliases import AliasGenerator
from pydantic.functional_serializers import PlainSerializer
from pydantic.functional_validators import BeforeValidator
from pydantic.networks import AnyUrl, EmailStr, IPvAnyAddress


class AfterReferMessage(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    uid: str = Field(default="", alias_priority=1, validation_alias="uid", serialization_alias="uid", min_length=1)
    age: int = Field(default=0, alias_priority=1, validation_alias="age", serialization_alias="age", ge=0, lt=500)


class AnyTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        arbitrary_types_allowed=True,
        serialize_by_alias=True,
    )

    required_test: Any = Field(alias_priority=1, validation_alias="requiredTest", serialization_alias="requiredTest")
    not_in_test: Any = Field(
        default_factory=Any,
        alias_priority=1,
        validation_alias="notInTest",
        serialization_alias="notInTest",
        any_not_in=["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"],
    )
    in_test: Any = Field(
        default_factory=Any,
        alias_priority=1,
        validation_alias="inTest",
        serialization_alias="inTest",
        any_in=["type.googleapis.com/google.protobuf.Duration", "type.googleapis.com/google.protobuf.Timestamp"],
    )

    not_in_test_any_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(
        any_not_in_validator
    )
    in_test_any_in_validator = field_validator("in_test", mode="after", check_fields=None)(any_in_validator)


class BoolTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    bool_1_test: typing.Literal[True] = Field(
        default=False, alias_priority=1, validation_alias="bool1Test", serialization_alias="bool1Test"
    )
    bool_2_test: typing.Literal[False] = Field(
        default=False, alias_priority=1, validation_alias="bool2Test", serialization_alias="bool2Test"
    )


class BytesTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: typing.Literal[b"demo"] = Field(
        default=b"", alias_priority=1, validation_alias="constTest", serialization_alias="constTest"
    )
    len_test: bytes = Field(
        default=b"", alias_priority=1, validation_alias="lenTest", serialization_alias="lenTest", len=4
    )
    range_len_test: bytes = Field(
        default=b"",
        alias_priority=1,
        validation_alias="rangeLenTest",
        serialization_alias="rangeLenTest",
        min_length=1,
        max_length=4,
    )
    pattern_test: bytes = Field(
        default=b"", alias_priority=1, validation_alias="patternTest", serialization_alias="patternTest"
    )
    prefix_test: bytes = Field(
        default=b"", alias_priority=1, validation_alias="prefixTest", serialization_alias="prefixTest", prefix=b"prefix"
    )
    suffix_test: bytes = Field(
        default=b"", alias_priority=1, validation_alias="suffixTest", serialization_alias="suffixTest", suffix=b"suffix"
    )
    contains_test: bytes = Field(
        default=b"",
        alias_priority=1,
        validation_alias="containsTest",
        serialization_alias="containsTest",
        contains=b"contains",
    )
    in_test: bytes = Field(
        default=b"", alias_priority=1, validation_alias="inTest", serialization_alias="inTest", in_=[b"a", b"b", b"c"]
    )
    not_in_test: bytes = Field(
        default=b"",
        alias_priority=1,
        validation_alias="notInTest",
        serialization_alias="notInTest",
        not_in=[b"a", b"b", b"c"],
    )

    len_test_len_validator = field_validator("len_test", mode="after", check_fields=None)(len_validator)
    prefix_test_prefix_validator = field_validator("prefix_test", mode="after", check_fields=None)(prefix_validator)
    suffix_test_suffix_validator = field_validator("suffix_test", mode="after", check_fields=None)(suffix_validator)
    contains_test_contains_validator = field_validator("contains_test", mode="after", check_fields=None)(
        contains_validator
    )
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class DoubleTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: typing.Literal[1.0] = Field(
        default=0.0, alias_priority=1, validation_alias="constTest", serialization_alias="constTest"
    )
    range_e_test: float = Field(
        default=0.0, alias_priority=1, validation_alias="rangeETest", serialization_alias="rangeETest", ge=1.0, le=10.0
    )
    range_test: float = Field(
        default=0.0, alias_priority=1, validation_alias="rangeTest", serialization_alias="rangeTest", gt=1.0, lt=10.0
    )
    in_test: float = Field(
        default=0.0, alias_priority=1, validation_alias="inTest", serialization_alias="inTest", in_=[1.0, 2.0, 3.0]
    )
    not_in_test: float = Field(
        default=0.0,
        alias_priority=1,
        validation_alias="notInTest",
        serialization_alias="notInTest",
        not_in=[1.0, 2.0, 3.0],
    )
    ignore_test: float = Field(
        default=0.0, alias_priority=1, validation_alias="ignoreTest", serialization_alias="ignoreTest"
    )

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class DurationTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    required_test: typing_extensions.Annotated[
        timedelta,
        BeforeValidator(func=Timedelta.validate),
        PlainSerializer(func=duration_serializer, return_type=str, when_used="json"),
    ] = Field(alias_priority=1, validation_alias="requiredTest", serialization_alias="requiredTest")
    const_test: typing_extensions.Annotated[
        timedelta,
        BeforeValidator(func=Timedelta.validate),
        PlainSerializer(func=duration_serializer, return_type=str, when_used="json"),
    ] = Field(
        default_factory=Timedelta,
        alias_priority=1,
        validation_alias="constTest",
        serialization_alias="constTest",
        duration_const=timedelta(seconds=1, microseconds=500000),
    )
    range_test: typing_extensions.Annotated[
        timedelta,
        BeforeValidator(func=Timedelta.validate),
        PlainSerializer(func=duration_serializer, return_type=str, when_used="json"),
    ] = Field(
        default_factory=Timedelta,
        alias_priority=1,
        validation_alias="rangeTest",
        serialization_alias="rangeTest",
        duration_lt=timedelta(seconds=10, microseconds=500000),
        duration_gt=timedelta(seconds=5, microseconds=500000),
    )
    range_e_test: typing_extensions.Annotated[
        timedelta,
        BeforeValidator(func=Timedelta.validate),
        PlainSerializer(func=duration_serializer, return_type=str, when_used="json"),
    ] = Field(
        default_factory=Timedelta,
        alias_priority=1,
        validation_alias="rangeETest",
        serialization_alias="rangeETest",
        duration_le=timedelta(seconds=10, microseconds=500000),
        duration_ge=timedelta(seconds=5, microseconds=500000),
    )
    in_test: typing_extensions.Annotated[
        timedelta,
        BeforeValidator(func=Timedelta.validate),
        PlainSerializer(func=duration_serializer, return_type=str, when_used="json"),
    ] = Field(
        default_factory=Timedelta,
        alias_priority=1,
        validation_alias="inTest",
        serialization_alias="inTest",
        duration_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )
    not_in_test: typing_extensions.Annotated[
        timedelta,
        BeforeValidator(func=Timedelta.validate),
        PlainSerializer(func=duration_serializer, return_type=str, when_used="json"),
    ] = Field(
        default_factory=Timedelta,
        alias_priority=1,
        validation_alias="notInTest",
        serialization_alias="notInTest",
        duration_not_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )

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


class State(IntEnum):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class EnumTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        validate_default=True,
        serialize_by_alias=True,
    )

    const_test: typing.Literal[2] = Field(
        default=0, alias_priority=1, validation_alias="constTest", serialization_alias="constTest"
    )
    defined_only_test: State = Field(
        default=0, alias_priority=1, validation_alias="definedOnlyTest", serialization_alias="definedOnlyTest"
    )
    in_test: State = Field(
        default=0, alias_priority=1, validation_alias="inTest", serialization_alias="inTest", in_=[0, 2]
    )
    not_in_test: State = Field(
        default=0, alias_priority=1, validation_alias="notInTest", serialization_alias="notInTest", not_in=[0, 2]
    )

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Fixed32Test(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: typing.Literal[1] = Field(
        default=0, alias_priority=1, validation_alias="constTest", serialization_alias="constTest"
    )
    range_e_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeETest", serialization_alias="rangeETest", ge=1, le=10
    )
    range_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeTest", serialization_alias="rangeTest", gt=1, lt=10
    )
    in_test: int = Field(
        default=0, alias_priority=1, validation_alias="inTest", serialization_alias="inTest", in_=[1, 2, 3]
    )
    not_in_test: int = Field(
        default=0, alias_priority=1, validation_alias="notInTest", serialization_alias="notInTest", not_in=[1, 2, 3]
    )
    ignore_test: int = Field(
        default=0, alias_priority=1, validation_alias="ignoreTest", serialization_alias="ignoreTest"
    )

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Fixed64Test(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: typing.Literal[1] = Field(
        default=0, alias_priority=1, validation_alias="constTest", serialization_alias="constTest"
    )
    range_e_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeETest", serialization_alias="rangeETest", ge=1, le=10
    )
    range_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeTest", serialization_alias="rangeTest", gt=1, lt=10
    )
    in_test: int = Field(
        default=0, alias_priority=1, validation_alias="inTest", serialization_alias="inTest", in_=[1, 2, 3]
    )
    not_in_test: int = Field(
        default=0, alias_priority=1, validation_alias="notInTest", serialization_alias="notInTest", not_in=[1, 2, 3]
    )
    ignore_test: int = Field(
        default=0, alias_priority=1, validation_alias="ignoreTest", serialization_alias="ignoreTest"
    )

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class FloatTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: typing.Literal[1.0] = Field(
        default=0.0, alias_priority=1, validation_alias="constTest", serialization_alias="constTest"
    )
    range_e_test: float = Field(
        default=0.0, alias_priority=1, validation_alias="rangeETest", serialization_alias="rangeETest", ge=1.0, le=10.0
    )
    range_test: float = Field(
        default=0.0, alias_priority=1, validation_alias="rangeTest", serialization_alias="rangeTest", gt=1.0, lt=10.0
    )
    in_test: float = Field(
        default=0.0, alias_priority=1, validation_alias="inTest", serialization_alias="inTest", in_=[1.0, 2.0, 3.0]
    )
    not_in_test: float = Field(
        default=0.0,
        alias_priority=1,
        validation_alias="notInTest",
        serialization_alias="notInTest",
        not_in=[1.0, 2.0, 3.0],
    )
    ignore_test: float = Field(
        default=0.0, alias_priority=1, validation_alias="ignoreTest", serialization_alias="ignoreTest"
    )

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Int32Test(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: typing.Literal[1] = Field(
        default=0, alias_priority=1, validation_alias="constTest", serialization_alias="constTest"
    )
    range_e_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeETest", serialization_alias="rangeETest", ge=1, le=10
    )
    range_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeTest", serialization_alias="rangeTest", gt=1, lt=10
    )
    in_test: int = Field(
        default=0, alias_priority=1, validation_alias="inTest", serialization_alias="inTest", in_=[1, 2, 3]
    )
    not_in_test: int = Field(
        default=0, alias_priority=1, validation_alias="notInTest", serialization_alias="notInTest", not_in=[1, 2, 3]
    )
    ignore_test: int = Field(
        default=0, alias_priority=1, validation_alias="ignoreTest", serialization_alias="ignoreTest"
    )

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Int64Test(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: typing.Literal[1] = Field(
        default=0, alias_priority=1, validation_alias="constTest", serialization_alias="constTest"
    )
    range_e_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeETest", serialization_alias="rangeETest", ge=1, le=10
    )
    range_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeTest", serialization_alias="rangeTest", gt=1, lt=10
    )
    in_test: int = Field(
        default=0, alias_priority=1, validation_alias="inTest", serialization_alias="inTest", in_=[1, 2, 3]
    )
    not_in_test: int = Field(
        default=0, alias_priority=1, validation_alias="notInTest", serialization_alias="notInTest", not_in=[1, 2, 3]
    )
    ignore_test: int = Field(
        default=0, alias_priority=1, validation_alias="ignoreTest", serialization_alias="ignoreTest"
    )

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class MapTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    pair_test: typing.Dict[str, int] = Field(
        default_factory=dict,
        alias_priority=1,
        validation_alias="pairTest",
        serialization_alias="pairTest",
        map_min_pairs=1,
        map_max_pairs=5,
    )
    no_parse_test: typing.Dict[str, int] = Field(
        default_factory=dict, alias_priority=1, validation_alias="noParseTest", serialization_alias="noParseTest"
    )
    keys_test: typing.Dict[typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)], int] = Field(
        default_factory=dict, alias_priority=1, validation_alias="keysTest", serialization_alias="keysTest"
    )
    values_test: typing.Dict[str, typing_extensions.Annotated[int, Ge(ge=5), Le(le=5)]] = Field(
        default_factory=dict, alias_priority=1, validation_alias="valuesTest", serialization_alias="valuesTest"
    )
    keys_values_test: typing.Dict[
        typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)],
        typing_extensions.Annotated[DatetimeType, gt_now(True)],
    ] = Field(
        default_factory=dict, alias_priority=1, validation_alias="keysValuesTest", serialization_alias="keysValuesTest"
    )
    ignore_test: typing.Dict[str, int] = Field(
        default_factory=dict, alias_priority=1, validation_alias="ignoreTest", serialization_alias="ignoreTest"
    )

    pair_test_map_min_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_min_pairs_validator
    )
    pair_test_map_max_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_max_pairs_validator
    )


class MessageDisabledTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: int = Field(default=0, alias_priority=1, validation_alias="constTest", serialization_alias="constTest")
    range_e_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeETest", serialization_alias="rangeETest"
    )
    range_test: int = Field(default=0, alias_priority=1, validation_alias="rangeTest", serialization_alias="rangeTest")


class MessageIgnoredTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: int = Field(default=0, alias_priority=1, validation_alias="constTest", serialization_alias="constTest")
    range_e_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeETest", serialization_alias="rangeETest"
    )
    range_test: int = Field(default=0, alias_priority=1, validation_alias="rangeTest", serialization_alias="rangeTest")


class MessageTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    skip_test: str = Field(default="", alias_priority=1, validation_alias="skipTest", serialization_alias="skipTest")
    required_test: str = Field(alias_priority=1, validation_alias="requiredTest", serialization_alias="requiredTest")


class StringTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: typing.Literal["aaa"] = Field(
        default="", alias_priority=1, validation_alias="constTest", serialization_alias="constTest"
    )
    len_test: str = Field(
        default="", alias_priority=1, validation_alias="lenTest", serialization_alias="lenTest", len=3
    )
    s_range_len_test: str = Field(
        default="",
        alias_priority=1,
        validation_alias="sRangeLenTest",
        serialization_alias="sRangeLenTest",
        min_length=1,
        max_length=3,
    )
    b_range_len_test: str = Field(
        default="", alias_priority=1, validation_alias="bRangeLenTest", serialization_alias="bRangeLenTest"
    )
    pattern_test: str = Field(
        default="", alias_priority=1, validation_alias="patternTest", serialization_alias="patternTest"
    )
    prefix_test: str = Field(
        default="", alias_priority=1, validation_alias="prefixTest", serialization_alias="prefixTest", prefix="prefix"
    )
    suffix_test: str = Field(
        default="", alias_priority=1, validation_alias="suffixTest", serialization_alias="suffixTest", suffix="suffix"
    )
    contains_test: str = Field(
        default="",
        alias_priority=1,
        validation_alias="containsTest",
        serialization_alias="containsTest",
        contains="contains",
    )
    not_contains_test: str = Field(
        default="",
        alias_priority=1,
        validation_alias="notContainsTest",
        serialization_alias="notContainsTest",
        not_contains="not_contains",
    )
    in_test: str = Field(
        default="", alias_priority=1, validation_alias="inTest", serialization_alias="inTest", in_=["a", "b", "c"]
    )
    not_in_test: str = Field(
        default="",
        alias_priority=1,
        validation_alias="notInTest",
        serialization_alias="notInTest",
        not_in=["a", "b", "c"],
    )
    email_test: EmailStr = Field(
        default="", alias_priority=1, validation_alias="emailTest", serialization_alias="emailTest"
    )
    hostname_test: HostNameStr = Field(
        default="", alias_priority=1, validation_alias="hostnameTest", serialization_alias="hostnameTest"
    )
    ip_test: IPvAnyAddress = Field(
        default="", alias_priority=1, validation_alias="ipTest", serialization_alias="ipTest"
    )
    ipv4_test: IPv4Address = Field(
        default="", alias_priority=1, validation_alias="ipv4Test", serialization_alias="ipv4Test"
    )
    ipv6_test: IPv6Address = Field(
        default="", alias_priority=1, validation_alias="ipv6Test", serialization_alias="ipv6Test"
    )
    uri_test: AnyUrl = Field(default="", alias_priority=1, validation_alias="uriTest", serialization_alias="uriTest")
    uri_ref_test: UriRefStr = Field(
        default="", alias_priority=1, validation_alias="uriRefTest", serialization_alias="uriRefTest"
    )
    address_test: IPvAnyAddress = Field(
        default="", alias_priority=1, validation_alias="addressTest", serialization_alias="addressTest"
    )
    uuid_test: UUID = Field(default="", alias_priority=1, validation_alias="uuidTest", serialization_alias="uuidTest")
    ignore_test: str = Field(
        default="", alias_priority=1, validation_alias="ignoreTest", serialization_alias="ignoreTest"
    )

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
            default="",
            alias_priority=1,
            validation_alias="bankNumber",
            serialization_alias="bankNumber",
            min_length=13,
            max_length=19,
        )
        exp: typing_extensions.Annotated[
            datetime, PlainSerializer(func=timestamp_serializer, return_type=str, when_used="json")
        ] = Field(
            default_factory=datetime_utc_now,
            alias_priority=1,
            validation_alias="exp",
            serialization_alias="exp",
            timestamp_gt_now=True,
        )
        uuid: UUID = Field(default="", alias_priority=1, validation_alias="uuid", serialization_alias="uuid")

        exp_timestamp_gt_now_validator = field_validator("exp", mode="after", check_fields=None)(
            timestamp_gt_now_validator
        )

    class NotEnableUserPayMessage(ProtobufCompatibleBaseModel):
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

    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    string_in_map_test: typing.Dict[str, StringTest] = Field(
        default_factory=dict,
        alias_priority=1,
        validation_alias="stringInMapTest",
        serialization_alias="stringInMapTest",
    )
    map_in_map_test: typing.Dict[str, MapTest] = Field(
        default_factory=dict, alias_priority=1, validation_alias="mapInMapTest", serialization_alias="mapInMapTest"
    )
    user_pay: UserPayMessage = Field(
        default_factory=UserPayMessage, alias_priority=1, validation_alias="userPay", serialization_alias="userPay"
    )
    not_enable_user_pay: NotEnableUserPayMessage = Field(
        default_factory=NotEnableUserPayMessage,
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


class OneOfNotTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    _one_of_dict = {"validate_test.OneOfNotTest.id": {"fields": {"x", "y"}, "required": False}}

    header: str = Field(default="", alias_priority=1, validation_alias="header", serialization_alias="header")
    x: str = Field(default="", alias_priority=1, validation_alias="x", serialization_alias="x")
    y: int = Field(default=0, alias_priority=1, validation_alias="y", serialization_alias="y")

    one_of_validator = model_validator(mode="before")(check_one_of)


class OneOfTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    _one_of_dict = {"validate_test.OneOfTest.id": {"fields": {"x", "y"}, "required": True}}

    header: str = Field(default="", alias_priority=1, validation_alias="header", serialization_alias="header")
    x: str = Field(default="", alias_priority=1, validation_alias="x", serialization_alias="x")
    y: int = Field(default=0, alias_priority=1, validation_alias="y", serialization_alias="y")

    one_of_validator = model_validator(mode="before")(check_one_of)


class RepeatedTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    range_test: typing.List[str] = Field(
        default_factory=list,
        alias_priority=1,
        validation_alias="rangeTest",
        serialization_alias="rangeTest",
        min_length=1,
        max_length=5,
    )
    unique_test: typing.Set[str] = Field(
        default_factory=set, alias_priority=1, validation_alias="uniqueTest", serialization_alias="uniqueTest"
    )
    items_string_test: typing.List[typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)]] = (
        Field(
            default_factory=list,
            alias_priority=1,
            validation_alias="itemsStringTest",
            serialization_alias="itemsStringTest",
            min_length=1,
            max_length=5,
        )
    )
    items_double_test: typing.List[typing_extensions.Annotated[float, Gt(gt=1.0), Lt(lt=5.0)]] = Field(
        default_factory=list,
        alias_priority=1,
        validation_alias="itemsDoubleTest",
        serialization_alias="itemsDoubleTest",
        min_length=1,
        max_length=5,
    )
    items_int32_test: typing.List[typing_extensions.Annotated[int, Gt(gt=1), Lt(lt=5)]] = Field(
        default_factory=list,
        alias_priority=1,
        validation_alias="itemsInt32Test",
        serialization_alias="itemsInt32Test",
        min_length=1,
        max_length=5,
    )
    items_timestamp_test: typing.List[
        typing_extensions.Annotated[DatetimeType, t_gt(1600000000.0), t_lt(1600000010.0)]
    ] = Field(
        default_factory=list,
        alias_priority=1,
        validation_alias="itemsTimestampTest",
        serialization_alias="itemsTimestampTest",
        min_length=1,
        max_length=5,
    )
    items_duration_test: typing.List[
        typing_extensions.Annotated[TimedeltaType, Gt(gt=timedelta(seconds=10)), Lt(lt=timedelta(seconds=20))]
    ] = Field(
        default_factory=list,
        alias_priority=1,
        validation_alias="itemsDurationTest",
        serialization_alias="itemsDurationTest",
        min_length=1,
        max_length=5,
    )
    items_bytes_test: typing.List[typing_extensions.Annotated[bytes, MinLen(min_length=1), MaxLen(max_length=5)]] = (
        Field(
            default_factory=list,
            alias_priority=1,
            validation_alias="itemsBytesTest",
            serialization_alias="itemsBytesTest",
            min_length=1,
            max_length=5,
        )
    )
    ignore_test: typing.List[str] = Field(
        default_factory=list, alias_priority=1, validation_alias="ignoreTest", serialization_alias="ignoreTest"
    )


class Sfixed32Test(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: typing.Literal[1] = Field(
        default=0, alias_priority=1, validation_alias="constTest", serialization_alias="constTest"
    )
    range_e_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeETest", serialization_alias="rangeETest", ge=1, le=10
    )
    range_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeTest", serialization_alias="rangeTest", gt=1, lt=10
    )
    in_test: int = Field(
        default=0, alias_priority=1, validation_alias="inTest", serialization_alias="inTest", in_=[1, 2, 3]
    )
    not_in_test: int = Field(
        default=0, alias_priority=1, validation_alias="notInTest", serialization_alias="notInTest", not_in=[1, 2, 3]
    )
    ignore_test: int = Field(
        default=0, alias_priority=1, validation_alias="ignoreTest", serialization_alias="ignoreTest"
    )

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Sfixed64Test(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: typing.Literal[1] = Field(
        default=0, alias_priority=1, validation_alias="constTest", serialization_alias="constTest"
    )
    range_e_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeETest", serialization_alias="rangeETest", ge=1, le=10
    )
    range_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeTest", serialization_alias="rangeTest", gt=1, lt=10
    )
    in_test: int = Field(
        default=0, alias_priority=1, validation_alias="inTest", serialization_alias="inTest", in_=[1, 2, 3]
    )
    not_in_test: int = Field(
        default=0, alias_priority=1, validation_alias="notInTest", serialization_alias="notInTest", not_in=[1, 2, 3]
    )
    ignore_test: int = Field(
        default=0, alias_priority=1, validation_alias="ignoreTest", serialization_alias="ignoreTest"
    )

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Sint32Test(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: typing.Literal[1] = Field(
        default=0, alias_priority=1, validation_alias="constTest", serialization_alias="constTest"
    )
    range_e_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeETest", serialization_alias="rangeETest", ge=1, le=10
    )
    range_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeTest", serialization_alias="rangeTest", gt=1, lt=10
    )
    in_test: int = Field(
        default=0, alias_priority=1, validation_alias="inTest", serialization_alias="inTest", in_=[1, 2, 3]
    )
    not_in_test: int = Field(
        default=0, alias_priority=1, validation_alias="notInTest", serialization_alias="notInTest", not_in=[1, 2, 3]
    )
    ignore_test: int = Field(
        default=0, alias_priority=1, validation_alias="ignoreTest", serialization_alias="ignoreTest"
    )

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Sint64Test(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: typing.Literal[1] = Field(
        default=0, alias_priority=1, validation_alias="constTest", serialization_alias="constTest"
    )
    range_e_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeETest", serialization_alias="rangeETest", ge=1, le=10
    )
    range_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeTest", serialization_alias="rangeTest", gt=1, lt=10
    )
    in_test: int = Field(
        default=0, alias_priority=1, validation_alias="inTest", serialization_alias="inTest", in_=[1, 2, 3]
    )
    not_in_test: int = Field(
        default=0, alias_priority=1, validation_alias="notInTest", serialization_alias="notInTest", not_in=[1, 2, 3]
    )
    ignore_test: int = Field(
        default=0, alias_priority=1, validation_alias="ignoreTest", serialization_alias="ignoreTest"
    )

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class TimestampTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    required_test: typing_extensions.Annotated[
        datetime, PlainSerializer(func=timestamp_serializer, return_type=str, when_used="json")
    ] = Field(alias_priority=1, validation_alias="requiredTest", serialization_alias="requiredTest")
    const_test: typing_extensions.Annotated[
        datetime, PlainSerializer(func=timestamp_serializer, return_type=str, when_used="json")
    ] = Field(
        default_factory=datetime_utc_now,
        alias_priority=1,
        validation_alias="constTest",
        serialization_alias="constTest",
        timestamp_const=1600000000.0,
    )
    range_test: typing_extensions.Annotated[
        datetime, PlainSerializer(func=timestamp_serializer, return_type=str, when_used="json")
    ] = Field(
        default_factory=datetime_utc_now,
        alias_priority=1,
        validation_alias="rangeTest",
        serialization_alias="rangeTest",
        timestamp_lt=1600000010.0,
        timestamp_gt=1600000000.0,
    )
    range_e_test: typing_extensions.Annotated[
        datetime, PlainSerializer(func=timestamp_serializer, return_type=str, when_used="json")
    ] = Field(
        default_factory=datetime_utc_now,
        alias_priority=1,
        validation_alias="rangeETest",
        serialization_alias="rangeETest",
        timestamp_le=1600000010.0,
        timestamp_ge=1600000000.0,
    )
    lt_now_test: typing_extensions.Annotated[
        datetime, PlainSerializer(func=timestamp_serializer, return_type=str, when_used="json")
    ] = Field(
        default_factory=datetime_utc_now,
        alias_priority=1,
        validation_alias="ltNowTest",
        serialization_alias="ltNowTest",
        timestamp_lt_now=True,
    )
    gt_now_test: typing_extensions.Annotated[
        datetime, PlainSerializer(func=timestamp_serializer, return_type=str, when_used="json")
    ] = Field(
        default_factory=datetime_utc_now,
        alias_priority=1,
        validation_alias="gtNowTest",
        serialization_alias="gtNowTest",
        timestamp_gt_now=True,
    )
    within_test: typing_extensions.Annotated[
        datetime, PlainSerializer(func=timestamp_serializer, return_type=str, when_used="json")
    ] = Field(
        default_factory=datetime_utc_now,
        alias_priority=1,
        validation_alias="withinTest",
        serialization_alias="withinTest",
        timestamp_within=timedelta(seconds=1),
    )
    within_and_gt_now_test: typing_extensions.Annotated[
        datetime, PlainSerializer(func=timestamp_serializer, return_type=str, when_used="json")
    ] = Field(
        default_factory=datetime_utc_now,
        alias_priority=1,
        validation_alias="withinAndGtNowTest",
        serialization_alias="withinAndGtNowTest",
        timestamp_gt_now=True,
        timestamp_within=timedelta(seconds=3600),
    )

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


class Uint32Test(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: typing.Literal[1] = Field(
        default=0, alias_priority=1, validation_alias="constTest", serialization_alias="constTest"
    )
    range_e_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeETest", serialization_alias="rangeETest", ge=1, le=10
    )
    range_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeTest", serialization_alias="rangeTest", gt=1, lt=10
    )
    in_test: int = Field(
        default=0, alias_priority=1, validation_alias="inTest", serialization_alias="inTest", in_=[1, 2, 3]
    )
    not_in_test: int = Field(
        default=0, alias_priority=1, validation_alias="notInTest", serialization_alias="notInTest", not_in=[1, 2, 3]
    )
    ignore_test: int = Field(
        default=0, alias_priority=1, validation_alias="ignoreTest", serialization_alias="ignoreTest"
    )

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)


class Uint64Test(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    const_test: typing.Literal[1] = Field(
        default=0, alias_priority=1, validation_alias="constTest", serialization_alias="constTest"
    )
    range_e_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeETest", serialization_alias="rangeETest", ge=1, le=10
    )
    range_test: int = Field(
        default=0, alias_priority=1, validation_alias="rangeTest", serialization_alias="rangeTest", gt=1, lt=10
    )
    in_test: int = Field(
        default=0, alias_priority=1, validation_alias="inTest", serialization_alias="inTest", in_=[1, 2, 3]
    )
    not_in_test: int = Field(
        default=0, alias_priority=1, validation_alias="notInTest", serialization_alias="notInTest", not_in=[1, 2, 3]
    )
    ignore_test: int = Field(
        default=0, alias_priority=1, validation_alias="ignoreTest", serialization_alias="ignoreTest"
    )

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
