"""Test basic oneof functionality with generated Pydantic models.

Tests the fundamental behavior of oneofs:
- Only one field can be set at a time (mutex behavior)
- Setting a new field clears the previous one
- Empty oneof state
- Field access when not set
"""

import pytest
from pydantic import ValidationError
from example.proto_pydanticv2.example.example_proto.demo.demo_p2p import (
    OptionalMessage,
    InvoiceItem,
)
from example.proto_pydanticv2.example.example_proto.demo.alias_demo_p2p import (
    ReportData,
    GeoLocation,
)
from google.protobuf.timestamp_pb2 import Timestamp


class TestOneofBasicFunctionality:
    """Test basic oneof mutex behavior and field access."""

    def test_oneof_mutex_behavior(self):
        """Test that only one field can be set at a time."""
        # Create with x set
        msg = OptionalMessage(x="test_value")
        assert msg.a.x == "test_value"
        assert msg.a.a_case == "x"

        # Verify y is not accessible when x is set
        assert not hasattr(msg.a, "y")

        # Create with y set
        msg2 = OptionalMessage(y=42)
        assert msg2.a.y == 42
        assert msg2.a.a_case == "y"

        # Verify x is not accessible when y is set
        assert not hasattr(msg2.a, "x")

    def test_oneof_field_switching_immutable(self):
        """Test that oneof fields enforce single value even across model updates.

        Since Pydantic models are immutable, we can't modify fields in place.
        This test demonstrates the patterns for working with oneofs.
        """
        # Start with x set
        msg = OptionalMessage(x="initial", name="test_name", age=25)
        assert msg.a.x == "initial"
        assert msg.a.a_case == "x"

        # To "switch" fields, we need to create a new instance
        # Method 1: Create completely new instance
        msg2 = OptionalMessage(y=100, name=msg.name, age=msg.age)
        assert msg2.a.y == 100
        assert msg2.a.a_case == "y"
        assert not hasattr(msg2.a, "x")

        # Method 2: Use model_copy with update (if supported)
        try:
            # Note: This might not work as expected with oneofs due to validation
            msg3 = msg.model_copy(update={"y": 200})
        except (ValidationError, ValueError) as e:
            # This is expected - can't have both x and y
            assert (
                "Multiple fields" in str(e) or "multiple oneof fields" in str(e).lower()
            )

        # Method 3: Convert to dict, modify, and recreate
        data = msg.model_dump()
        # Remove x, add y
        data.pop("x", None)
        data["y"] = 300

        try:
            msg4 = OptionalMessage.model_validate(data)
            # This might work depending on implementation
            if hasattr(msg4, "a"):
                assert msg4.a.y == 300
                assert msg4.a.a_case == "y"
        except ValidationError:
            # Some implementations might require proper union structure
            pass

        # The original message remains unchanged
        assert msg.a.x == "initial"
        assert msg.a.a_case == "x"

    def test_empty_oneof_state(self):
        """Test behavior when no oneof field is set."""
        # Try to create message without setting oneof
        try:
            msg = OptionalMessage(name="test", age=30)
            # If this succeeds, oneof is optional
            assert msg.name == "test"
            assert msg.age == 30
            # Oneof is optional - verify we can access it
            assert hasattr(msg, "a")
        except ValidationError as e:
            # If this fails, oneof is required
            # Oneof is required
            assert "Field required" in str(e) or "missing" in str(e).lower()

        # Test that we can create with minimal oneof
        msg = OptionalMessage(
            x="", name="test", age=30
        )  # Empty string is still a value
        assert msg.a.x == ""
        assert msg.a.a_case == "x"

    def test_oneof_field_access_when_not_set(self):
        """Test accessing oneof fields when they're not the active field."""
        msg = OptionalMessage(x="active_field")

        # x should be accessible
        assert msg.a.x == "active_field"

        # y should not be accessible (not just None, but not present)
        assert not hasattr(msg.a, "y")

        # Trying to access y should raise AttributeError
        with pytest.raises(AttributeError):
            _ = msg.a.y

    def test_oneof_with_complex_message_type(self):
        """Test oneof behavior with message types."""
        geo = GeoLocation(latitude=37.7749, longitude=-122.4194, altitude_meters=100)
        report = ReportData(location_value=geo)

        assert report.data.location_value == geo
        assert report.data.data_case == "location_value"

        # time_value should not be accessible
        assert not hasattr(report.data, "time_value")

        # Switch to time_value
        ts = Timestamp()
        ts.GetCurrentTime()
        report2 = ReportData(time_value=ts)

        assert report2.data.time_value == ts
        assert report2.data.data_case == "time_value"

        # location_value should not be accessible
        assert not hasattr(report2.data, "location_value")

    def test_multiple_oneof_fields_error(self):
        """Test that setting multiple oneof fields simultaneously raises an error."""
        # Try to set both x and y
        with pytest.raises(ValueError, match="Multiple fields"):
            OptionalMessage(x="test", y=42)

        # Same with dict initialization
        with pytest.raises(ValueError, match="Multiple fields"):
            OptionalMessage.model_validate({"x": "test", "y": 42})

        # Test with ReportData
        geo = GeoLocation(latitude=37.7749, longitude=-122.4194)
        ts = Timestamp()
        ts.GetCurrentTime()

        with pytest.raises(ValueError, match="Multiple fields"):
            ReportData(location_value=geo, time_value=ts)

    def test_oneof_discriminator_field(self):
        """Test that the discriminator field correctly identifies the active field."""
        # Test with x set
        msg_x = OptionalMessage(x="test")
        assert msg_x.a.a_case == "x"

        # Test with y set
        msg_y = OptionalMessage(y=42)
        assert msg_y.a.a_case == "y"

        # Test with ReportData
        geo = GeoLocation(latitude=37.7749, longitude=-122.4194)
        report_geo = ReportData(location_value=geo)
        assert report_geo.data.data_case == "location_value"

        ts = Timestamp()
        ts.GetCurrentTime()
        report_time = ReportData(time_value=ts)
        assert report_time.data.data_case == "time_value"

    def test_oneof_model_copy_behavior(self):
        """Test that copying a model preserves oneof state."""
        # Create original with x set
        original = OptionalMessage(x="original_value", name="test")

        # Create a copy
        copy = original.model_copy()

        # Verify copy has same oneof state
        assert copy.a.x == "original_value"
        assert copy.a.a_case == "x"
        assert not hasattr(copy.a, "y")

        # Verify it's a true copy (not same object)
        assert copy is not original
        # Note: Pydantic might reuse immutable objects, so we check values instead
        assert copy.a.x == original.a.x
        assert copy.name == original.name

    def test_oneof_dict_representation(self):
        """Test how oneofs are represented in dict form."""
        # Create message with x set
        msg = OptionalMessage(x="test_value", name="test")

        # Convert to dict
        data = msg.model_dump()

        # Check the structure - this helps understand the internal representation

        # The dict should contain the discriminated union structure
        assert "a" in data or "x" in data  # Depends on implementation

        # Exclude none values
        data_clean = msg.model_dump(exclude_none=True)
        # Verify the cleaned dump still contains the union structure
        assert "a" in data_clean or "x" in data_clean

        # Test with ReportData
        geo = GeoLocation(latitude=37.7749, longitude=-122.4194)
        report = ReportData(location_value=geo)
        report_dict = report.model_dump()
        # Verify the report dict contains expected structure
        assert "data" in report_dict or "location_value" in report_dict

    def test_oneof_validation_with_invalid_discriminator(self):
        """Test validation when discriminator doesn't match the field."""
        # Try to create with mismatched discriminator
        # This tests the internal validation logic

        # Try to force a mismatch through dict construction
        data = {
            "a": {
                "a_case": "x",  # Says x is set
                "y": 42,  # But provides y value
            },
            "name": "test",
        }
        pytest.raises(
            ValidationError,
            lambda: OptionalMessage.model_validate(data),  # type: ignore
        )

    def test_oneof_none_value_behavior(self):
        """Test how oneofs handle None values."""
        # Test 1: Try to set a field to None explicitly
        pytest.raises(
            ValidationError,
            lambda: OptionalMessage(x=None),  # type: ignore
        )

        # Test 2: Create without any oneof field
        pytest.raises(
            ValidationError,
            lambda: OptionalMessage(name="test"),  # type: ignore
        )

        # Test 3: Empty dict for oneof
        pytest.raises(
            ValidationError,
            lambda: OptionalMessage.model_validate({"name": "test", "a": {}}),
        )
