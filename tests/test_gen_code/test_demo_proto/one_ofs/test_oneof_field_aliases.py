"""Test oneof field naming conventions.

Currently, protobuf_to_pydantic generates Python field names using snake_case,
following Python conventions. This test documents the current behavior and
what would be needed to support camelCase aliases.
"""

from datetime import datetime
import pytest
from example.proto_pydanticv2.example.example_proto.demo.alias_demo_p2p import (
    ReportData,
    GeoLocation,
    Report,
)
from google.protobuf.timestamp_pb2 import Timestamp


class TestOneofFieldNaming:
    """Test oneof field access with different naming conventions."""

    def test_oneof_instantiation_with_snake_case(self):
        """Test creating oneof with snake_case field names (current behavior)."""
        # Create with location_value (snake_case)
        geo = GeoLocation(latitude=37.7749, longitude=-122.4194)
        report_data = ReportData(location_value=geo)

        assert hasattr(report_data, "data")
        assert report_data.data.location_value == geo
        assert report_data.data.data_case == "location_value"

        # Create with time_value (snake_case)
        ts = datetime.now()
        report_data2 = ReportData(time_value=ts)

        assert report_data2.data.time_value == ts
        assert report_data2.data.data_case == "time_value"

    def test_oneof_supports_camelcase(self):
        """Test that camelCase field names are now supported via aliases."""
        geo = GeoLocation(latitude=40.7128, longitude=-74.0060)

        # CamelCase is now supported
        report_data = ReportData(locationValue=geo)
        assert report_data.data.location_value == geo
        assert report_data.data.data_case == "location_value"

        # Snake case still works
        report_data2 = ReportData(location_value=geo)
        assert report_data2.data.location_value == geo

    def test_oneof_dict_instantiation_supports_both_cases(self):
        """Test creating oneof from dict supports both snake_case and camelCase."""
        geo = GeoLocation(latitude=51.5074, longitude=-0.1278)

        # Snake case in dict works
        report_data1 = ReportData(**{"location_value": geo})
        assert report_data1.data.location_value == geo

        # Camel case in dict now also works
        report_data2 = ReportData(**{"locationValue": geo})
        assert report_data2.data.location_value == geo

    def test_model_dump_uses_snake_case(self):
        """Test that model_dump uses snake_case."""
        geo = GeoLocation(latitude=35.6762, longitude=139.6503)
        report_data = ReportData(location_value=geo)
        dump = report_data.model_dump()

        # Output uses snake_case
        assert "location_value" in dump
        assert "locationValue" not in dump
        assert dump["location_value"]["latitude"] == 35.6762

    def test_nested_oneof_with_snake_case(self):
        """Test oneofs nested in other messages."""
        geo = GeoLocation(latitude=48.8566, longitude=2.3522, altitude_meters=100)

        # Create Report with nested ReportData
        report = Report(source_id="sensor-123", data=ReportData(location_value=geo))

        assert report.data.data.location_value == geo
        assert report.data.data.data_case == "location_value"

        # Also test with dict
        report2 = Report(source_id="sensor-456", data={"location_value": geo})

        assert report2.source_id == "sensor-456"
        assert report2.data.data.location_value == geo

    def test_json_serialization_uses_snake_case(self):
        """Test JSON serialization uses snake_case."""
        geo = GeoLocation(latitude=-33.8688, longitude=151.2093)
        report_data = ReportData(location_value=geo)

        json_str = report_data.model_dump_json()
        assert "location_value" in json_str
        assert "locationValue" not in json_str

        # Parse back from JSON should work with dict representation
        report_data2 = ReportData.model_validate_json(json_str)
        # Since location_value is typed as Any, it comes back as a dict
        assert report_data2.data.location_value.latitude == -33.8688

    def test_camelcase_alias_support(self):
        """Test comprehensive camelCase support for oneofs."""
        geo = GeoLocation(latitude=40.7128, longitude=-74.0060)

        # Accept camelCase
        report_data = ReportData(locationValue=geo)
        assert report_data.data.location_value == geo
        assert report_data.data.data_case == "location_value"

        # Also accept snake_case
        report_data2 = ReportData(location_value=geo)
        assert report_data2.data.location_value == geo

        # JSON can use either format
        json_camel = '{"locationValue": {"latitude": 40.7128, "longitude": -74.0060, "altitude_meters": 0.0}}'
        report_data3 = ReportData.model_validate_json(json_camel)
        assert report_data3.data.location_value.latitude == 40.7128

        # Test with multiple oneof fields error (not multiple aliases)
        ts = Timestamp()
        ts.GetCurrentTime()
        with pytest.raises(ValueError, match="Multiple fields"):
            ReportData.model_validate({"location_value": geo, "time_value": ts})
