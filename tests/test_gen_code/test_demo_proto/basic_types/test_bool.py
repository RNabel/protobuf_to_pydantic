"""
Test round-trip conversion for boolean protobuf type.

Tests bool fields including edge cases and JSON representation.
"""

from example.proto_pydanticv2.example.example_proto.demo import (
    basic_types_roundtrip_pb2,
    basic_types_roundtrip_p2p,
)
from ..common.base_test import RoundTripTestBase


class TestBooleanType(RoundTripTestBase):
    """Test round-trip conversion for boolean protobuf type."""

    def test_bool_true_roundtrip(self):
        """Test bool field with true value."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        proto_msg.bool_field = True

        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

    def test_bool_false_roundtrip(self):
        """Test bool field with false value."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        proto_msg.bool_field = False

        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

    def test_bool_default_value(self):
        """Test bool field default value (false)."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        # Don't set bool_field, it should default to false

        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

        # Verify default is false
        assert proto_msg.bool_field == False

    def test_bool_json_representation(self):
        """Test bool field JSON representation."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        # Test true
        proto_msg.bool_field = True
        json_str = self.protobuf_to_json(proto_msg)
        assert '"boolField": true' in json_str

        # Test false
        proto_msg.bool_field = False
        json_str = self.protobuf_to_json(proto_msg)
        assert '"boolField": false' in json_str

    def test_bool_with_other_fields(self):
        """Test bool field alongside other field types."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        proto_msg.bool_field = True
        proto_msg.int32_field = 42
        proto_msg.string_field = "test"
        proto_msg.float_field = 3.14

        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

    def test_repeated_bool_roundtrip(self):
        """Test repeated bool field if available."""
        # Check if the message has a repeated bool field
        if hasattr(basic_types_roundtrip_pb2.BasicTypesMessage, "repeated_bool"):
            proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
            proto_msg.repeated_bool.extend([True, False, True, True, False])

            self.verify_roundtrip(
                proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage
            )

    def test_optional_bool_roundtrip(self):
        """Test optional bool field if available."""
        # Check if the message has an optional bool field
        if hasattr(basic_types_roundtrip_pb2.BasicTypesMessage, "optional_bool"):
            # Test with value set
            proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
            proto_msg.optional_bool = True

            self.verify_roundtrip(
                proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage
            )

            # Test without value set
            proto_msg_unset = basic_types_roundtrip_pb2.BasicTypesMessage()

            self.verify_roundtrip(
                proto_msg_unset, basic_types_roundtrip_p2p.BasicTypesMessage
            )
