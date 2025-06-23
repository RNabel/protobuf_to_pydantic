from typing import Any, Callable, Type

from google.protobuf import __version__

if __version__ > "4.0.0":
    from example.proto_pydanticv2.example.example_proto.p2p_validate_by_comment import demo_p2p  # type: ignore
else:
    from example.proto_3_20_pydanticv2.example.example_proto.p2p_validate_by_comment import demo_p2p # type: ignore

from tests.test_validate_in_runtime.test_gen_model_validate_in_runtime.test_p2p_validate import (
    BaseTestP2pModelValidator,
    local_dict,
)


def stub_func(model_class: Type, **kwargs: Any) -> Type:
    return model_class


class TestP2pModelValidator(BaseTestP2pModelValidator):
    number_model_class_list: list = [
        demo_p2p.FloatTest, demo_p2p.DoubleTest, demo_p2p.Int32Test, demo_p2p.Uint32Test,
        demo_p2p.Sfixed32Test, demo_p2p.Int64Test, demo_p2p.Sint64Test, demo_p2p.Uint64Test,
        demo_p2p.Sfixed64Test, demo_p2p.Fixed32Test, demo_p2p.Fixed64Test
    ]
    replace_message_fn: Callable = staticmethod(stub_func)  # type: ignore

    def test_bool(self) -> None:
        self._test_bool(self.replace_message_fn(demo_p2p.BoolTest, local_dict=local_dict))

    def test_string(self) -> None:
        self._test_string(self.replace_message_fn(demo_p2p.StringTest, local_dict=local_dict))

    def test_bytes(self) -> None:
        self._test_bytes(self.replace_message_fn(demo_p2p.BytesTest, local_dict=local_dict))

    def test_enum(self) -> None:
        self._test_enum(demo_p2p.EnumTest)

    def test_map(self) -> None:
        self._test_map(demo_p2p.MapTest)

    def test_repeated(self) -> None:
        self._test_repeated(demo_p2p.RepeatedTest)

    def test_any(self) -> None:
        self._test_any(demo_p2p.AnyTest)

    def test_duration(self) -> None:
        self._test_duration(demo_p2p.DurationTest)

    def test_timestamp(self) -> None:
        self._test_timestamp(demo_p2p.TimestampTest)

    def test_nested(self) -> None:
        self._test_nested(demo_p2p.NestedMessage)

    def test_one_of(self) -> None:
        self._test_one_of(demo_p2p.OneOfTest)

    def test_one_of_not(self) -> None:
        self._test_one_of_not(demo_p2p.OneOfNotTest)

    def test_one_of_optional(self) -> None:
        self._test_one_of_optional(demo_p2p.OneOfOptionalTest)

    def test_optional_message(self) -> None:
        self._test_optional_message(demo_p2p.OptionalMessage)
