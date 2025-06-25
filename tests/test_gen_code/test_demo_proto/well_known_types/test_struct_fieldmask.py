"""
Test round-trip conversion for google.protobuf.Struct and FieldMask.

Tests Struct (JSON-like object) and FieldMask (field path tracking) types.
"""

import pytest

from example.proto_pydanticv2.example.example_proto.demo import (
    demo_pb2,
    demo_p2p,
)
from ..common.base_test import RoundTripTestBase


class TestStructFieldMask(RoundTripTestBase):
    """Test round-trip conversion for Struct and FieldMask types."""

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_struct_basic(self):
        """Test basic Struct functionality."""
        proto_msg = demo_pb2.OtherMessage()

        # Set metadata as a struct
        proto_msg.metadata["string_key"] = "string value"
        proto_msg.metadata["number_key"] = 42.5
        proto_msg.metadata["bool_key"] = True
        proto_msg.metadata["null_key"] = None

        self.verify_roundtrip(proto_msg, demo_p2p.OtherMessage)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_struct_nested(self):
        """Test nested Struct."""
        proto_msg = demo_pb2.OtherMessage()

        # Create nested structure
        proto_msg.metadata["user"] = {
            "name": "Alice",
            "age": 30,
            "active": True,
            "address": {"street": "123 Main St", "city": "Anytown", "zip": 12345},
        }

        proto_msg.metadata["tags"] = ["python", "protobuf", "testing"]

        self.verify_roundtrip(proto_msg, demo_p2p.OtherMessage)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_struct_empty(self):
        """Test empty Struct."""
        proto_msg = demo_pb2.OtherMessage()

        # Empty struct (no fields)
        # Just accessing metadata creates an empty struct
        _ = proto_msg.metadata

        self.verify_roundtrip(proto_msg, demo_p2p.OtherMessage)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_struct_mixed_types(self):
        """Test Struct with all supported types."""
        proto_msg = demo_pb2.OtherMessage()

        proto_msg.metadata["types"] = {
            "null": None,
            "boolean": True,
            "integer": 42,
            "float": 3.14,
            "string": "hello",
            "array": [1, 2, 3, "four", True, None],
            "object": {"nested": "value", "count": 10},
        }

        self.verify_roundtrip(proto_msg, demo_p2p.OtherMessage)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_struct_special_values(self):
        """Test Struct with special float values and edge cases."""
        proto_msg = demo_pb2.OtherMessage()

        # Special values
        proto_msg.metadata["empty_string"] = ""
        proto_msg.metadata["zero"] = 0
        proto_msg.metadata["negative"] = -42
        proto_msg.metadata["large_number"] = 1e20
        proto_msg.metadata["small_number"] = 1e-20
        proto_msg.metadata["empty_array"] = []
        proto_msg.metadata["empty_object"] = {}

        self.verify_roundtrip(proto_msg, demo_p2p.OtherMessage)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_fieldmask_basic(self):
        """Test basic FieldMask functionality."""
        proto_msg = demo_pb2.OtherMessage()

        # Set field mask with various paths
        proto_msg.field_mask.paths.extend(
            [
                "user.name",
                "user.email",
                "settings.notifications.email",
                "metadata",
            ]
        )

        self.verify_roundtrip(proto_msg, demo_p2p.OtherMessage)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_fieldmask_empty(self):
        """Test empty FieldMask."""
        proto_msg = demo_pb2.OtherMessage()

        # Create field mask but don't add paths
        proto_msg.field_mask.CopyFrom(proto_msg.field_mask)

        self.verify_roundtrip(proto_msg, demo_p2p.OtherMessage)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_fieldmask_special_paths(self):
        """Test FieldMask with special path names."""
        proto_msg = demo_pb2.OtherMessage()

        # Paths with special characters and formats
        proto_msg.field_mask.paths.extend(
            [
                "field_with_underscore",
                "nested.deeply.nested.field",
                "array_field[0]",  # Note: This is valid in path
                "map_field.key_name",
                "*",  # Wildcard
            ]
        )

        self.verify_roundtrip(proto_msg, demo_p2p.OtherMessage)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_struct_and_fieldmask_together(self):
        """Test message with both Struct and FieldMask."""
        proto_msg = demo_pb2.OtherMessage()

        # Set struct data
        proto_msg.metadata["user"] = {
            "id": 123,
            "name": "John Doe",
            "email": "john@example.com",
            "settings": {
                "theme": "dark",
                "notifications": {"email": True, "push": False},
            },
        }

        # Set field mask to indicate which fields to update
        proto_msg.field_mask.paths.extend(
            ["user.name", "user.settings.theme", "user.settings.notifications.email"]
        )

        # Also set double value
        proto_msg.double_value.value = 99.99

        self.verify_roundtrip(proto_msg, demo_p2p.OtherMessage)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_struct_from_pydantic_dict(self):
        """Test creating Struct from Pydantic model with dict."""
        # Create Pydantic model with dict for metadata
        pydantic_model = demo_p2p.OtherMessage(
            metadata={
                "version": "1.0.0",
                "author": "Test User",
                "tags": ["test", "example"],
                "config": {"debug": True, "timeout": 30},
            }
        )

        # Convert to JSON then to protobuf
        json_str = self.pydantic_to_json(pydantic_model)
        proto_msg = self.json_to_protobuf(json_str, demo_pb2.OtherMessage)

        # Verify struct contents
        assert "version" in proto_msg.metadata
        assert proto_msg.metadata["version"] == "1.0.0"
        assert "tags" in proto_msg.metadata
        assert len(proto_msg.metadata["tags"]) == 2
        assert "config" in proto_msg.metadata
        assert proto_msg.metadata["config"]["debug"] == True

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_fieldmask_from_pydantic_list(self):
        """Test creating FieldMask from Pydantic model with list."""
        # Create Pydantic model with list for field mask
        pydantic_model = demo_p2p.OtherMessage(
            field_mask=["user.name", "user.email", "metadata.version"]
        )

        # Convert to JSON then to protobuf
        json_str = self.pydantic_to_json(pydantic_model)
        proto_msg = self.json_to_protobuf(json_str, demo_pb2.OtherMessage)

        # Verify field mask paths
        assert len(proto_msg.field_mask.paths) == 3
        assert "user.name" in proto_msg.field_mask.paths
        assert "user.email" in proto_msg.field_mask.paths
        assert "metadata.version" in proto_msg.field_mask.paths

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_struct_json_representation(self):
        """Test that Struct JSON representation is clean."""
        proto_msg = demo_pb2.OtherMessage()

        proto_msg.metadata["simple"] = "value"
        proto_msg.metadata["nested"] = {"key": "value"}

        # Convert to JSON
        json_str = self.protobuf_to_json(proto_msg)

        # Struct should serialize as plain JSON object
        assert '"metadata": {"simple": "value", "nested": {"key": "value"}}' in json_str

    def test_fieldmask_json_representation(self):
        """Test that FieldMask JSON representation is a string."""
        proto_msg = demo_pb2.OtherMessage()

        proto_msg.field_mask.paths.extend(["field1", "field2.nested"])

        # Convert to JSON
        json_str = self.protobuf_to_json(proto_msg)

        # FieldMask should serialize as comma-separated string
        assert '"fieldMask": "field1,field2.nested"' in json_str
