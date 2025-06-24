"""
Test round-trip conversion integrity for enum types.

Focuses on verifying data integrity through the conversion cycle:
Protobuf -> JSON -> Pydantic -> JSON -> Protobuf
"""

from example.proto_pydanticv2.example.example_proto.demo import (
    enum_types_roundtrip_pb2,
    enum_types_roundtrip_p2p,
)
from .common.base_test import RoundTripTestBase


class TestEnumTypesRoundTrip(RoundTripTestBase):
    """Test round-trip conversion between Protobuf and Pydantic for enum types."""

    def test_basic_enum_roundtrip(self):
        """Test basic enum field roundtrip conversion."""
        proto_msg = enum_types_roundtrip_pb2.EnumMessage()
        proto_msg.status = enum_types_roundtrip_pb2.Status.ACTIVE
        proto_msg.priority = enum_types_roundtrip_pb2.Priority.HIGH
        proto_msg.error_code = enum_types_roundtrip_pb2.ErrorCode.ERROR_TIMEOUT
        
        self.verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.EnumMessage)

    def test_optional_enum_roundtrip(self):
        """Test optional enum field roundtrip conversion."""
        # Test with optional field set
        proto_msg = enum_types_roundtrip_pb2.EnumMessage()
        proto_msg.optional_status = enum_types_roundtrip_pb2.Status.COMPLETED
        
        self.verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.EnumMessage)
        
        # Test without optional field set
        proto_msg_empty = enum_types_roundtrip_pb2.EnumMessage()
        self.verify_roundtrip(proto_msg_empty, enum_types_roundtrip_p2p.EnumMessage)

    def test_repeated_enum_roundtrip(self):
        """Test repeated enum field roundtrip conversion."""
        proto_msg = enum_types_roundtrip_pb2.EnumMessage()
        proto_msg.priority_list.extend([
            enum_types_roundtrip_pb2.Priority.LOW,
            enum_types_roundtrip_pb2.Priority.MEDIUM,
            enum_types_roundtrip_pb2.Priority.HIGH,
            enum_types_roundtrip_pb2.Priority.URGENT,
        ])
        
        self.verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.EnumMessage)

    def test_map_enum_roundtrip(self):
        """Test map field with enum values roundtrip conversion."""
        proto_msg = enum_types_roundtrip_pb2.EnumMessage()
        proto_msg.status_map["task1"] = enum_types_roundtrip_pb2.Status.ACTIVE
        proto_msg.status_map["task2"] = enum_types_roundtrip_pb2.Status.PENDING
        proto_msg.status_map["task3"] = enum_types_roundtrip_pb2.Status.COMPLETED
        
        self.verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.EnumMessage)

    def test_complex_message_roundtrip(self):
        """Test complex message with nested enums roundtrip conversion."""
        proto_msg = enum_types_roundtrip_pb2.ComplexEnumMessage()
        
        # Set main fields
        proto_msg.primary_status = enum_types_roundtrip_pb2.Status.COMPLETED
        proto_msg.status_history.extend([
            enum_types_roundtrip_pb2.Status.PENDING,
            enum_types_roundtrip_pb2.Status.ACTIVE,
            enum_types_roundtrip_pb2.Status.COMPLETED,
        ])
        
        # Set map field
        proto_msg.task_priorities["feature1"] = enum_types_roundtrip_pb2.Priority.HIGH
        proto_msg.task_priorities["bugfix"] = enum_types_roundtrip_pb2.Priority.URGENT
        
        # Set optional field
        proto_msg.last_error = enum_types_roundtrip_pb2.ErrorCode.ERROR_NONE
        
        # Set nested message
        proto_msg.nested.nested_status = enum_types_roundtrip_pb2.Status.ACTIVE
        proto_msg.nested.nested_priority = enum_types_roundtrip_pb2.Priority.HIGH
        
        # Add to nested list
        nested_item = proto_msg.nested_list.add()
        nested_item.nested_status = enum_types_roundtrip_pb2.Status.PENDING
        nested_item.nested_priority = enum_types_roundtrip_pb2.Priority.LOW
        
        self.verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.ComplexEnumMessage)

    def test_all_enum_values_roundtrip(self):
        """Test that all enum values can complete roundtrip."""
        # Test all Status values
        for status in enum_types_roundtrip_pb2.Status.values():
            proto_msg = enum_types_roundtrip_pb2.EnumMessage()
            proto_msg.status = status
            self.verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.EnumMessage)
        
        # Test all Priority values
        for priority in enum_types_roundtrip_pb2.Priority.values():
            proto_msg = enum_types_roundtrip_pb2.EnumMessage()
            proto_msg.priority = priority
            self.verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.EnumMessage)
        
        # Test all ErrorCode values (non-consecutive)
        for error_code in enum_types_roundtrip_pb2.ErrorCode.values():
            proto_msg = enum_types_roundtrip_pb2.EnumMessage()
            proto_msg.error_code = error_code
            self.verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.EnumMessage)

    def test_pydantic_to_protobuf_roundtrip(self):
        """Test roundtrip starting from Pydantic model."""
        # Create Pydantic model
        pydantic_model = enum_types_roundtrip_p2p.EnumMessage(
            status=enum_types_roundtrip_pb2.Status.ACTIVE,
            priority=enum_types_roundtrip_pb2.Priority.HIGH,
            error_code=enum_types_roundtrip_pb2.ErrorCode.ERROR_TIMEOUT,
            priority_list=[
                enum_types_roundtrip_pb2.Priority.LOW,
                enum_types_roundtrip_pb2.Priority.URGENT,
            ],
            status_map={
                "task1": enum_types_roundtrip_pb2.Status.PENDING,
                "task2": enum_types_roundtrip_pb2.Status.COMPLETED,
            }
        )
        
        # Convert to JSON
        json_str = self.pydantic_to_json(pydantic_model)
        
        # Parse to protobuf
        proto_msg = self.json_to_protobuf(json_str, enum_types_roundtrip_pb2.EnumMessage)
        
        # Convert back to JSON
        proto_json = self.protobuf_to_json(proto_msg)
        
        # Parse back to Pydantic
        pydantic_model_2 = self.json_to_pydantic(
            proto_json, enum_types_roundtrip_p2p.EnumMessage
        )
        
        # Verify values match
        assert pydantic_model.status == pydantic_model_2.status
        assert pydantic_model.priority == pydantic_model_2.priority
        assert pydantic_model.error_code == pydantic_model_2.error_code
        assert pydantic_model.priority_list == pydantic_model_2.priority_list
        assert pydantic_model.status_map == pydantic_model_2.status_map