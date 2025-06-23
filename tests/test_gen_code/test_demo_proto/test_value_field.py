"""Test cases for google.protobuf.Value field handling"""

from typing import Any

from expecttest import assert_expected_inline
from google.protobuf import __version__

if __version__ > "4.0.0":
    from example.proto_pydanticv2.example.example_proto.demo import value_demo_pb2
    from example.proto_pydanticv2.example.example_proto.demo import value_demo_p2p
else:
    from example.proto_3_20_pydanticv2.example.example_proto.demo import value_demo_pb2  # type: ignore[no-redef]
    from example.proto_3_20_pydanticv2.example.example_proto.demo import value_demo_p2p  # type: ignore[no-redef]

from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_code
from protobuf_to_pydantic.gen_model import clear_create_model_cache
from tests.test_gen_code.test_helper import P2CNoHeader


class TestValueField:
    @staticmethod
    def _model_output(msg: Any) -> str:
        # Make sure that the cache pool is clean before each build
        clear_create_model_cache()
        return pydantic_model_to_py_code(
            msg_to_pydantic_model(msg, parse_msg_desc_method="ignore"),
            p2c_class=P2CNoHeader,
        )

    def test_value_field_message(self) -> None:
        """Test that google.protobuf.Value fields are converted to typing.Any"""
        output = self._model_output(value_demo_pb2.ValueTestMessage)
        assert_expected_inline(
            output,
            """\
class ValueTestMessage(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        validate_by_name=True,
    )

    id: str = Field(default="", alias_priority=1, validation_alias="id", serialization_alias="id")
    dynamic_value: typing.Optional[typing.Any] = Field(
        default=None, alias_priority=1, validation_alias="dynamicValue", serialization_alias="dynamicValue"
    )
    value_list: typing.List[typing.Any] = Field(
        default_factory=list, alias_priority=1, validation_alias="valueList", serialization_alias="valueList"
    )
    value_map: typing.Dict[str, typing.Any] = Field(
        default_factory=dict, alias_priority=1, validation_alias="valueMap", serialization_alias="valueMap"
    )
""",
        )

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
                "key4": {"nested": "dict"},
            },
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

    def test_value_field_type_conversion_variations(self) -> None:
        """Test various type conversions for Value fields"""
        # Test different primitive types
        test_cases = [
            {"dynamic_value": 42},  # int
            {"dynamic_value": 3.14},  # float
            {"dynamic_value": True},  # bool
            {"dynamic_value": False},  # bool
            {"dynamic_value": None},  # null
            {"dynamic_value": "test"},  # string
            {"dynamic_value": {"key": "value"}},  # dict/struct
            {"dynamic_value": [1, 2, 3]},  # list
            {"dynamic_value": {"nested": {"deeply": {"value": 123}}}},  # nested dict
        ]

        for test_data in test_cases:
            test_data["id"] = "test"
            instance = value_demo_p2p.ValueTestMessage(**test_data)
            assert instance.dynamic_value == test_data["dynamic_value"]

    def test_value_field_json_serialization(self) -> None:
        """Test JSON serialization/deserialization of Value fields"""
        instance = value_demo_p2p.ValueTestMessage(
            id="json-test",
            dynamic_value={"complex": [1, "two", 3.0, None]},
            value_list=[{"nested": "dict"}, [1, 2], "string", None],
            value_map={
                "mixed": [True, False, None],
                "number": 42.5,
                "object": {"a": 1, "b": 2},
            },
        )

        # Convert to JSON and back
        json_dict = (
            instance.model_dump()
            if hasattr(instance, "model_dump")
            else instance.dict()
        )

        # Recreate from dict
        new_instance = value_demo_p2p.ValueTestMessage(**json_dict)

        # Verify all fields match
        assert new_instance.id == instance.id
        assert new_instance.dynamic_value == instance.dynamic_value
        assert new_instance.value_list == instance.value_list
        assert new_instance.value_map == instance.value_map

    def test_value_field_edge_cases(self) -> None:
        """Test edge cases for Value fields"""
        # Empty values
        instance1 = value_demo_p2p.ValueTestMessage(id="empty")
        assert instance1.id == "empty"
        assert instance1.value_list == []
        assert instance1.value_map == {}

        # Very nested structures
        deep_nested = {"level1": {"level2": {"level3": {"level4": {"level5": "deep"}}}}}
        instance2 = value_demo_p2p.ValueTestMessage(
            id="nested", dynamic_value=deep_nested
        )
        assert instance2.dynamic_value == deep_nested

        # Large lists
        large_list = list(range(100))
        instance3 = value_demo_p2p.ValueTestMessage(id="large", value_list=large_list)
        assert instance3.value_list == large_list
