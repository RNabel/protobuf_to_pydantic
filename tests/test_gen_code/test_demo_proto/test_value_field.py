"""Test cases for google.protobuf.Value field handling"""

from typing import Any

from google.protobuf import __version__

from protobuf_to_pydantic._pydantic_adapter import is_v1

if __version__ > "4.0.0":
    if is_v1:
        from example.proto_pydanticv1.example.example_proto.demo import value_demo_pb2
        from example.proto_pydanticv1.example.example_proto.demo import value_demo_p2p
    else:
        from example.proto_pydanticv2.example.example_proto.demo import value_demo_pb2  # type: ignore[no-redef]
        from example.proto_pydanticv2.example.example_proto.demo import value_demo_p2p  # type: ignore[no-redef]
else:
    if is_v1:
        from example.proto_3_20_pydanticv1.example.example_proto.demo import value_demo_pb2  # type: ignore[no-redef]
        from example.proto_3_20_pydanticv1.example.example_proto.demo import value_demo_p2p  # type: ignore[no-redef]
    else:
        from example.proto_3_20_pydanticv2.example.example_proto.demo import value_demo_pb2  # type: ignore[no-redef]
        from example.proto_3_20_pydanticv2.example.example_proto.demo import value_demo_p2p  # type: ignore[no-redef]

from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_code
from protobuf_to_pydantic.gen_model import clear_create_model_cache
from protobuf_to_pydantic.util import format_content
from tests.test_gen_code.test_helper import P2CNoHeader


class TestValueField:
    @staticmethod
    def _model_output(msg: Any) -> str:
        # Make sure that the cache pool is clean before each build
        clear_create_model_cache()
        return pydantic_model_to_py_code(msg_to_pydantic_model(msg, parse_msg_desc_method="ignore"), p2c_class=P2CNoHeader)

    def test_value_field_message(self) -> None:
        """Test that google.protobuf.Value fields are converted to typing.Any"""
        content = """
class ValueTestMessage(BaseModel):
    id: str = Field(default="")
    dynamic_value: typing.Any = Field()
    value_list: typing.List[typing.Any] = Field(default_factory=list)
    value_map: typing.Dict[str, typing.Any] = Field(default_factory=dict)
"""
        assert format_content(content) in self._model_output(value_demo_pb2.ValueTestMessage)

    def test_plugin_generated_value_field(self) -> None:
        """Test that plugin-generated code with Value fields can be instantiated"""
        # Test creating an instance with various Value types
        test_data = {
            "id": "test-123",
            "dynamic_value": "string value",  # Can be string
            "value_list": [42, "hello", True, None],  # Can be mixed types
            "value_map": {
                "key1": "value1",
                "key2": 123,
                "key3": None,
                "key4": {"nested": "dict"}
            }
        }
        
        # This should not raise any validation errors
        instance = value_demo_p2p.ValueTestMessage(**test_data)
        
        # Verify the fields are set correctly
        assert instance.id == "test-123"
        assert instance.dynamic_value == "string value"
        assert instance.value_list == [42, "hello", True, None]
        assert instance.value_map["key1"] == "value1"
        assert instance.value_map["key2"] == 123
        assert instance.value_map["key3"] is None
        assert instance.value_map["key4"] == {"nested": "dict"}