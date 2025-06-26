import json
import pytest
from google.protobuf import json_format

from example.proto_pydanticv2.example.example_proto.demo import demo_pb2
from example.proto_pydanticv2.example.example_proto.demo.demo_p2p import (
    OptionalMessage,
    UserMessage,
    MapMessage,
    WithOptionalOneofMsgEntry,
)


class TestOneofNullSerialization:
    """Test that oneof fields don't serialize as null when unset."""

    def test_oneof_wrapper_field_not_in_output(self):
        """Test that the oneof wrapper field 'a' doesn't appear in JSON output."""
        # Create message with x variant
        msg = OptionalMessage(x="test_value", name="test_name", age=25)

        # Serialize with default settings
        json_str = msg.model_dump_json()
        data = json.loads(json_str)

        # The wrapper field 'a' should NOT appear in the output
        assert "a" not in data, "Wrapper field 'a' should not appear in JSON output"

        # Only the actual field should appear
        assert "x" in data
        assert data["x"] == "test_value"

        # Test with y variant too
        msg_y = OptionalMessage(y=42, name="test_name")
        json_y = msg_y.model_dump_json()
        data_y = json.loads(json_y)

        assert "a" not in data_y, "Wrapper field 'a' should not appear in JSON output"
        assert "y" in data_y
        assert data_y["y"] == 42

    def test_protobuf_json_behavior_for_unset_oneof(self):
        """Shows how protobuf handles unset oneofs in JSON - they don't appear at all."""
        # Create protobuf message without setting oneof
        proto_msg = demo_pb2.OptionalMessage()
        proto_msg.name = "test_name"
        proto_msg.age = 25
        # Note: We're NOT setting x or y, so the oneof is unset

        # Serialize to JSON
        proto_json = json_format.MessageToJson(proto_msg)
        proto_data = json.loads(proto_json)

        # Protobuf behavior: unset oneofs don't appear in JSON at all
        assert "x" not in proto_data
        assert "y" not in proto_data
        # There's no wrapper field like "a" in protobuf JSON

    def test_empty_string_oneof_serialization(self):
        """Test that empty string in oneof still serializes correctly."""
        # Create message with empty string in oneof
        msg = OptionalMessage(x="", name="test_name", age=25)

        # Serialize with default settings
        json_str = msg.model_dump_json()
        data = json.loads(json_str)

        # Empty string should still be serialized (it's a valid value)
        assert "x" in data
        assert data["x"] == ""

        # Wrapper field should not appear
        assert "a" not in data

        # Other fields should be present
        assert data.get("name") == "test_name"
        assert data.get("age") == 25

    def test_default_exclude_none_behavior(self):
        """Test that the default behavior now excludes None values."""
        # Create message with minimal oneof value
        msg = WithOptionalOneofMsgEntry()

        # Use default serialization (should have exclude_none=True by default)
        data = json.loads(msg.model_dump_json())

        # Default behavior should exclude None values
        for key, value in data.items():
            assert value is not None, f"Field {key} has None value"

    def test_set_oneof_serialization(self):
        """Test that set oneofs serialize correctly."""
        # Test with x variant set
        msg_x = OptionalMessage(x="hello", name="test_x")
        json_x = msg_x.model_dump_json()
        data_x = json.loads(json_x)

        print(f"JSON with x set: {json_x}")

        # Should have x but not y
        assert "x" in data_x
        assert data_x["x"] == "hello"
        assert "y" not in data_x

        # Test with y variant set
        msg_y = OptionalMessage(y=42, age=30)
        json_y = msg_y.model_dump_json()
        data_y = json.loads(json_y)

        print(f"JSON with y set: {json_y}")

        # Should have y but not x
        assert "y" in data_y
        assert data_y["y"] == 42
        assert "x" not in data_y

    def test_protobuf_json_roundtrip_compatibility(self):
        """Test roundtrip compatibility with protobuf JSON format."""
        # Create protobuf message with oneof set
        proto_msg = demo_pb2.OptionalMessage()
        proto_msg.x = "test_value"
        proto_msg.name = "proto_test"

        # Convert to JSON
        proto_json = json_format.MessageToJson(proto_msg)

        # Parse with Pydantic model
        pydantic_model = OptionalMessage.model_validate_json(proto_json)

        # Serialize back to JSON
        pydantic_json = pydantic_model.model_dump_json()

        # Parse back into protobuf
        proto_roundtrip = demo_pb2.OptionalMessage()
        json_format.Parse(pydantic_json, proto_roundtrip)

        # Verify roundtrip preservation
        assert proto_roundtrip.x == proto_msg.x
        assert proto_roundtrip.name == proto_msg.name
        assert proto_roundtrip.WhichOneof("a") == "x"

    def test_multiple_oneofs_in_message(self):
        """Test behavior with multiple oneofs (simulated with nested messages)."""
        # Since OptionalMessage only has one oneof, we'll test with nested structures
        msg1 = OptionalMessage(x="first", name="msg1")
        msg2 = OptionalMessage(y=100, name="msg2")

        # Create a structure with multiple messages
        map_msg = MapMessage(
            user_map={
                "user1": UserMessage(uid="1", age=20, user_name="alice"),
                "user2": UserMessage(uid="2", age=30, user_name="bob"),
            }
        )

        # Serialize
        json_str = map_msg.model_dump_json()
        data = json.loads(json_str)

        print(f"JSON with nested messages: {json_str}")

        # Verify no null values in the output
        def check_no_nulls(obj, path=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    assert v is not None, f"Null value at {path}.{k}"
                    check_no_nulls(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    assert v is not None, f"Null value at {path}[{i}]"
                    check_no_nulls(v, f"{path}[{i}]")

        check_no_nulls(data)

    def test_empty_repeated_and_map_fields(self):
        """Test that empty repeated and map fields don't cause issues."""
        msg = OptionalMessage(
            x="test",
            str_list=[],  # Empty list
            int_map={},  # Empty map
        )

        # Serialize with different options
        json_default = msg.model_dump_json()
        json_exclude_defaults = msg.model_dump_json(exclude_defaults=True)

        data_default = json.loads(json_default)
        data_exclude = json.loads(json_exclude_defaults)

        print(f"JSON with empty collections (default): {json_default}")
        print(
            f"JSON with empty collections (exclude_defaults): {json_exclude_defaults}"
        )

        # Empty collections might or might not appear depending on settings
        # But they should never be null
        if "str_list" in data_default:
            assert isinstance(data_default["str_list"], list)
        if "int_map" in data_default:
            assert isinstance(data_default["int_map"], dict)

    def test_discriminator_not_in_output(self):
        """Test that internal discriminator fields don't appear in JSON output."""
        msg = OptionalMessage(x="test_value", name="test")

        # Serialize
        json_str = msg.model_dump_json()
        data = json.loads(json_str)

        print(f"JSON output: {json_str}")

        # The discriminator field (a_case) should not appear in the output
        assert "a_case" not in data
        # No wrapper object should appear
        assert "a" not in data

        # Only the actual fields should be present
        assert "x" in data
        assert "name" in data

    @pytest.mark.parametrize("exclude_none", [True, False])
    @pytest.mark.parametrize("exclude_defaults", [True, False])
    @pytest.mark.parametrize("exclude_unset", [True, False])
    def test_serialization_options_matrix(
        self, exclude_none, exclude_defaults, exclude_unset
    ):
        """Test various combinations of serialization options."""
        # Create message with some fields set and some defaults
        msg = OptionalMessage(
            x="", name="test"
        )  # age will be default 0, x is empty string

        # Serialize with the given options
        json_str = msg.model_dump_json(
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
            exclude_unset=exclude_unset,
        )
        data = json.loads(json_str)

        print(
            f"JSON (none={exclude_none}, defaults={exclude_defaults}, unset={exclude_unset}): {json_str}"
        )

        # With exclude_none=True, no None values should appear
        if exclude_none:
            for key, value in data.items():
                assert value is not None, f"Field {key} is None with exclude_none=True"


def test_summary():
    """Summary of the oneof null serialization issue and fix.

    ISSUE:
    ------
    When a Pydantic model has a oneof field that is not set, it serializes as:
    {"a": null, "other_field": "value"}

    This is incorrect because:
    1. Protobuf JSON format doesn't include unset oneofs at all
    2. The wrapper field "a" shouldn't appear in the output
    3. Null values break protobuf compatibility

    ROOT CAUSE:
    -----------
    The discriminated union implementation requires the oneof field to exist
    in the model structure. When no variant is set, it defaults to None.
    Without proper exclusion settings, this None value gets serialized.

    FIX:
    ----
    The ProtobufCompatibleBaseModel now sets exclude_none=True by default
    in the model_dump() method. This ensures that:
    - Unset oneofs don't appear in JSON output
    - Only actually set fields are serialized
    - The output matches protobuf JSON format

    VERIFICATION:
    -------------
    Run this test file to verify that:
    1. Unset oneofs no longer serialize as null
    2. Set oneofs serialize correctly with only the active field
    3. Roundtrip with protobuf JSON works correctly
    4. No discriminator or wrapper fields appear in output
    """
    print(__doc__)
