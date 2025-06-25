"""
Test round-trip conversion for google.protobuf.Value.

Tests Value fields including all value types (null, number, string, bool, struct, list).
"""

from example.proto_pydanticv2.example.example_proto.demo import (
    value_demo_pb2,
    value_demo_p2p,
)
from ..common.base_test import RoundTripTestBase


class TestValue(RoundTripTestBase):
    """Test round-trip conversion for google.protobuf.Value."""

    def test_value_null(self):
        """Test Value with null."""
        proto_msg = value_demo_pb2.ValueTestMessage()
        proto_msg.dynamic_value.null_value = 0  # NULL_VALUE

        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueTestMessage)

    def test_value_number(self):
        """Test Value with numbers."""
        proto_msg = value_demo_pb2.ValueTestMessage()

        test_numbers = [
            0,
            42,
            -42,
            3.14159,
            -3.14159,
            1e10,
            1e-10,
        ]

        for number in test_numbers:
            proto_msg.Clear()
            proto_msg.dynamic_value.number_value = number

            self.verify_roundtrip(proto_msg, value_demo_p2p.ValueTestMessage)

    def test_value_string(self):
        """Test Value with strings."""
        proto_msg = value_demo_pb2.ValueTestMessage()

        test_strings = [
            "",
            "hello",
            "Hello, World!",
            "unicode: 你好世界",
            "emoji: 😀🎉",
            "special: @#$%^&*()",
            "multiline\nstring\nvalue",
        ]

        for string in test_strings:
            proto_msg.Clear()
            proto_msg.dynamic_value.string_value = string

            self.verify_roundtrip(proto_msg, value_demo_p2p.ValueTestMessage)

    def test_value_bool(self):
        """Test Value with booleans."""
        proto_msg = value_demo_pb2.ValueTestMessage()

        # Test true
        proto_msg.dynamic_value.bool_value = True
        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueTestMessage)

        # Test false
        proto_msg.Clear()
        proto_msg.dynamic_value.bool_value = False
        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueTestMessage)

    def test_value_struct(self):
        """Test Value with struct (object)."""
        proto_msg = value_demo_pb2.ValueTestMessage()

        # Simple struct
        proto_msg.dynamic_value.struct_value.fields["name"].string_value = "John"
        proto_msg.dynamic_value.struct_value.fields["age"].number_value = 30
        proto_msg.dynamic_value.struct_value.fields["active"].bool_value = True
        proto_msg.dynamic_value.struct_value.fields["email"].null_value = 0

        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueTestMessage)

    def test_value_nested_struct(self):
        """Test Value with nested struct."""
        proto_msg = value_demo_pb2.ValueTestMessage()

        # Create nested structure
        root = proto_msg.dynamic_value.struct_value
        root.fields["user"].struct_value.fields["name"].string_value = "Alice"
        root.fields["user"].struct_value.fields["id"].number_value = 123

        # Add array in struct
        scores_list = root.fields["scores"].list_value
        scores_list.values.add().number_value = 95
        scores_list.values.add().number_value = 87
        scores_list.values.add().number_value = 92

        # Add nested object in struct
        meta = root.fields["metadata"].struct_value
        meta.fields["created"].string_value = "2024-01-01"
        meta.fields["version"].number_value = 1.0

        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueTestMessage)

    def test_value_list(self):
        """Test Value with list."""
        proto_msg = value_demo_pb2.ValueTestMessage()

        # Create list with mixed types
        list_value = proto_msg.dynamic_value.list_value
        list_value.values.add().number_value = 42
        list_value.values.add().string_value = "hello"
        list_value.values.add().bool_value = True
        list_value.values.add().null_value = 0

        # Add nested object in list
        obj = list_value.values.add().struct_value
        obj.fields["key"].string_value = "value"

        # Add nested list in list
        nested_list = list_value.values.add().list_value
        nested_list.values.add().number_value = 1
        nested_list.values.add().number_value = 2
        nested_list.values.add().number_value = 3

        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueTestMessage)

    def test_value_empty_collections(self):
        """Test Value with empty struct and list."""
        proto_msg = value_demo_pb2.ValueTestMessage()

        # Empty struct
        proto_msg.dynamic_value.struct_value.CopyFrom(
            proto_msg.dynamic_value.struct_value
        )
        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueTestMessage)

        # Empty list
        proto_msg.Clear()
        proto_msg.dynamic_value.list_value.CopyFrom(proto_msg.dynamic_value.list_value)
        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueTestMessage)

    def test_value_map(self):
        """Test map with Value values."""
        proto_msg = value_demo_pb2.ValueTestMessage()

        # Add various value types to map
        proto_msg.value_map["null"].null_value = 0
        proto_msg.value_map["number"].number_value = 123.45
        proto_msg.value_map["string"].string_value = "hello"
        proto_msg.value_map["bool"].bool_value = True

        # Add struct to map
        proto_msg.value_map["object"].struct_value.fields[
            "nested"
        ].string_value = "value"

        # Add list to map
        list_val = proto_msg.value_map["array"].list_value
        list_val.values.add().number_value = 1
        list_val.values.add().number_value = 2
        list_val.values.add().number_value = 3

        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueTestMessage)

    def test_value_repeated(self):
        """Test repeated Value field."""
        proto_msg = value_demo_pb2.ValueTestMessage()

        # Add different value types to repeated field
        proto_msg.value_list.add().null_value = 0
        proto_msg.value_list.add().number_value = 42
        proto_msg.value_list.add().string_value = "test"
        proto_msg.value_list.add().bool_value = False

        # Add struct
        struct_val = proto_msg.value_list.add().struct_value
        struct_val.fields["key"].string_value = "value"

        # Add list
        list_val = proto_msg.value_list.add().list_value
        list_val.values.add().string_value = "a"
        list_val.values.add().string_value = "b"

        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueTestMessage)

    def test_value_from_pydantic_dict(self):
        """Test creating Value from Pydantic model with dict."""
        # Create Pydantic model with various value types
        pydantic_model = value_demo_p2p.ValueTestMessage(
            dynamic_value={
                "name": "Test",
                "count": 42,
                "active": True,
                "tags": ["python", "protobuf"],
                "metadata": {"version": 1.0, "author": None},
            }
        )

        # Convert to JSON then to protobuf
        json_str = self.pydantic_to_json(pydantic_model)
        proto_msg = self.json_to_protobuf(json_str, value_demo_pb2.ValueTestMessage)

        # Verify structure
        assert (
            proto_msg.dynamic_value.struct_value.fields["name"].string_value == "Test"
        )
        assert proto_msg.dynamic_value.struct_value.fields["count"].number_value == 42
        assert proto_msg.dynamic_value.struct_value.fields["active"].bool_value == True

        # Verify nested list
        tags_list = proto_msg.dynamic_value.struct_value.fields["tags"].list_value
        assert len(tags_list.values) == 2
        assert tags_list.values[0].string_value == "python"

        # Verify nested struct
        metadata = proto_msg.dynamic_value.struct_value.fields["metadata"].struct_value
        assert metadata.fields["version"].number_value == 1.0
        assert metadata.fields["author"].HasField("null_value")

    def test_value_json_representation(self):
        """Test Value JSON representation matches expected format."""
        import json

        proto_msg = value_demo_pb2.ValueTestMessage()

        # Set a struct value
        proto_msg.dynamic_value.struct_value.fields["foo"].string_value = "bar"
        proto_msg.dynamic_value.struct_value.fields["num"].number_value = 42

        # Convert to JSON
        json_str = self.protobuf_to_json(proto_msg)
        json_obj = json.loads(json_str)

        # Check the structure - dynamicValue should contain the struct as a plain object
        assert "dynamicValue" in json_obj
        assert json_obj["dynamicValue"] == {"foo": "bar", "num": 42}

    def test_value_special_float_values(self):
        """Test Value with special float values.

        Note: google.protobuf.Value doesn't support Infinity/NaN in number_value
        because these would be ambiguous with string_value in JSON.
        This is a known limitation of the protobuf Value type.
        """
        import pytest
        from google.protobuf.json_format import SerializeToJsonError

        proto_msg = value_demo_pb2.ValueTestMessage()

        # These special values are not supported by protobuf Value type
        special_values = [
            float("inf"),
            float("-inf"),
            float("nan"),
        ]

        for value in special_values:
            proto_msg.Clear()
            proto_msg.dynamic_value.number_value = value

            # Protobuf's JSON serializer will raise an error for these values
            with pytest.raises(SerializeToJsonError, match="Fail to serialize"):
                self.protobuf_to_json(proto_msg)
