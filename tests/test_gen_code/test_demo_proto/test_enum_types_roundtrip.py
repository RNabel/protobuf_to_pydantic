"""
Test round-trip conversion integrity for enum types.

Focuses on verifying data integrity through the conversion cycle:
Protobuf -> JSON -> Pydantic -> JSON -> Protobuf
"""

import json
from typing import Any

from google.protobuf import json_format
from google.protobuf.message import Message
from pydantic import BaseModel

from example.proto_pydanticv2.example.example_proto.demo import (
    enum_types_roundtrip_pb2,
    enum_types_roundtrip_p2p,
)


class TestEnumTypesRoundTrip:
    """Test round-trip conversion between Protobuf and Pydantic for enum types."""

    @staticmethod
    def _protobuf_to_json(msg: Message) -> str:
        """Convert protobuf message to JSON string."""
        return json_format.MessageToJson(
            msg, always_print_fields_with_no_presence=True, use_integers_for_enums=True
        )

    @staticmethod
    def _json_to_protobuf(json_str: str, msg_class: Any) -> Message:
        """Convert JSON string to protobuf message."""
        msg = msg_class()
        json_format.Parse(json_str, msg)
        return msg

    @staticmethod
    def _pydantic_to_json(model: BaseModel) -> str:
        """Convert Pydantic model to JSON string."""
        return model.model_dump_json(by_alias=True)

    @staticmethod
    def _json_to_pydantic(json_str: str, model_class: type[BaseModel]) -> BaseModel:
        """Convert JSON string to Pydantic model."""
        return model_class.model_validate_json(json_str)

    def _verify_roundtrip(
        self, proto_msg: Message, pydantic_model_class: type[BaseModel]
    ) -> None:
        """Verify that data survives the complete roundtrip."""
        # Step 1: Protobuf -> JSON
        proto_json = self._protobuf_to_json(proto_msg)
        
        # Step 2: JSON -> Pydantic
        pydantic_model = self._json_to_pydantic(proto_json, pydantic_model_class)
        
        # Step 3: Pydantic -> JSON
        pydantic_json = self._pydantic_to_json(pydantic_model)
        
        # Step 4: JSON -> Protobuf
        reconstructed_msg = self._json_to_protobuf(pydantic_json, type(proto_msg))
        
        # Verify the round trip was successful
        final_json = self._protobuf_to_json(reconstructed_msg)
        
        # Compare JSONs
        original_dict = json.loads(proto_json)
        final_dict = json.loads(final_json)
        
        # Handle optional fields
        msg_descriptor = proto_msg.DESCRIPTOR
        optional_fields = set()
        
        for field in msg_descriptor.fields:
            if field.has_presence:
                json_name = field.json_name if hasattr(field, "json_name") else field.name
                optional_fields.add(json_name)
        
        for key in list(final_dict.keys()):
            if key not in original_dict and key in optional_fields:
                final_dict.pop(key)
        
        assert original_dict == final_dict, (
            f"Round-trip failed:\nOriginal: {original_dict}\nFinal: {final_dict}"
        )

    def test_basic_enum_roundtrip(self):
        """Test basic enum field roundtrip conversion."""
        proto_msg = enum_types_roundtrip_pb2.EnumMessage()
        proto_msg.status = enum_types_roundtrip_pb2.Status.ACTIVE
        proto_msg.priority = enum_types_roundtrip_pb2.Priority.HIGH
        proto_msg.error_code = enum_types_roundtrip_pb2.ErrorCode.ERROR_TIMEOUT
        
        self._verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.EnumMessage)

    def test_optional_enum_roundtrip(self):
        """Test optional enum field roundtrip conversion."""
        # Test with optional field set
        proto_msg = enum_types_roundtrip_pb2.EnumMessage()
        proto_msg.optional_status = enum_types_roundtrip_pb2.Status.COMPLETED
        
        self._verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.EnumMessage)
        
        # Test without optional field set
        proto_msg_empty = enum_types_roundtrip_pb2.EnumMessage()
        self._verify_roundtrip(proto_msg_empty, enum_types_roundtrip_p2p.EnumMessage)

    def test_repeated_enum_roundtrip(self):
        """Test repeated enum field roundtrip conversion."""
        proto_msg = enum_types_roundtrip_pb2.EnumMessage()
        proto_msg.priority_list.extend([
            enum_types_roundtrip_pb2.Priority.LOW,
            enum_types_roundtrip_pb2.Priority.MEDIUM,
            enum_types_roundtrip_pb2.Priority.HIGH,
            enum_types_roundtrip_pb2.Priority.URGENT,
        ])
        
        self._verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.EnumMessage)

    def test_map_enum_roundtrip(self):
        """Test map field with enum values roundtrip conversion."""
        proto_msg = enum_types_roundtrip_pb2.EnumMessage()
        proto_msg.status_map["task1"] = enum_types_roundtrip_pb2.Status.ACTIVE
        proto_msg.status_map["task2"] = enum_types_roundtrip_pb2.Status.PENDING
        proto_msg.status_map["task3"] = enum_types_roundtrip_pb2.Status.COMPLETED
        
        self._verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.EnumMessage)

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
        
        self._verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.ComplexEnumMessage)

    def test_all_enum_values_roundtrip(self):
        """Test that all enum values can complete roundtrip."""
        # Test all Status values
        for status in enum_types_roundtrip_pb2.Status.values():
            proto_msg = enum_types_roundtrip_pb2.EnumMessage()
            proto_msg.status = status
            self._verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.EnumMessage)
        
        # Test all Priority values
        for priority in enum_types_roundtrip_pb2.Priority.values():
            proto_msg = enum_types_roundtrip_pb2.EnumMessage()
            proto_msg.priority = priority
            self._verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.EnumMessage)
        
        # Test all ErrorCode values (non-consecutive)
        for error_code in enum_types_roundtrip_pb2.ErrorCode.values():
            proto_msg = enum_types_roundtrip_pb2.EnumMessage()
            proto_msg.error_code = error_code
            self._verify_roundtrip(proto_msg, enum_types_roundtrip_p2p.EnumMessage)

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
        json_str = self._pydantic_to_json(pydantic_model)
        
        # Parse to protobuf
        proto_msg = self._json_to_protobuf(json_str, enum_types_roundtrip_pb2.EnumMessage)
        
        # Convert back to JSON
        proto_json = self._protobuf_to_json(proto_msg)
        
        # Parse back to Pydantic
        pydantic_model_2 = self._json_to_pydantic(
            proto_json, enum_types_roundtrip_p2p.EnumMessage
        )
        
        # Verify values match
        assert pydantic_model.status == pydantic_model_2.status
        assert pydantic_model.priority == pydantic_model_2.priority
        assert pydantic_model.error_code == pydantic_model_2.error_code
        assert pydantic_model.priority_list == pydantic_model_2.priority_list
        assert pydantic_model.status_map == pydantic_model_2.status_map