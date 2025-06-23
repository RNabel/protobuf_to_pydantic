import sys
import time
from typing import Any

from expecttest import assert_expected_inline
from google.protobuf import __version__

from tests.test_gen_code.test_helper import P2CNoHeader

if __version__ > "4.0.0":
    from example.proto_pydanticv2.example.example_proto.validate import demo_pb2
else:
    from example.proto_3_20_pydanticv2.example.example_proto.validate import (
        demo_pb2,
    )

from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_code


def exp_time() -> float:
    return time.time()


class TestValidate:
    @staticmethod
    def _model_output(msg: Any) -> str:
        return pydantic_model_to_py_code(
            msg_to_pydantic_model(msg, parse_msg_desc_method="PGV"),
            p2c_class=P2CNoHeader,
        )

    def test_string(self) -> None:
        output = self._model_output(demo_pb2.StringTest)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_any(self) -> None:
        output = self._model_output(demo_pb2.AnyTest)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_bool(self) -> None:
        output = self._model_output(demo_pb2.BoolTest)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_bytes(self) -> None:
        output = self._model_output(demo_pb2.BytesTest)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_double(self) -> None:
        output = self._model_output(demo_pb2.DoubleTest)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_duration(self) -> None:
        output = self._model_output(demo_pb2.DurationTest)
        assert_expected_inline(
            output,
            """\
class DurationTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    required_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        alias_priority=1, validation_alias="requiredTest", serialization_alias="requiredTest"
    )
    const_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta,
        alias_priority=1,
        validation_alias="constTest",
        serialization_alias="constTest",
        duration_const=timedelta(seconds=1, microseconds=500000),
    )
    range_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta,
        alias_priority=1,
        validation_alias="rangeTest",
        serialization_alias="rangeTest",
        duration_lt=timedelta(seconds=10, microseconds=500000),
        duration_gt=timedelta(seconds=5, microseconds=500000),
    )
    range_e_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta,
        alias_priority=1,
        validation_alias="rangeETest",
        serialization_alias="rangeETest",
        duration_le=timedelta(seconds=10, microseconds=500000),
        duration_ge=timedelta(seconds=5, microseconds=500000),
    )
    in_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta,
        alias_priority=1,
        validation_alias="inTest",
        serialization_alias="inTest",
        duration_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )
    not_in_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
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
""",
        )

    def test_enum(self) -> None:
        output = self._model_output(demo_pb2.EnumTest)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_fixed32(self) -> None:
        output = self._model_output(demo_pb2.Fixed32Test)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_fixed64(self) -> None:
        output = self._model_output(demo_pb2.Fixed64Test)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_float(self) -> None:
        output = self._model_output(demo_pb2.FloatTest)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_int32(self) -> None:
        output = self._model_output(demo_pb2.Int32Test)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_int64(self) -> None:
        output = self._model_output(demo_pb2.Int64Test)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_map(self) -> None:
        output = self._model_output(demo_pb2.MapTest)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_message_disable(self) -> None:
        output = self._model_output(demo_pb2.MessageDisabledTest)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_message_ignored(self) -> None:
        output = self._model_output(demo_pb2.MessageIgnoredTest)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_message(self) -> None:
        output = self._model_output(demo_pb2.MessageTest)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_nested(self) -> None:
        output = self._model_output(demo_pb2.NestedMessage)
        assert_expected_inline(
            output,
            """\
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
        exp: datetime = Field(
            default_factory=datetime.now,
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
        exp: datetime = Field(
            default_factory=datetime.now, alias_priority=1, validation_alias="exp", serialization_alias="exp"
        )
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
""",
        )

    def test_one_of_not(self) -> None:
        output = self._model_output(demo_pb2.OneOfNotTest)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_one_of(self) -> None:
        output = self._model_output(demo_pb2.OneOfTest)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_repeated(self) -> None:
        output = self._model_output(demo_pb2.RepeatedTest)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_sfixed32(self) -> None:
        output = self._model_output(demo_pb2.Sfixed32Test)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_sfixed64(self) -> None:
        output = self._model_output(demo_pb2.Sfixed64Test)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_sint64(self) -> None:
        output = self._model_output(demo_pb2.Sint64Test)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_timestamp(self) -> None:
        output = self._model_output(demo_pb2.TimestampTest)
        assert_expected_inline(
            output,
            """\
class TimestampTest(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    required_test: datetime = Field(
        alias_priority=1, validation_alias="requiredTest", serialization_alias="requiredTest"
    )
    const_test: datetime = Field(
        default_factory=datetime.now,
        alias_priority=1,
        validation_alias="constTest",
        serialization_alias="constTest",
        timestamp_const=1600000000.0,
    )
    range_test: datetime = Field(
        default_factory=datetime.now,
        alias_priority=1,
        validation_alias="rangeTest",
        serialization_alias="rangeTest",
        timestamp_lt=1600000010.0,
        timestamp_gt=1600000000.0,
    )
    range_e_test: datetime = Field(
        default_factory=datetime.now,
        alias_priority=1,
        validation_alias="rangeETest",
        serialization_alias="rangeETest",
        timestamp_le=1600000010.0,
        timestamp_ge=1600000000.0,
    )
    lt_now_test: datetime = Field(
        default_factory=datetime.now,
        alias_priority=1,
        validation_alias="ltNowTest",
        serialization_alias="ltNowTest",
        timestamp_lt_now=True,
    )
    gt_now_test: datetime = Field(
        default_factory=datetime.now,
        alias_priority=1,
        validation_alias="gtNowTest",
        serialization_alias="gtNowTest",
        timestamp_gt_now=True,
    )
    within_test: datetime = Field(
        default_factory=datetime.now,
        alias_priority=1,
        validation_alias="withinTest",
        serialization_alias="withinTest",
        timestamp_within=timedelta(seconds=1),
    )
    within_and_gt_now_test: datetime = Field(
        default_factory=datetime.now,
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
""",
        )

    def test_unit32(self) -> None:
        output = self._model_output(demo_pb2.Uint32Test)
        assert_expected_inline(
            output,
            """\
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
""",
        )

    def test_unit64(self) -> None:
        output = self._model_output(demo_pb2.Uint64Test)
        assert_expected_inline(
            output,
            """\
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
""",
        )
