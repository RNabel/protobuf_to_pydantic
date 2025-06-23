from inspect import getsource

from expecttest import assert_expected_inline
from google.protobuf import __version__

from protobuf_to_pydantic._pydantic_adapter import is_v1

if __version__ > "4.0.0":
    if is_v1:
        from example.proto_pydanticv1.example.example_proto.demo import demo_p2p, diff_pkg_refer_2_p2p
    else:
        from example.proto_pydanticv2.example.example_proto.demo import (  # type: ignore[no-redef]
            demo_p2p,
            diff_pkg_refer_2_p2p,
        )
else:
    if is_v1:
        from example.proto_3_20_pydanticv1.example.example_proto.demo import (  # type: ignore[no-redef]
            demo_p2p,
            diff_pkg_refer_2_p2p,
        )
    else:
        from example.proto_3_20_pydanticv2.example.example_proto.demo import (  # type: ignore[no-redef]
            demo_p2p,
            diff_pkg_refer_2_p2p,
        )

class TestPlugin:

    def test_empty_message(self) -> None:
        output = getsource(demo_p2p.EmptyMessage)
        assert_expected_inline(output, """\
class EmptyMessage(BaseModel):
    pass
""")

    def test_user_message(self) -> None:
        output = getsource(demo_p2p.UserMessage)
        if not is_v1:
            assert_expected_inline(output, """\
class UserMessage(BaseModel):
    \"\"\"
    user info
    \"\"\"

    model_config = ConfigDict(validate_default=True)
    uid: str = Field(title="UID", description="user union id", example="10086")
    age: int = Field(default=0, title="use age", ge=0, example=18)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    sex: SexType = Field(default=0)
    demo: DemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", description="user name", min_length=1, max_length=10, example="so1n")
    demo_message: DemoMessage = Field(default_factory=DemoMessage, customer_string="c1", customer_int=1)
""")
        else:
            assert_expected_inline(output, """\
class UserMessage(BaseModel):
    \"\"\"
    user info
    \"\"\"

    class Config:
        validate_all = True

    uid: str = Field(example="10086", title="UID", description="user union id")
    age: int = Field(default=0, example=18, title="use age", ge=0.0)
    height: float = Field(default=0.0, ge=0.0, le=2.5)
    sex: SexType = Field(default=0)
    demo: DemoEnum = Field(default=0)
    is_adult: bool = Field(default=False)
    user_name: str = Field(default="", example="so1n", description="user name", min_length=1, max_length=10)
    demo_message: DemoMessage = Field(default_factory=DemoMessage, customer_string="c1", customer_int=1)
""")

    def test_other_message(self) -> None:
        output = getsource(demo_p2p.OtherMessage)
        if is_v1:
            assert_expected_inline(output, """\
class OtherMessage(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    metadata: typing.Dict[str, typing.Any] = Field(default_factory=dict)
    double_value: DoubleValue = Field(default_factory=DoubleValue)
    field_mask: typing.Optional[FieldMask] = Field(default_factory=FieldMask)
""")
        else:
            assert_expected_inline(output, """\
class OtherMessage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    metadata: typing.Dict[str, typing.Any] = Field(default_factory=dict)
    double_value: DoubleValue = Field(default_factory=DoubleValue)
    field_mask: typing.Optional[FieldMask] = Field(default_factory=FieldMask)
""")

    def test_map_message(self) -> None:
        output = getsource(demo_p2p.MapMessage)
        assert_expected_inline(output, """\
class MapMessage(BaseModel):
    \"\"\"
    test map message and bad message
    \"\"\"

    user_map: "typing.Dict[str, UserMessage]" = Field(default_factory=dict)
    user_flag: "typing.Dict[str, bool]" = Field(default_factory=dict)
""")

    def test_repeated_message(self) -> None:
        output = getsource(demo_p2p.RepeatedMessage)
        if is_v1:
            assert_expected_inline(output, """\
class RepeatedMessage(BaseModel):
    \"\"\"
    test repeated msg
    \"\"\"

    str_list: typing.List[str] = Field(default_factory=list, min_items=3, max_items=5)
    int_list: typing.List[int] = Field(default_factory=list, min_items=1, max_items=5, unique_items=True)
    user_list: typing.List[UserMessage] = Field(default_factory=list)
""")
        else:
            assert_expected_inline(output, """\
class RepeatedMessage(BaseModel):
    \"\"\"
    test repeated msg
    \"\"\"

    str_list: typing.List[str] = Field(default_factory=list, min_length=3, max_length=5)
    int_list: typing.Set[int] = Field(default_factory=set, min_length=1, max_length=5)
    user_list: typing.List[UserMessage] = Field(default_factory=list)
""")

    def test_nested_message(self) -> None:
        output = getsource(demo_p2p.NestedMessage)
        if is_v1:
            assert_expected_inline(output, """\
class NestedMessage(BaseModel):
    \"\"\"
    test nested message
    \"\"\"

    class UserPayMessage(BaseModel):
        bank_number: PaymentCardNumber = Field(default="")
        exp: datetime = Field(default_factory=exp_time)
        uuid: str = Field(default_factory=uuid4)

    class IncludeEnum(IntEnum):
        zero = 0
        one = 1
        two = 2

    class Config:
        validate_all = True

    user_list_map: "typing.Dict[str, RepeatedMessage]" = Field(default_factory=dict)
    user_map: "typing.Dict[str, MapMessage]" = Field(default_factory=dict)
    user_pay: "NestedMessage.UserPayMessage" = Field(default_factory=lambda: NestedMessage.UserPayMessage())
    include_enum: "NestedMessage.IncludeEnum" = Field(default=0)
    empty: None = Field()
    after_refer: AfterReferMessage = Field(default_factory=AfterReferMessage)
""")
        else:
            assert_expected_inline(output, """\
class NestedMessage(BaseModel):
    \"\"\"
    test nested message
    \"\"\"

    class UserPayMessage(BaseModel):
        bank_number: PaymentCardNumber = Field(default="")
        exp: datetime = Field(default_factory=exp_time)
        uuid: str = Field(default_factory=uuid4)

    class IncludeEnum(IntEnum):
        zero = 0
        one = 1
        two = 2

    model_config = ConfigDict(validate_default=True)
    user_list_map: "typing.Dict[str, RepeatedMessage]" = Field(default_factory=dict)
    user_map: "typing.Dict[str, MapMessage]" = Field(default_factory=dict)
    user_pay: "NestedMessage.UserPayMessage" = Field(default_factory=lambda: NestedMessage.UserPayMessage())
    include_enum: "NestedMessage.IncludeEnum" = Field(default=0)
    empty: None = Field()
    after_refer: AfterReferMessage = Field(default_factory=AfterReferMessage)
""")

    def test_self_referencing(self) -> None:
        output = getsource(demo_p2p.InvoiceItem)
        assert_expected_inline(output, """\
class InvoiceItem(BaseModel):
    \"\"\"
        Test self-referencing Messages
    from: https://github.com/so1n/protobuf_to_pydantic/issues/7#issuecomment-1490705932
    \"\"\"

    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem"] = Field(default_factory=list)
""")

    def test_field_optional(self) -> None:
        output = getsource(demo_p2p.OptionalMessage)
        if not is_v1:
            assert_expected_inline(output, """\
class OptionalMessage(BaseModel):
    _one_of_dict = {"OptionalMessage.a": {"fields": {"x", "yy"}, "required": True}}
    one_of_validator = model_validator(mode="before")(check_one_of)
    x: str = Field(default="")
    y: int = Field(default=0, alias="yy", title="use age", ge=0, example=18)
    name: typing.Optional[str] = Field(default="")
    age: typing.Optional[int] = Field(default=0)
    item: typing.Optional[InvoiceItem] = Field(default_factory=InvoiceItem)
    str_list: typing.List[str] = Field(default_factory=list)
    int_map: "typing.Dict[str, int]" = Field(default_factory=dict)
    default_template_test: float = Field(default=1600000000.0)
""")
        else:
            assert_expected_inline(output, """\
class OptionalMessage(BaseModel):
    _one_of_dict = {"OptionalMessage.a": {"fields": {"x", "yy"}, "required": True}}
    one_of_validator = root_validator(pre=True, allow_reuse=True)(check_one_of)
    x: str = Field(default="")
    y: int = Field(default=0, example=18, alias="yy", title="use age", ge=0.0)
    name: typing.Optional[str] = Field(default="")
    age: typing.Optional[int] = Field(default=0)
    item: typing.Optional[InvoiceItem] = Field(default_factory=InvoiceItem)
    str_list: typing.List[str] = Field(default_factory=list)
    int_map: "typing.Dict[str, int]" = Field(default_factory=dict)
    default_template_test: float = Field(default=1600000000.0)
""")

    def test_after_refer_message(self) -> None:
        pass

    def test_circular_references(self) -> None:
        output = getsource(demo_p2p.Invoice3)
        assert_expected_inline(output, """\
class Invoice3(BaseModel):
    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem2"] = Field(default_factory=list)
""")
        
        output = getsource(demo_p2p.InvoiceItem2)
        assert_expected_inline(output, """\
class InvoiceItem2(BaseModel):
    \"\"\"
        Test Circular references
    from: https://github.com/so1n/protobuf_to_pydantic/issues/57
    \"\"\"

    name: str = Field(default="")
    amount: int = Field(default=0)
    quantity: int = Field(default=0)
    items: typing.List["InvoiceItem2"] = Field(default_factory=list)
    invoice: Invoice3 = Field(default_factory=Invoice3)
""")

    def test_message_reference(self) -> None:
        output = getsource(demo_p2p.AnOtherMessage)
        assert_expected_inline(output, """\
class AnOtherMessage(BaseModel):
    class SubMessage(BaseModel):
        text: str = Field(default="")

    field1: str = Field(default="")
    field2: SubMessage = Field(default_factory=SubMessage)
""")

        output = getsource(demo_p2p.RootMessage)
        assert_expected_inline(output, """\
class RootMessage(BaseModel):
    \"\"\"
        Test Message references
    from: https://github.com/so1n/protobuf_to_pydantic/issues/64
    \"\"\"

    field1: str = Field(default="")
    field2: AnOtherMessage = Field(default_factory=AnOtherMessage)
""")


    def test_same_bane_inline_structure(self) -> None:
        output = getsource(demo_p2p.TestSameName0)
        assert_expected_inline(output, """\
class TestSameName0(BaseModel):
    \"\"\"
        Test inline structure of the same name
    from: https://github.com/so1n/protobuf_to_pydantic/issues/76
    \"\"\"

    class Body(BaseModel):
        input_model: str = Field(default="")
        input_info: "typing.Dict[str, str]" = Field(default_factory=dict)

    body: "TestSameName0.Body" = Field(default_factory=lambda: TestSameName0.Body())
""")
        
        output = getsource(demo_p2p.TestSameName1)
        assert_expected_inline(output, """\
class TestSameName1(BaseModel):
    class Body(BaseModel):
        output_model: str = Field(default="")
        output_info: "typing.Dict[str, str]" = Field(default_factory=dict)

    body: "TestSameName1.Body" = Field(default_factory=lambda: TestSameName1.Body())
""")

    def test_diff_pkg_refer(self) -> None:
        output = getsource(diff_pkg_refer_2_p2p.Demo2)
        assert_expected_inline(output, """\
class Demo2(BaseModel):
    myField: "typing.Dict[str, Demo1]" = Field(default_factory=dict)
""")

        # If the source code can be obtained, Demo1 can be imported normally
        output = getsource(diff_pkg_refer_2_p2p.Demo1)
        assert_expected_inline(output, """\
class Demo1(BaseModel):
    pass
""")
