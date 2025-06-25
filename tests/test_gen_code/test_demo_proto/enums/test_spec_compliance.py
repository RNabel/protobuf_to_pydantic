"""
Test enum JSON serialization compliance with protobuf specification.

According to https://protobuf.dev/programming-guides/json/:
- Enums are represented as strings in JSON by default
- The name of the enum value as specified in proto is used
- Parsers accept both enum names and integer values
"""

import json
import pytest
from google.protobuf import json_format
from example.proto_pydanticv2.example.example_proto.demo import (
    enum_types_roundtrip_pb2,
    enum_types_roundtrip_p2p,
)


class TestEnumJSONSpecCompliance:
    """Test that enum serialization follows protobuf JSON specification."""

    def test_default_enum_serialization_as_string(self):
        """Per spec: enums serialize as strings by default in protobuf JSON."""
        # Create protobuf message with enum
        proto_msg = enum_types_roundtrip_pb2.EnumMessage()
        proto_msg.status = enum_types_roundtrip_pb2.Status.ACTIVE
        proto_msg.priority = enum_types_roundtrip_pb2.Priority.HIGH
        proto_msg.error_code = enum_types_roundtrip_pb2.ErrorCode.ERROR_TIMEOUT

        # Default protobuf JSON serialization
        json_str = json_format.MessageToJson(proto_msg)
        json_dict = json.loads(json_str)

        # Verify enums are serialized as strings, not integers
        assert json_dict["status"] == "ACTIVE"
        assert json_dict["priority"] == "HIGH"
        assert json_dict["errorCode"] == "ERROR_TIMEOUT"

    def test_enum_parsing_accepts_string_names(self):
        """Per spec: parsers accept enum names."""
        json_data = {
            "status": "ACTIVE",
            "priority": "HIGH",
            "errorCode": "ERROR_TIMEOUT",
        }
        json_str = json.dumps(json_data)

        # Parse into protobuf
        proto_msg = json_format.Parse(json_str, enum_types_roundtrip_pb2.EnumMessage())

        # Verify correct enum values
        assert proto_msg.status == enum_types_roundtrip_pb2.Status.ACTIVE
        assert proto_msg.priority == enum_types_roundtrip_pb2.Priority.HIGH
        assert proto_msg.error_code == enum_types_roundtrip_pb2.ErrorCode.ERROR_TIMEOUT

    def test_enum_parsing_accepts_integer_values(self):
        """Per spec: parsers accept integer values."""
        json_data = {
            "status": 1,  # ACTIVE
            "priority": 2,  # HIGH
            "errorCode": 200,  # ERROR_TIMEOUT
        }
        json_str = json.dumps(json_data)

        # Parse into protobuf
        proto_msg = json_format.Parse(json_str, enum_types_roundtrip_pb2.EnumMessage())

        # Verify correct enum values
        assert proto_msg.status == enum_types_roundtrip_pb2.Status.ACTIVE
        assert proto_msg.priority == enum_types_roundtrip_pb2.Priority.HIGH
        assert proto_msg.error_code == enum_types_roundtrip_pb2.ErrorCode.ERROR_TIMEOUT

    def test_enum_name_case_sensitive(self):
        """Verify enum names must match exactly (case sensitive)."""
        # Test lowercase - should fail
        json_str = '{"status": "active"}'
        with pytest.raises(json_format.ParseError) as exc_info:
            json_format.Parse(json_str, enum_types_roundtrip_pb2.EnumMessage())
        assert "invalid enum value" in str(exc_info.value).lower()

        # Test mixed case - should fail
        json_str = '{"status": "Active"}'
        with pytest.raises(json_format.ParseError) as exc_info:
            json_format.Parse(json_str, enum_types_roundtrip_pb2.EnumMessage())
        assert "invalid enum value" in str(exc_info.value).lower()

    def test_unknown_enum_value_handling(self):
        """Test behavior with unknown enum values."""
        # Unknown string value
        json_str = '{"status": "UNKNOWN_STATUS"}'
        with pytest.raises(json_format.ParseError):
            json_format.Parse(json_str, enum_types_roundtrip_pb2.EnumMessage())

        # Unknown integer value - protobuf actually accepts any integer
        # and stores it even if it's not a defined enum value
        json_str = '{"status": 999}'
        msg = json_format.Parse(json_str, enum_types_roundtrip_pb2.EnumMessage())
        assert msg.status == 999  # Protobuf stores unknown enum values

    def test_zero_value_default_serialization(self):
        """Test that unset enums (zero value) serialize correctly."""
        # Create message without setting enums (they default to 0)
        proto_msg = enum_types_roundtrip_pb2.EnumMessage()

        # Default JSON serialization (without always_print_fields_with_no_presence)
        json_str = json_format.MessageToJson(proto_msg)
        json_dict = json.loads(json_str)

        # By default, protobuf doesn't include unset fields in JSON
        assert json_dict == {}

        # With always_print_fields_with_no_presence=True
        json_str = json_format.MessageToJson(
            proto_msg, always_print_fields_with_no_presence=True
        )
        json_dict = json.loads(json_str)

        # Now zero values should serialize to the first enum value name
        assert json_dict["status"] == "UNKNOWN"  # Value 0
        assert json_dict["priority"] == "LOW"  # Value 0
        assert json_dict["errorCode"] == "ERROR_NONE"  # Value 0

    def test_pydantic_compatibility_with_protobuf_json(self):
        """Test that Pydantic models maintain compatibility with protobuf JSON format."""
        # Create protobuf message
        proto_msg = enum_types_roundtrip_pb2.EnumMessage()
        proto_msg.status = enum_types_roundtrip_pb2.Status.ACTIVE
        proto_msg.priority = enum_types_roundtrip_pb2.Priority.HIGH

        # Convert to default protobuf JSON (strings)
        proto_json_str = json_format.MessageToJson(proto_msg)

        # Parse with Pydantic model
        pydantic_model = enum_types_roundtrip_p2p.EnumMessage.model_validate_json(
            proto_json_str
        )

        # Verify values are correct
        assert pydantic_model.status == enum_types_roundtrip_pb2.Status.ACTIVE
        assert pydantic_model.priority == enum_types_roundtrip_pb2.Priority.HIGH

    def test_repeated_enum_json_format(self):
        """Test JSON format for repeated enum fields."""
        proto_msg = enum_types_roundtrip_pb2.EnumMessage()
        proto_msg.priority_list.extend(
            [
                enum_types_roundtrip_pb2.Priority.LOW,
                enum_types_roundtrip_pb2.Priority.HIGH,
                enum_types_roundtrip_pb2.Priority.URGENT,
            ]
        )

        # Default JSON serialization
        json_str = json_format.MessageToJson(proto_msg)
        json_dict = json.loads(json_str)

        # Repeated enums should be string array
        assert json_dict["priorityList"] == ["LOW", "HIGH", "URGENT"]

    def test_map_enum_json_format(self):
        """Test JSON format for map fields with enum values."""
        proto_msg = enum_types_roundtrip_pb2.EnumMessage()
        proto_msg.status_map["task1"] = enum_types_roundtrip_pb2.Status.ACTIVE
        proto_msg.status_map["task2"] = enum_types_roundtrip_pb2.Status.COMPLETED

        # Default JSON serialization
        json_str = json_format.MessageToJson(proto_msg)
        json_dict = json.loads(json_str)

        # Map enum values should be strings
        assert json_dict["statusMap"] == {"task1": "ACTIVE", "task2": "COMPLETED"}

    def test_optional_enum_presence(self):
        """Test optional enum field presence in JSON."""
        # Without setting optional field
        proto_msg = enum_types_roundtrip_pb2.EnumMessage()
        json_str = json_format.MessageToJson(proto_msg)
        json_dict = json.loads(json_str)

        # Optional field should not be present if not set
        assert "optionalStatus" not in json_dict

        # With optional field set
        proto_msg.optional_status = enum_types_roundtrip_pb2.Status.ACTIVE
        json_str = json_format.MessageToJson(proto_msg)
        json_dict = json.loads(json_str)

        # Now it should be present as string
        assert json_dict["optionalStatus"] == "ACTIVE"

    def test_protobuf_json_options(self):
        """Test different protobuf JSON serialization options."""
        proto_msg = enum_types_roundtrip_pb2.EnumMessage()
        proto_msg.status = enum_types_roundtrip_pb2.Status.ACTIVE

        # Test use_integers_for_enums option
        json_str_int = json_format.MessageToJson(proto_msg, use_integers_for_enums=True)
        json_dict_int = json.loads(json_str_int)
        assert json_dict_int["status"] == 1  # Integer representation

        # Test default (strings)
        json_str_default = json_format.MessageToJson(proto_msg)
        json_dict_default = json.loads(json_str_default)
        assert json_dict_default["status"] == "ACTIVE"  # String representation
