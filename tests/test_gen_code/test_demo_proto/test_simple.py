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
    pass
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

    earth: str = Field(default="")
    mercury: str = Field(default="")
    mars: str = Field(default="")


class UserMessage(BaseModel):
    model_config = ConfigDict(validate_default=True)

    uid: str = Field(default="")
    age: int = Field(default=0)
    height: float = Field(default=0.0)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage
    )
""",
        )

    def test_other_message(self) -> None:
        output = self._model_output(demo_pb2.OtherMessage)  # type: ignore
        assert_expected_inline(
            output,
            """\
class OtherMessage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    metadata: typing.Dict[str, typing.Any] = Field(default_factory=dict)
    double_value: DoubleValue = Field(default_factory=DoubleValue)
    field_mask: typing.Optional[FieldMask] = Field(default_factory=FieldMask)
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

    earth: str = Field(default="")
    mercury: str = Field(default="")
    mars: str = Field(default="")


class UserMessage(BaseModel):
    model_config = ConfigDict(validate_default=True)

    uid: str = Field(default="")
    age: int = Field(default=0)
    height: float = Field(default=0.0)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage
    )


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = Field(default_factory=dict)
    user_flag: typing.Dict[str, bool] = Field(default_factory=dict)
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

    earth: str = Field(default="")
    mercury: str = Field(default="")
    mars: str = Field(default="")


class UserMessage(BaseModel):
    model_config = ConfigDict(validate_default=True)

    uid: str = Field(default="")
    age: int = Field(default=0)
    height: float = Field(default=0.0)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage
    )


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = Field(default_factory=list)
    int_list: typing.List[int] = Field(default_factory=list)
    user_list: typing.List[UserMessage] = Field(default_factory=list)
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

    earth: str = Field(default="")
    mercury: str = Field(default="")
    mars: str = Field(default="")


class UserMessage(BaseModel):
    model_config = ConfigDict(validate_default=True)

    uid: str = Field(default="")
    age: int = Field(default=0)
    height: float = Field(default=0.0)
    sex: SexType = Field(default=0)
    demo: ExampleExampleProtoCommonSingleDemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="")
    demo_message: ExampleExampleProtoCommonSingleDemoMessage = Field(
        default_factory=ExampleExampleProtoCommonSingleDemoMessage
    )


class RepeatedMessage(BaseModel):
    str_list: typing.List[str] = Field(default_factory=list)
    int_list: typing.List[int] = Field(default_factory=list)
    user_list: typing.List[UserMessage] = Field(default_factory=list)


class MapMessage(BaseModel):
    user_map: typing.Dict[str, UserMessage] = Field(default_factory=dict)
    user_flag: typing.Dict[str, bool] = Field(default_factory=dict)


class AfterReferMessage(BaseModel):
    uid: str = Field(default="")
    age: int = Field(default=0)


class NestedMessage(BaseModel):
    class UserPayMessage(BaseModel):
        bank_number: str = Field(default="")
        exp: datetime = Field(default_factory=datetime.now)
        uuid: str = Field(default="")

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
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem"] = Field(default_factory=list)
""",
        )

    def test_self_referencing(self) -> None:
        output = self._model_output(demo_pb2.OptionalMessage)
        assert_expected_inline(
            output,
            """\
class InvoiceItem(BaseModel):
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem"] = Field(default_factory=list)


class OptionalMessage(BaseModel):
    _one_of_dict = {"user.OptionalMessage.a": {"fields": {"x", "y"}, "required": False}}

    x: str = Field(default="")
    y: int = Field(default=0)
    name: typing.Optional[str] = Field(default="")
    age: typing.Optional[int] = Field(default=0)
    item: typing.Optional[InvoiceItem] = Field(default_factory=InvoiceItem)
    str_list: typing.List[str] = Field(default_factory=list)
    int_map: typing.Dict[str, int] = Field(default_factory=dict)
    default_template_test: float = Field(default=0.0)

    one_of_validator = model_validator(mode="before")(check_one_of)
""",
        )

    def test_circular_references(self) -> None:
        output = self._model_output(demo_pb2.InvoiceItem2)
        assert_expected_inline(
            output,
            """\
class Invoice3(BaseModel):
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem2"] = Field(default_factory=list)


class InvoiceItem2(BaseModel):
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem2"] = Field(default_factory=list)
    invoice: Invoice3 = Field(default_factory=Invoice3)
""",
        )

    def test_message_reference(self) -> None:
        output = self._model_output(demo_pb2.RootMessage)
        assert_expected_inline(
            output,
            """\
class AnOtherMessage(BaseModel):
    class SubMessage(BaseModel):
        text: str = Field(default="")

    field1: str = Field(default="")
    field2: SubMessage = Field(default_factory=SubMessage)


class RootMessage(BaseModel):
    field1: str = Field(default="")
    field2: AnOtherMessage = Field(default_factory=AnOtherMessage)
""",
        )

    def test_same_bane_inline_structure(self) -> None:
        output = self._model_output(demo_pb2.TestSameName0)
        assert_expected_inline(
            output,
            """\
class TestSameName0(BaseModel):
    class Body(BaseModel):
        input_model: str = Field(default="")
        input_info: typing.Dict[str, str] = Field(default_factory=dict)

    body: Body = Field(default_factory=Body)
""",
        )

        output = self._model_output(demo_pb2.TestSameName1)
        assert_expected_inline(
            output,
            """\
class TestSameName1(BaseModel):
    class Body(BaseModel):
        output_model: str = Field(default="")
        output_info: typing.Dict[str, str] = Field(default_factory=dict)

    body: Body = Field(default_factory=Body)
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
    model_config = ConfigDict(validate_default=True)

    enum: typing.Optional[OptionalEnum] = Field(default=0)
""",
        )
