import textwrap
import time
from typing import Any

from expecttest import assert_expected_inline
from google.protobuf import __version__

from protobuf_to_pydantic._pydantic_adapter import is_v1
from tests.test_gen_code.test_helper import P2CNoHeader

if __version__ > "4.0.0":
    if is_v1:
        from example.proto_pydanticv1.example.example_proto.p2p_validate import demo_pb2
    else:
        from example.proto_pydanticv2.example.example_proto.p2p_validate import demo_pb2
else:
    if is_v1:
        from example.proto_3_20_pydanticv1.example.example_proto.p2p_validate import (
            demo_pb2,
        )  # type: ignore[no-redef]
    else:
        from example.proto_3_20_pydanticv2.example.example_proto.p2p_validate import (
            demo_pb2,
        )  # type: ignore[no-redef]

from example.gen_p2p_code import (
    CustomCommentTemplate,
    CustomerField,
    confloat,
    conint,
    customer_any,
)
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_code


def exp_time() -> float:
    return time.time()


class TestP2pValidate:
    @staticmethod
    def _model_output(msg: Any) -> str:
        local_dict: dict = {
            "CustomerField": CustomerField,
            "confloat": confloat,
            "conint": conint,
            "customer_any": customer_any,
        }
        return pydantic_model_to_py_code(
            msg_to_pydantic_model(
                msg, local_dict=local_dict, template=CustomCommentTemplate
            ),
            p2c_class=P2CNoHeader,
        )

    def test_any(self) -> None:
        output = self._model_output(demo_pb2.AnyTest)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class AnyTest(BaseModel):
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
    miss_default_test: Any = Field()
    alias_test: Any = Field(default_factory=Any, alias="alias", alias_priority=2)
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
""",
            )
        else:
            assert_expected_inline(
                output,
                """
from google.protobuf.any_pb2 import Any  # type: ignore
from pydantic import BaseModel, Field, validator

from example.gen_p2p_code import CustomerField, customer_any
from protobuf_to_pydantic.util import any_in_validator, any_not_in_validator


class AnyTest(BaseModel):
    class Config:
        arbitrary_types_allowed = True

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
    miss_default_test: Any = Field()
    alias_test: Any = Field(default_factory=Any, alias="alias", alias_priority=2)
    desc_test: Any = Field(default_factory=Any, description="test desc")
    example_test: Any = Field(default_factory=Any, example="type.googleapis.com/google.protobuf.Duration")
    example_factory_test: Any = Field(default_factory=Any, example=customer_any)
    field_test: Any = CustomerField(default_factory=Any)
    title_test: Any = Field(default_factory=Any, title="title_test")
    extra_test: Any = Field(default_factory=Any, customer_string="c1", customer_int=1)

    not_in_test_any_not_in_validator = validator("not_in_test", allow_reuse=True)(any_not_in_validator)
    in_test_any_in_validator = validator("in_test", allow_reuse=True)(any_in_validator)
""",
            )

    def test_bool(self) -> None:
        output = self._model_output(demo_pb2.BoolTest)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class BoolTest(BaseModel):
    bool_1_test: typing.Literal[True] = Field(default=False)
    bool_2_test: typing.Literal[False] = Field(default=False)
    default_test: bool = Field(default=True)
    miss_default_test: bool = Field()
    required_test: bool = Field()
    alias_test: bool = Field(default=False, alias="alias", alias_priority=2)
    desc_test: bool = Field(default=False, description="test desc")
    example_test: bool = Field(default=False, example=True)
    field_test: bool = CustomerField(default=False)
    title_test: bool = Field(default=False, title="title_test")
    extra_test: bool = Field(default=False, customer_string="c1", customer_int=1)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
from pydantic import BaseModel, Field

from example.gen_p2p_code import CustomerField


class BoolTest(BaseModel):
    bool_1_test: bool = Field(default=True, const=True)
    bool_2_test: bool = Field(default=False, const=True)
    default_test: bool = Field(default=True)
    miss_default_test: bool = Field()
    required_test: bool = Field()
    alias_test: bool = Field(default=False, alias="alias", alias_priority=2)
    desc_test: bool = Field(default=False, description="test desc")
    example_test: bool = Field(default=False, example=True)
    field_test: bool = CustomerField(default=False)
    title_test: bool = Field(default=False, title="title_test")
    extra_test: bool = Field(default=False, customer_string="c1", customer_int=1)
""",
            )

    def test_bytes(self) -> None:
        output = self._model_output(demo_pb2.BytesTest)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class BytesTest(BaseModel):
    const_test: typing.Literal[b"demo"] = Field(default=b"")
    range_len_test: bytes = Field(default=b"", min_length=1, max_length=4)
    prefix_test: bytes = Field(default=b"", prefix=b"prefix")
    suffix_test: bytes = Field(default=b"", suffix=b"suffix")
    contains_test: bytes = Field(default=b"", contains=b"contains")
    in_test: bytes = Field(default=b"", in_=[b"a", b"b", b"c"])
    not_in_test: bytes = Field(default=b"", not_in=[b"a", b"b", b"c"])
    default_test: bytes = Field(default=b"default")
    default_factory_test: bytes = Field(default_factory=bytes)
    miss_default_test: bytes = Field()
    required_test: bytes = Field()
    alias_test: bytes = Field(default=b"", alias="alias", alias_priority=2)
    desc_test: bytes = Field(default=b"", description="test desc")
    example_test: bytes = Field(default=b"", example=b"example")
    example_factory_test: bytes = Field(default=b"", example=bytes)
    field_test: bytes = CustomerField(default=b"")
    title_test: bytes = Field(default=b"", title="title_test")
    type_test: str = Field(default=b"")
    extra_test: bytes = Field(default=b"", customer_string="c1", customer_int=1)

    prefix_test_prefix_validator = field_validator("prefix_test", mode="after", check_fields=None)(prefix_validator)
    suffix_test_suffix_validator = field_validator("suffix_test", mode="after", check_fields=None)(suffix_validator)
    contains_test_contains_validator = field_validator("contains_test", mode="after", check_fields=None)(
        contains_validator
    )
    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
""",
            )
        else:
            assert_expected_inline(
                output,
                """""",
            )

    def test_double(self) -> None:
        output = self._model_output(demo_pb2.DoubleTest)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class DoubleTest(BaseModel):
    const_test: typing.Literal[1.0] = Field(default=0.0)
    range_e_test: float = Field(default=0.0, ge=1.0, le=10.0)
    range_test: float = Field(default=0.0, gt=1.0, lt=10.0)
    in_test: float = Field(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = Field(default=0.0, not_in=[1.0, 2.0, 3.0])
    default_test: float = Field(default=1.0)
    default_template_test: float = Field(default=1600000000)
    default_factory_test: float = Field(default_factory=float)
    miss_default_test: float = Field()
    required_test: float = Field()
    alias_test: float = Field(default=0.0, alias="alias", alias_priority=2)
    desc_test: float = Field(default=0.0, description="test desc")
    multiple_of_test: float = Field(default=0.0, multiple_of=3)
    example_test: float = Field(default=0.0, example=1.0)
    example_factory: float = Field(default=0.0, example=float)
    field_test: float = CustomerField(default=0.0)
    type_test: float = Field(default=0.0)
    title_test: float = Field(default=0.0, title="title_test")
    extra_test: float = Field(default=0.0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
""",
            )
        else:
            assert_expected_inline(
                output,
                """""",
            )

    def test_duration(self) -> None:
        output = self._model_output(demo_pb2.DurationTest)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class DurationTest(BaseModel):
    const_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta, duration_const=timedelta(seconds=1, microseconds=500000)
    )
    range_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta,
        duration_lt=timedelta(seconds=10, microseconds=500000),
        duration_gt=timedelta(seconds=5, microseconds=500000),
    )
    range_e_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta,
        duration_le=timedelta(seconds=10, microseconds=500000),
        duration_ge=timedelta(seconds=5, microseconds=500000),
    )
    in_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta,
        duration_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )
    not_in_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta,
        duration_not_in=[timedelta(seconds=1, microseconds=500000), timedelta(seconds=3, microseconds=500000)],
    )
    default_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default=timedelta(seconds=1, microseconds=500000)
    )
    default_factory_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=timedelta
    )
    miss_default_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field()
    required_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field()
    alias_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta, alias="alias", alias_priority=2
    )
    desc_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta, description="test desc"
    )
    example_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta, example=timedelta(seconds=1, microseconds=500000)
    )
    example_factory_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta, example=timedelta
    )
    field_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = CustomerField(
        default_factory=Timedelta
    )
    title_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta, title="title_test"
    )
    type_test: timedelta = Field(default_factory=Timedelta)
    extra_test: typing_extensions.Annotated[timedelta, BeforeValidator(func=Timedelta.validate)] = Field(
        default_factory=Timedelta, customer_string="c1", customer_int=1
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
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_enum(self) -> None:
        output = self._model_output(demo_pb2.EnumTest)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class State(IntEnum):
    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2


class EnumTest(BaseModel):
    model_config = ConfigDict(validate_default=True)

    const_test: typing.Literal[2] = Field(default=0)
    in_test: State = Field(default=0, in_=[0, 2])
    not_in_test: State = Field(default=0, not_in=[0, 2])
    default_test: State = Field(default=1)
    miss_default_test: State = Field()
    required_test: State = Field()
    alias_test: State = Field(default=0, alias="alias", alias_priority=2)
    desc_test: State = Field(default=0, description="test desc")
    example_test: State = Field(default=0, example=2)
    field_test: State = CustomerField(default=0)
    title_test: State = Field(default=0, title="title_test")
    extra_test: State = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_fixed32(self) -> None:
        output = self._model_output(demo_pb2.Fixed32Test)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class Fixed32Test(BaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    default_test: float = Field(default=1.0)
    default_template_test: float = Field(default=1600000000)
    default_factory_test: float = Field(default_factory=float)
    miss_default_test: float = Field()
    required_test: float = Field()
    alias_test: float = Field(default=0, alias="alias", alias_priority=2)
    desc_test: float = Field(default=0, description="test desc")
    multiple_of_test: float = Field(default=0, multiple_of=3)
    example_test: float = Field(default=0, example=1.0)
    example_factory: float = Field(default=0, example=float)
    field_test: float = CustomerField(default=0)
    type_test: float = Field(default=0)
    title_test: float = Field(default=0, title="title_test")
    extra_test: float = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_fixed64(self) -> None:
        output = self._model_output(demo_pb2.Fixed64Test)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class Fixed64Test(BaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    default_test: float = Field(default=1.0)
    default_template_test: float = Field(default=1600000000)
    default_factory_test: float = Field(default_factory=float)
    miss_default_test: float = Field()
    required_test: float = Field()
    alias_test: float = Field(default=0, alias="alias", alias_priority=2)
    desc_test: float = Field(default=0, description="test desc")
    multiple_of_test: float = Field(default=0, multiple_of=3)
    example_test: float = Field(default=0, example=1.0)
    example_factory: float = Field(default=0, example=float)
    field_test: float = CustomerField(default=0)
    type_test: float = Field(default=0)
    title_test: float = Field(default=0, title="title_test")
    extra_test: float = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_float(self) -> None:
        output = self._model_output(demo_pb2.FloatTest)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class FloatTest(BaseModel):
    const_test: typing.Literal[1.0] = Field(default=0.0)
    range_e_test: float = Field(default=0.0, ge=1.0, le=10.0)
    range_test: float = Field(default=0.0, gt=1.0, lt=10.0)
    in_test: float = Field(default=0.0, in_=[1.0, 2.0, 3.0])
    not_in_test: float = Field(default=0.0, not_in=[1.0, 2.0, 3.0])
    default_test: float = Field(default=1.0)
    default_template_test: float = Field(default=1600000000)
    default_factory_test: float = Field(default_factory=float)
    miss_default_test: float = Field()
    required_test: float = Field()
    alias_test: float = Field(default=0.0, alias="alias", alias_priority=2)
    desc_test: float = Field(default=0.0, description="test desc")
    multiple_of_test: float = Field(default=0.0, multiple_of=3)
    example_test: float = Field(default=0.0, example=1.0)
    example_factory: float = Field(default=0.0, example=float)
    field_test: float = CustomerField(default=0.0)
    type_test: float = Field(default=0.0)
    title_test: float = Field(default=0.0, title="title_test")
    extra_test: float = Field(default=0.0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_int32(self) -> None:
        output = self._model_output(demo_pb2.Int32Test)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class Int32Test(BaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_template_test: int = Field(default=1600000000)
    default_factory_test: int = Field(default_factory=int)
    miss_default_test: int = Field()
    required_test: int = Field()
    alias_test: int = Field(default=0, alias="alias", alias_priority=2)
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: float = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_int64(self) -> None:
        output = self._model_output(demo_pb2.Int64Test)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class Int64Test(BaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_template_test: int = Field(default=1600000000)
    default_factory_test: int = Field(default_factory=int)
    miss_default_test: int = Field()
    required_test: int = Field()
    alias_test: int = Field(default=0, alias="alias", alias_priority=2)
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: float = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_map(self) -> None:
        output = self._model_output(demo_pb2.MapTest)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = Field(default_factory=dict, map_min_pairs=1, map_max_pairs=5)
    keys_test: typing.Dict[typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)], int] = Field(
        default_factory=dict
    )
    values_test: typing.Dict[str, typing_extensions.Annotated[int, Ge(ge=5), Le(le=5)]] = Field(default_factory=dict)
    keys_values_test: typing.Dict[
        typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)],
        typing_extensions.Annotated[DatetimeType, gt_now(True)],
    ] = Field(default_factory=dict)
    default_factory_test: typing.Dict[str, int] = Field(default_factory=dict)
    miss_default_test: typing.Dict[str, int] = Field()
    required_test: typing.Dict[str, int] = Field()
    alias_test: typing.Dict[str, int] = Field(default_factory=dict, alias="alias", alias_priority=2)
    desc_test: typing.Dict[str, int] = Field(default_factory=dict, description="test desc")
    example_factory_test: typing.Dict[str, int] = Field(default_factory=dict, example=dict)
    field_test: typing.Dict[str, int] = CustomerField(default_factory=dict)
    title_test: typing.Dict[str, int] = Field(default_factory=dict, title="title_test")
    type_test: dict = Field(default_factory=dict)
    extra_test: typing.Dict[str, int] = Field(default_factory=dict, customer_string="c1", customer_int=1)

    pair_test_map_min_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_min_pairs_validator
    )
    pair_test_map_max_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_max_pairs_validator
    )
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_message_ignored(self) -> None:
        output = self._model_output(demo_pb2.MessageIgnoredTest)
        expected = textwrap.dedent("""
class MessageIgnoredTest(BaseModel):
    const_test: int = Field(default=0)
    range_e_test: int = Field(default=0)
    range_test: int = Field(default=0)
""").strip()
        assert expected in output

    def test_message(self) -> None:
        output = self._model_output(demo_pb2.MessageTest)
        expected = textwrap.dedent("""
class MessageTest(BaseModel):
    skip_test: str = Field(default="")
    required_test: str = Field()
    extra_test: str = Field(default="", customer_string="c1", customer_int=1)
""").strip()
        assert expected in output

    def test_nested(self) -> None:
        output = self._model_output(demo_pb2.NestedMessage)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class StringTest(BaseModel):
    const_test: typing.Literal["aaa"] = Field(default="")
    len_test: str = Field(default="", len=3)
    s_range_len_test: str = Field(default="", min_length=1, max_length=3)
    pattern_test: str = Field(default="")
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
    miss_default_test: str = Field()
    required_test: str = Field()
    alias_test: str = Field(default="", alias="alias", alias_priority=2)
    desc_test: str = Field(default="", description="test desc")
    example_test: str = Field(default="", example="example")
    example_factory_test: str = Field(default="", example=uuid4)
    field_test: str = CustomerField(default="")
    title_test: str = Field(default="", title="title_test")
    type_test: str = Field(default="")
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


class MapTest(BaseModel):
    pair_test: typing.Dict[str, int] = Field(default_factory=dict, map_min_pairs=1, map_max_pairs=5)
    keys_test: typing.Dict[typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)], int] = Field(
        default_factory=dict
    )
    values_test: typing.Dict[str, typing_extensions.Annotated[int, Ge(ge=5), Le(le=5)]] = Field(default_factory=dict)
    keys_values_test: typing.Dict[
        typing_extensions.Annotated[str, MinLen(min_length=1), MaxLen(max_length=5)],
        typing_extensions.Annotated[DatetimeType, gt_now(True)],
    ] = Field(default_factory=dict)
    default_factory_test: typing.Dict[str, int] = Field(default_factory=dict)
    miss_default_test: typing.Dict[str, int] = Field()
    required_test: typing.Dict[str, int] = Field()
    alias_test: typing.Dict[str, int] = Field(default_factory=dict, alias="alias", alias_priority=2)
    desc_test: typing.Dict[str, int] = Field(default_factory=dict, description="test desc")
    example_factory_test: typing.Dict[str, int] = Field(default_factory=dict, example=dict)
    field_test: typing.Dict[str, int] = CustomerField(default_factory=dict)
    title_test: typing.Dict[str, int] = Field(default_factory=dict, title="title_test")
    type_test: dict = Field(default_factory=dict)
    extra_test: typing.Dict[str, int] = Field(default_factory=dict, customer_string="c1", customer_int=1)

    pair_test_map_min_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_min_pairs_validator
    )
    pair_test_map_max_pairs_validator = field_validator("pair_test", mode="after", check_fields=None)(
        map_max_pairs_validator
    )


class AfterReferMessage(BaseModel):
    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", example=18.0, ge=0)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        bank_number: str = Field(default="", min_length=13, max_length=19)
        exp: datetime = Field(default_factory=datetime.now, timestamp_gt_now=True)
        uuid: UUID = Field(default="")

        exp_timestamp_gt_now_validator = field_validator("exp", mode="after", check_fields=None)(
            timestamp_gt_now_validator
        )

    class NotEnableUserPayMessage(BaseModel):
        bank_number: str = Field(default="")
        exp: datetime = Field(default_factory=datetime.now)
        uuid: str = Field(default="")

    string_in_map_test: typing.Dict[str, StringTest] = Field(default_factory=dict)
    map_in_map_test: typing.Dict[str, MapTest] = Field(default_factory=dict)
    user_pay: UserPayMessage = Field(default_factory=UserPayMessage)
    not_enable_user_pay: NotEnableUserPayMessage = Field(default_factory=NotEnableUserPayMessage)
    empty: typing.Any = Field()
    after_refer: AfterReferMessage = Field(default_factory=AfterReferMessage)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_one_of_not(self) -> None:
        output = self._model_output(demo_pb2.OneOfNotTest)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class OneOfNotTest(BaseModel):
    _one_of_dict = {"p2p_validate_test.OneOfNotTest.id": {"fields": {"x", "y"}, "required": False}}

    header: str = Field(default="")
    x: str = Field(default="")
    y: int = Field(default=0)

    one_of_validator = model_validator(mode="before")(check_one_of)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_one_of(self) -> None:
        output = self._model_output(demo_pb2.OneOfTest)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class OneOfTest(BaseModel):
    _one_of_dict = {"p2p_validate_test.OneOfTest.id": {"fields": {"x", "y"}, "required": True}}

    header: str = Field(default="")
    x: str = Field(default="")
    y: int = Field(default=0)

    one_of_validator = model_validator(mode="before")(check_one_of)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_one_of_optional(self) -> None:
        output = self._model_output(demo_pb2.OneOfOptionalTest)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class OneOfOptionalTest(BaseModel):
    _one_of_dict = {"p2p_validate_test.OneOfOptionalTest.id": {"fields": {"x", "y", "z"}, "required": True}}

    header: str = Field(default="")
    x: typing.Optional[str] = Field(default="")
    y: typing.Optional[int] = Field(default=0)
    z: bool = Field(default=False)
    name: typing.Optional[str] = Field(default="")
    age: typing.Optional[int] = Field(default=0)
    str_list: typing.List[str] = Field(default_factory=list)
    int_map: typing.Dict[str, int] = Field(default_factory=dict)

    one_of_validator = model_validator(mode="before")(check_one_of)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_repeated(self) -> None:
        output = self._model_output(demo_pb2.RepeatedTest)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class RepeatedTest(BaseModel):
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
    miss_default_test: typing.List[str] = Field()
    required_test: typing.List[str] = Field()
    alias_test: typing.List[str] = Field(default_factory=list, alias="alias", alias_priority=2)
    desc_test: typing.List[str] = Field(default_factory=list, description="test desc")
    example_factory_test: typing.List[str] = Field(default_factory=list, example=list)
    field_test: typing.List[str] = CustomerField(default_factory=list)
    title_test: typing.List[str] = Field(default_factory=list, title="title_test")
    type_test: list = Field(default_factory=list)
    extra_test: typing.List[str] = Field(default_factory=list, customer_string="c1", customer_int=1)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_sfixed32(self) -> None:
        output = self._model_output(demo_pb2.Sfixed32Test)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class Sfixed32Test(BaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    default_test: float = Field(default=1.0)
    default_template_test: float = Field(default=1600000000)
    default_factory_test: float = Field(default_factory=float)
    miss_default_test: float = Field()
    required_test: float = Field()
    alias_test: float = Field(default=0, alias="alias", alias_priority=2)
    desc_test: float = Field(default=0, description="test desc")
    multiple_of_test: float = Field(default=0, multiple_of=3)
    example_test: float = Field(default=0, example=1.0)
    example_factory: float = Field(default=0, example=float)
    field_test: float = CustomerField(default=0)
    type_test: float = Field(default=0)
    title_test: float = Field(default=0, title="title_test")
    extra_test: float = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_sfixed64(self) -> None:
        output = self._model_output(demo_pb2.Sfixed64Test)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class Sfixed64Test(BaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: float = Field(default=0, ge=1, le=10)
    range_test: float = Field(default=0, gt=1, lt=10)
    in_test: float = Field(default=0, in_=[1, 2, 3])
    not_in_test: float = Field(default=0, not_in=[1, 2, 3])
    default_test: float = Field(default=1.0)
    default_template_test: float = Field(default=1600000000)
    default_factory_test: float = Field(default_factory=float)
    miss_default_test: float = Field()
    required_test: float = Field()
    alias_test: float = Field(default=0, alias="alias", alias_priority=2)
    desc_test: float = Field(default=0, description="test desc")
    multiple_of_test: float = Field(default=0, multiple_of=3)
    example_test: float = Field(default=0, example=1.0)
    example_factory: float = Field(default=0, example=float)
    field_test: float = CustomerField(default=0)
    type_test: float = Field(default=0)
    title_test: float = Field(default=0, title="title_test")
    extra_test: float = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_sint64(self) -> None:
        output = self._model_output(demo_pb2.Sint64Test)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class Sint64Test(BaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_template_test: int = Field(default=1600000000)
    default_factory_test: int = Field(default_factory=int)
    miss_default_test: int = Field()
    required_test: int = Field()
    alias_test: int = Field(default=0, alias="alias", alias_priority=2)
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: int = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_string(self) -> None:
        output = self._model_output(demo_pb2.StringTest)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class StringTest(BaseModel):
    const_test: typing.Literal["aaa"] = Field(default="")
    len_test: str = Field(default="", len=3)
    s_range_len_test: str = Field(default="", min_length=1, max_length=3)
    pattern_test: str = Field(default="")
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
    miss_default_test: str = Field()
    required_test: str = Field()
    alias_test: str = Field(default="", alias="alias", alias_priority=2)
    desc_test: str = Field(default="", description="test desc")
    example_test: str = Field(default="", example="example")
    example_factory_test: str = Field(default="", example=uuid4)
    field_test: str = CustomerField(default="")
    title_test: str = Field(default="", title="title_test")
    type_test: str = Field(default="")
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
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_timestamp(self) -> None:
        output = self._model_output(demo_pb2.TimestampTest)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class TimestampTest(BaseModel):
    const_test: datetime = Field(default_factory=datetime.now, timestamp_const=1600000000.0)
    range_test: datetime = Field(default_factory=datetime.now, timestamp_lt=1600000010.0, timestamp_gt=1600000000.0)
    range_e_test: datetime = Field(default_factory=datetime.now, timestamp_le=1600000010.0, timestamp_ge=1600000000.0)
    lt_now_test: datetime = Field(default_factory=datetime.now, timestamp_lt_now=True)
    gt_now_test: datetime = Field(default_factory=datetime.now, timestamp_gt_now=True)
    within_test: datetime = Field(default_factory=datetime.now, timestamp_within=timedelta(seconds=1))
    within_and_gt_now_test: datetime = Field(
        default_factory=datetime.now, timestamp_gt_now=True, timestamp_within=timedelta(seconds=3600)
    )
    default_test: datetime = Field(default=1.5)
    default_factory_test: datetime = Field(default_factory=datetime.now)
    miss_default_test: datetime = Field()
    required_test: datetime = Field()
    alias_test: datetime = Field(default_factory=datetime.now, alias="alias", alias_priority=2)
    desc_test: datetime = Field(default_factory=datetime.now, description="test desc")
    example_test: datetime = Field(default_factory=datetime.now, example=1.5)
    example_factory_test: datetime = Field(default_factory=datetime.now, example=datetime.now)
    field_test: datetime = CustomerField(default_factory=datetime.now)
    title_test: datetime = Field(default_factory=datetime.now, title="title_test")
    type_test: datetime = Field(default_factory=datetime.now)
    extra_test: datetime = Field(default_factory=datetime.now, customer_string="c1", customer_int=1)

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
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_unit32(self) -> None:
        output = self._model_output(demo_pb2.Uint32Test)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class Uint32Test(BaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_template_test: int = Field(default=1600000000)
    default_factory_test: int = Field(default_factory=int)
    miss_default_test: int = Field()
    required_test: int = Field()
    alias_test: int = Field(default=0, alias="alias", alias_priority=2)
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: int = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_unit64(self) -> None:
        output = self._model_output(demo_pb2.Uint64Test)
        if not is_v1:
            assert_expected_inline(
                output,
                """\
class Uint64Test(BaseModel):
    const_test: typing.Literal[1] = Field(default=0)
    range_e_test: int = Field(default=0, ge=1, le=10)
    range_test: int = Field(default=0, gt=1, lt=10)
    in_test: int = Field(default=0, in_=[1, 2, 3])
    not_in_test: int = Field(default=0, not_in=[1, 2, 3])
    default_test: int = Field(default=1.0)
    default_template_test: int = Field(default=1600000000)
    default_factory_test: int = Field(default_factory=int)
    miss_default_test: int = Field()
    required_test: int = Field()
    alias_test: int = Field(default=0, alias="alias", alias_priority=2)
    desc_test: int = Field(default=0, description="test desc")
    multiple_of_test: int = Field(default=0, multiple_of=3)
    example_test: int = Field(default=0, example=1.0)
    example_factory: int = Field(default=0, example=int)
    field_test: int = CustomerField(default=0)
    type_test: int = Field(default=0)
    title_test: int = Field(default=0, title="title_test")
    extra_test: int = Field(default=0, customer_string="c1", customer_int=1)

    in_test_in_validator = field_validator("in_test", mode="after", check_fields=None)(in_validator)
    not_in_test_not_in_validator = field_validator("not_in_test", mode="after", check_fields=None)(not_in_validator)
""",
            )
        else:
            assert_expected_inline(
                output,
                """
""",
            )

    def test_optional_message(self):
        output = self._model_output(demo_pb2.OptionalMessage)
        assert_expected_inline(
            output,
            """\
class MessageIgnoredTest(BaseModel):
    const_test: int = Field(default=0)
    range_e_test: int = Field(default=0)
    range_test: int = Field(default=0)


class OptionalMessage(BaseModel):
    my_message1: typing.Optional[MessageIgnoredTest] = Field()
    my_message2: typing.Optional[MessageIgnoredTest] = Field(default_factory=MessageIgnoredTest)
    my_message3: MessageIgnoredTest = Field()
    my_message4: MessageIgnoredTest = Field(default_factory=MessageIgnoredTest)
    my_message_5: typing.Optional[MessageIgnoredTest] = Field(default=None)
""",
        )
