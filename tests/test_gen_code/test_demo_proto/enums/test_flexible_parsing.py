"""
Test FlexibleEnumMixin functionality for flexible enum parsing.

Tests the custom enum parsing behavior that allows:
- Enum members (Status.ACTIVE)
- String names ("ACTIVE")
- Integer values (1)
"""

import pytest
from pydantic import ValidationError
from example.proto_pydanticv2.example.example_proto.demo import enum_types_roundtrip_p2p


class TestFlexibleEnumParsing:
    """Test FlexibleEnumMixin behavior for flexible enum validation."""

    def test_accepts_enum_member_directly(self):
        """Test that enum members are accepted as-is."""
        model = enum_types_roundtrip_p2p.EnumMessage(
            status=enum_types_roundtrip_p2p.Status.ACTIVE,
            priority=enum_types_roundtrip_p2p.Priority.HIGH,
            error_code=enum_types_roundtrip_p2p.ErrorCode.ERROR_TIMEOUT,
        )

        assert model.status == enum_types_roundtrip_p2p.Status.ACTIVE
        assert model.priority == enum_types_roundtrip_p2p.Priority.HIGH
        assert model.error_code == enum_types_roundtrip_p2p.ErrorCode.ERROR_TIMEOUT

    def test_accepts_string_names(self):
        """Test that string enum names are converted to enum values."""
        model = enum_types_roundtrip_p2p.EnumMessage(
            status="ACTIVE", priority="HIGH", error_code="ERROR_TIMEOUT"
        )

        assert model.status == enum_types_roundtrip_p2p.Status.ACTIVE
        assert model.priority == enum_types_roundtrip_p2p.Priority.HIGH
        assert model.error_code == enum_types_roundtrip_p2p.ErrorCode.ERROR_TIMEOUT

    def test_accepts_integer_values(self):
        """Test that integer values are converted to enum values."""
        model = enum_types_roundtrip_p2p.EnumMessage(
            status=1,  # ACTIVE
            priority=2,  # HIGH
            error_code=200,  # ERROR_TIMEOUT
        )

        assert model.status == enum_types_roundtrip_p2p.Status.ACTIVE
        assert model.priority == enum_types_roundtrip_p2p.Priority.HIGH
        assert model.error_code == enum_types_roundtrip_p2p.ErrorCode.ERROR_TIMEOUT

    def test_string_name_case_sensitive(self):
        """Test that string names must match exactly."""
        # Lowercase should fail
        with pytest.raises(ValidationError) as exc_info:
            enum_types_roundtrip_p2p.EnumMessage(status="active")
        assert "'active' is not a valid name" in str(exc_info.value)

        # Mixed case should fail
        with pytest.raises(ValidationError) as exc_info:
            enum_types_roundtrip_p2p.EnumMessage(status="Active")
        assert "'Active' is not a valid name" in str(exc_info.value)

    def test_invalid_string_name(self):
        """Test that invalid string names raise appropriate errors."""
        with pytest.raises(ValidationError) as exc_info:
            enum_types_roundtrip_p2p.EnumMessage(status="INVALID_STATUS")
        assert "'INVALID_STATUS' is not a valid name for Status" in str(exc_info.value)

    def test_invalid_integer_value(self):
        """Test that invalid integer values raise appropriate errors."""
        with pytest.raises(ValidationError) as exc_info:
            enum_types_roundtrip_p2p.EnumMessage(status=999)
        assert "999 is not a valid Status" in str(exc_info.value)

    def test_none_value_rejected(self):
        """Test that None values are properly rejected for required fields."""
        with pytest.raises(ValidationError):
            enum_types_roundtrip_p2p.EnumMessage(status=None)

    def test_optional_enum_with_flexible_parsing(self):
        """Test flexible parsing works with optional enum fields."""
        # Test with string
        model1 = enum_types_roundtrip_p2p.EnumMessage(optional_status="ACTIVE")
        assert model1.optional_status == enum_types_roundtrip_p2p.Status.ACTIVE

        # Test with integer
        model2 = enum_types_roundtrip_p2p.EnumMessage(optional_status=1)
        assert model2.optional_status == enum_types_roundtrip_p2p.Status.ACTIVE

        # Test with enum member
        model3 = enum_types_roundtrip_p2p.EnumMessage(
            optional_status=enum_types_roundtrip_p2p.Status.ACTIVE
        )
        assert model3.optional_status == enum_types_roundtrip_p2p.Status.ACTIVE

    def test_repeated_enum_with_flexible_parsing(self):
        """Test flexible parsing works with repeated enum fields."""
        model = enum_types_roundtrip_p2p.EnumMessage(
            priority_list=[
                "LOW",  # String
                1,  # Integer (MEDIUM)
                enum_types_roundtrip_p2p.Priority.HIGH,  # Enum member
                "URGENT",  # String
            ]
        )

        expected = [
            enum_types_roundtrip_p2p.Priority.LOW,
            enum_types_roundtrip_p2p.Priority.MEDIUM,
            enum_types_roundtrip_p2p.Priority.HIGH,
            enum_types_roundtrip_p2p.Priority.URGENT,
        ]
        assert model.priority_list == expected

    def test_map_enum_with_flexible_parsing(self):
        """Test flexible parsing works with map fields containing enum values."""
        model = enum_types_roundtrip_p2p.EnumMessage(
            status_map={
                "task1": "ACTIVE",  # String
                "task2": 3,  # Integer (PENDING)
                "task3": enum_types_roundtrip_p2p.Status.COMPLETED,  # Enum member
            }
        )

        expected = {
            "task1": enum_types_roundtrip_p2p.Status.ACTIVE,
            "task2": enum_types_roundtrip_p2p.Status.PENDING,
            "task3": enum_types_roundtrip_p2p.Status.COMPLETED,
        }
        assert model.status_map == expected

    def test_nested_message_enum_flexible_parsing(self):
        """Test flexible parsing in nested messages."""
        model = enum_types_roundtrip_p2p.ComplexEnumMessage(
            primary_status="ACTIVE",
            nested={
                "nested_status": 1,  # ACTIVE as integer
                "nested_priority": "HIGH",  # String
            },
        )

        assert model.primary_status == enum_types_roundtrip_p2p.Status.ACTIVE
        assert model.nested.nested_status == enum_types_roundtrip_p2p.Status.ACTIVE
        assert model.nested.nested_priority == enum_types_roundtrip_p2p.Priority.HIGH

    def test_json_validation_with_flexible_parsing(self):
        """Test that flexible parsing works when validating from JSON."""
        json_data = {
            "status": "ACTIVE",  # String
            "priority": 2,  # Integer (HIGH)
            "errorCode": "ERROR_TIMEOUT",  # String
            "priorityList": ["LOW", 3, "HIGH"],  # Mixed
            "statusMap": {
                "task1": "PENDING",
                "task2": 4,  # COMPLETED
            },
        }

        model = enum_types_roundtrip_p2p.EnumMessage.model_validate(json_data)

        assert model.status == enum_types_roundtrip_p2p.Status.ACTIVE
        assert model.priority == enum_types_roundtrip_p2p.Priority.HIGH
        assert model.error_code == enum_types_roundtrip_p2p.ErrorCode.ERROR_TIMEOUT
        assert len(model.priority_list) == 3
        assert model.status_map["task1"] == enum_types_roundtrip_p2p.Status.PENDING
        assert model.status_map["task2"] == enum_types_roundtrip_p2p.Status.COMPLETED

    def test_non_consecutive_enum_values(self):
        """Test flexible parsing with non-consecutive enum values."""
        # ErrorCode has non-consecutive values: 0, 100, 200, 500, 999
        test_cases = [
            ("ERROR_NONE", 0),
            ("ERROR_INVALID_INPUT", 100),
            ("ERROR_TIMEOUT", 200),
            ("ERROR_INTERNAL", 500),
            ("ERROR_UNKNOWN", 999),
        ]

        for name, value in test_cases:
            # Test with string name
            model1 = enum_types_roundtrip_p2p.EnumMessage(error_code=name)
            assert model1.error_code.value == value

            # Test with integer value
            model2 = enum_types_roundtrip_p2p.EnumMessage(error_code=value)
            assert model2.error_code.name == name

    def test_serialization_maintains_integer_format(self):
        """Test that serialization still uses integers for protobuf compatibility."""
        model = enum_types_roundtrip_p2p.EnumMessage(
            status="ACTIVE",  # Provided as string
            priority=2,  # Provided as integer
            error_code=enum_types_roundtrip_p2p.ErrorCode.ERROR_TIMEOUT,  # Enum member
        )

        # Serialize to dict
        data = model.model_dump()

        assert data["status"] == enum_types_roundtrip_p2p.Status.ACTIVE
        assert data["priority"] == enum_types_roundtrip_p2p.Priority.HIGH
        assert data["error_code"] == enum_types_roundtrip_p2p.ErrorCode.ERROR_TIMEOUT

        # JSON serialization should also use integers
        import json

        json_str = model.model_dump_json(by_alias=True)
        json_data = json.loads(json_str)
        assert json_data["status"] == "ACTIVE"
        assert json_data["priority"] == "HIGH"
        assert json_data["errorCode"] == "ERROR_TIMEOUT"  # Note: camelCase due to alias
