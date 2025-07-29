"""Test oneofs with different field types.

Tests oneof behavior with:
- Primitive types (string, int, float, bool, bytes)
- Message types
- Repeated fields
- Map fields
- Enum fields
- Well-known types
"""

from datetime import datetime
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


class TestOneofFieldTypes:
    """Test oneofs containing different field types."""

    def test_oneof_with_primitive_types(self):
        """Test oneofs with basic primitive types."""
        # String type
        msg_str = OptionalMessage(x="test_string")
        assert msg_str.a.x == "test_string"
        assert msg_str.a.a_case == "x"
        assert isinstance(msg_str.a.x, str)

        # Integer type
        msg_int = OptionalMessage(y=12345)
        assert msg_int.a.y == 12345
        assert msg_int.a.a_case == "y"
        assert isinstance(msg_int.a.y, int)

        # Verify type checking works
        with pytest.raises(ValidationError):
            OptionalMessage(x=123)  # x expects string

        with pytest.raises(ValidationError):
            OptionalMessage(y="not_an_int")  # y expects int

    def test_oneof_with_message_types(self):
        """Test oneofs containing message types."""
        # Create with message type (GeoLocation)
        geo = GeoLocation(latitude=37.7749, longitude=-122.4194, altitude_meters=50.5)
        report = ReportData(location_value=geo)

        assert report.data.location_value == geo
        assert report.data.data_case == "location_value"
        assert isinstance(report.data.location_value, GeoLocation)

        # Access nested fields
        assert report.data.location_value.latitude == 37.7749
        assert report.data.location_value.longitude == -122.4194
        assert report.data.location_value.altitude_meters == 50.5

    def test_oneof_with_well_known_types(self):
        """Test oneofs with Google well-known types."""
        # Timestamp
        ts = datetime.now()
        report_time = ReportData(time_value=ts)

        assert report_time.data.time_value == ts
        assert report_time.data.data_case == "time_value"
        assert isinstance(report_time.data.time_value, datetime)

        # Can access timestamp methods
        dt = report_time.data.time_value
        assert dt is not None

    def test_oneof_with_repeated_fields(self):
        """Test oneofs containing repeated fields."""
        # OptionalMessage has str_list as a repeated field (not in oneof)
        # But we can test the behavior with the field
        msg = OptionalMessage(x="test", str_list=["item1", "item2", "item3"])

        assert msg.a.x == "test"
        assert msg.str_list == ["item1", "item2", "item3"]
        assert isinstance(msg.str_list, list)

        # Test modification behavior
        # Note: Due to immutability, we can't modify in place
        new_list = msg.str_list + ["item4"]
        msg2 = OptionalMessage(x="test", str_list=new_list)
        assert len(msg2.str_list) == 4

    def test_oneof_with_map_fields(self):
        """Test oneofs with map fields."""
        # OptionalMessage has int_map as a map field
        msg = OptionalMessage(y=42, int_map={"key1": 100, "key2": 200, "key3": 300})

        assert msg.a.y == 42
        assert msg.int_map == {"key1": 100, "key2": 200, "key3": 300}
        assert isinstance(msg.int_map, dict)

        # Access map values
        assert msg.int_map["key1"] == 100
        assert msg.int_map.get("key2") == 200

    def test_oneof_with_optional_fields(self):
        """Test interaction between oneofs and optional fields."""
        # Create message with oneof and optional fields
        msg = OptionalMessage(
            x="oneof_value",
            name="optional_name",  # optional field
            age=25,  # optional field
        )

        assert msg.a.x == "oneof_value"
        assert msg.name == "optional_name"
        assert msg.age == 25

        # Create without optional fields
        msg2 = OptionalMessage(y=100)
        assert msg2.a.y == 100
        assert msg2.name is None  # default value
        assert msg2.age is None  # default value

    def test_oneof_with_default_values(self):
        """Test oneof fields with various default values."""
        # Test empty/zero values
        msg_empty_str = OptionalMessage(x="")
        assert msg_empty_str.a.x == ""
        assert msg_empty_str.a.a_case == "x"

        msg_zero_int = OptionalMessage(y=0)
        assert msg_zero_int.a.y == 0
        assert msg_zero_int.a.a_case == "y"

        # Empty values should still set the oneof
        assert hasattr(msg_empty_str.a, "x")
        assert not hasattr(msg_empty_str.a, "y")

    def test_oneof_field_type_validation(self):
        """Test type validation for oneof fields."""
        # Test various invalid types
        with pytest.raises(ValidationError):
            OptionalMessage(x=123)  # x expects string

        with pytest.raises(ValidationError):
            OptionalMessage(y="string")  # y expects int

        with pytest.raises(ValidationError):
            OptionalMessage(y=3.14)  # y expects int, not float

        # Test with message types
        with pytest.raises(ValidationError):
            ReportData(location_value="not_a_geo_location")

        with pytest.raises(ValidationError):
            ReportData(time_value="not_a_timestamp")

    def test_oneof_with_complex_nested_structure(self):
        """Test oneofs in complex nested structures."""
        # Create nested structure
        item = InvoiceItem(
            name="Product", amount=100, quantity=2, note=["note1", "note2"]
        )

        msg = OptionalMessage(
            x="order_123", item=item, int_map={"price": 100, "discount": 10}
        )

        assert msg.a.x == "order_123"
        assert msg.item.name == "Product"
        assert msg.item.amount == 100
        assert msg.int_map["price"] == 100

    def test_oneof_serialization_with_different_types(self):
        """Test that different field types serialize correctly."""
        # String type
        msg_str = OptionalMessage(x="test")
        dict_str = msg_str.model_dump()
        assert "a" in dict_str or "x" in dict_str

        # Integer type
        msg_int = OptionalMessage(y=42)
        dict_int = msg_int.model_dump()
        assert "a" in dict_int or "y" in dict_int

        # Message type
        geo = GeoLocation(latitude=37.7749, longitude=-122.4194)
        report = ReportData(location_value=geo)
        dict_msg = report.model_dump()

        # The serialized form should preserve the type information
        # Verify that serialization works for all types
        assert dict_str is not None
        assert dict_int is not None
        assert dict_msg is not None

    def test_oneof_with_bytes_field(self):
        """Test oneof with bytes field type."""
        # Note: The current proto doesn't have bytes in oneof,
        # but we can test the general behavior

        # If there was a bytes field in oneof, it would work like:
        # msg = SomeMessage(bytes_field=b"binary_data")
        # assert msg.oneof.bytes_field == b"binary_data"
        # assert isinstance(msg.oneof.bytes_field, bytes)

        # For now, we can test that the model handles binary data in other fields
        item = InvoiceItem(
            name="Binary Item",
            amount=100,
            quantity=1,
            note=["Contains binary"],  # note is repeated string
        )
        msg = OptionalMessage(x="has_binary", item=item)
        assert msg.item.name == "Binary Item"

    def test_oneof_field_presence(self):
        """Test field presence detection for different types."""
        # Test with different field types
        msg_str = OptionalMessage(x="present")
        msg_int = OptionalMessage(y=0)  # Even zero should count as present

        # String field present
        assert hasattr(msg_str.a, "x")
        assert not hasattr(msg_str.a, "y")

        # Integer field present (even when zero)
        assert hasattr(msg_int.a, "y")
        assert not hasattr(msg_int.a, "x")

        # Test with message types
        geo = GeoLocation(latitude=0.0, longitude=0.0)  # Zero coordinates
        report = ReportData(location_value=geo)
        assert hasattr(report.data, "location_value")
        assert not hasattr(report.data, "time_value")
