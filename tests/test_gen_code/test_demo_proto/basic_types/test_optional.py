"""
Test round-trip conversion for optional protobuf fields.

Tests proto3 optional field presence and serialization behavior.
"""

from example.proto_pydanticv2.example.example_proto.demo import (
    basic_types_roundtrip_pb2,
    basic_types_roundtrip_p2p,
    demo_pb2,
    demo_p2p,
)
from ..common.base_test import RoundTripTestBase


class TestOptionalFields(RoundTripTestBase):
    """Test round-trip conversion for proto3 optional fields."""

    def test_optional_int32_set(self):
        """Test optional int32 field with value set."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        proto_msg.optional_int32 = 42
        
        self.verify_roundtrip(
            proto_msg,
            basic_types_roundtrip_p2p.BasicTypesMessage
        )

    def test_optional_int32_unset(self):
        """Test optional int32 field without value set."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        # Don't set optional_int32
        
        self.verify_roundtrip(
            proto_msg,
            basic_types_roundtrip_p2p.BasicTypesMessage
        )

    def test_optional_int32_zero(self):
        """Test optional int32 field explicitly set to zero."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        proto_msg.optional_int32 = 0
        
        # Zero should be serialized for optional fields
        json_str = self.protobuf_to_json(proto_msg)
        assert '"optionalInt32": 0' in json_str
        
        self.verify_roundtrip(
            proto_msg,
            basic_types_roundtrip_p2p.BasicTypesMessage
        )

    def test_optional_string_set(self):
        """Test optional string field with value set."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        proto_msg.optional_string = "hello"
        
        self.verify_roundtrip(
            proto_msg,
            basic_types_roundtrip_p2p.BasicTypesMessage
        )

    def test_optional_string_empty(self):
        """Test optional string field set to empty string."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        proto_msg.optional_string = ""
        
        # Empty string should be serialized for optional fields
        json_str = self.protobuf_to_json(proto_msg)
        assert '"optionalString": ""' in json_str
        
        self.verify_roundtrip(
            proto_msg,
            basic_types_roundtrip_p2p.BasicTypesMessage
        )

    def test_optional_string_unset(self):
        """Test optional string field without value set."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        # Don't set optional_string
        
        self.verify_roundtrip(
            proto_msg,
            basic_types_roundtrip_p2p.BasicTypesMessage
        )

    def test_optional_bool_true(self):
        """Test optional bool field set to true."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        proto_msg.optional_bool = True
        
        self.verify_roundtrip(
            proto_msg,
            basic_types_roundtrip_p2p.BasicTypesMessage
        )

    def test_optional_bool_false(self):
        """Test optional bool field explicitly set to false."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        proto_msg.optional_bool = False
        
        # False should be serialized for optional fields
        json_str = self.protobuf_to_json(proto_msg)
        assert '"optionalBool": false' in json_str
        
        self.verify_roundtrip(
            proto_msg,
            basic_types_roundtrip_p2p.BasicTypesMessage
        )

    def test_optional_bool_unset(self):
        """Test optional bool field without value set."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        # Don't set optional_bool
        
        self.verify_roundtrip(
            proto_msg,
            basic_types_roundtrip_p2p.BasicTypesMessage
        )

    def test_multiple_optional_fields(self):
        """Test message with multiple optional fields."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        
        # Set some optional fields, leave others unset
        proto_msg.optional_int32 = 100
        # optional_string is not set
        proto_msg.optional_bool = True
        
        # Also set some regular fields
        proto_msg.int32_field = 42
        proto_msg.string_field = "regular"
        
        self.verify_roundtrip(
            proto_msg,
            basic_types_roundtrip_p2p.BasicTypesMessage
        )

    def test_optional_field_presence_in_json(self):
        """Test that optional field presence is correctly reflected in JSON."""
        # Create two messages
        msg_with_optional = basic_types_roundtrip_pb2.BasicTypesMessage()
        msg_without_optional = basic_types_roundtrip_pb2.BasicTypesMessage()
        
        # Set optional field in one message
        msg_with_optional.optional_int32 = 0
        
        # Convert to JSON
        json_with = self.protobuf_to_json(msg_with_optional)
        json_without = self.protobuf_to_json(msg_without_optional)
        
        # The JSON should be different
        assert json_with != json_without
        assert '"optionalInt32": 0' in json_with
        assert '"optionalInt32"' not in json_without

    def test_optional_message_field(self):
        """Test optional message field if available."""
        proto_msg = demo_pb2.OptionalMessage()
        
        # Test with optional message field set
        proto_msg.item.name = "test item"
        proto_msg.item.amount = 100
        
        self.verify_roundtrip(
            proto_msg,
            demo_p2p.OptionalMessage
        )
        
        # Test without optional message field set
        proto_msg_unset = demo_pb2.OptionalMessage()
        proto_msg_unset.name = "test"  # Set other fields
        proto_msg_unset.age = 30
        
        self.verify_roundtrip(
            proto_msg_unset,
            demo_p2p.OptionalMessage
        )

    def test_has_presence_check(self):
        """Test HasField functionality for optional fields."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        
        # Check field is not present initially
        assert not proto_msg.HasField("optional_int32")
        
        # Set field to zero
        proto_msg.optional_int32 = 0
        
        # Now field should be present
        assert proto_msg.HasField("optional_int32")
        
        # Clear the field
        proto_msg.ClearField("optional_int32")
        
        # Field should not be present again
        assert not proto_msg.HasField("optional_int32")