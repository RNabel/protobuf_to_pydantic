"""
Test round-trip conversion for google.protobuf.Timestamp.

Tests Timestamp fields including timezone handling, precision, and edge cases.
"""

from datetime import datetime, timezone

import pytest

from example.proto_pydanticv2.example.example_proto.demo import (
    well_known_types_roundtrip_pb2,
    well_known_types_roundtrip_p2p,
)
from ..common.base_test import RoundTripTestBase


class TestTimestamp(RoundTripTestBase):
    """Test round-trip conversion for google.protobuf.Timestamp."""

    @pytest.mark.proto3_presence
    def test_timestamp_current_time(self):
        """Test Timestamp with current time."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        now = datetime.now(timezone.utc)
        proto_msg.created_at.FromDatetime(now)

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.proto3_presence
    def test_timestamp_specific_dates(self):
        """Test Timestamp with specific dates."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        test_dates = [
            datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),  # New year
            datetime(
                2023, 6, 15, 14, 30, 45, tzinfo=timezone.utc
            ),  # Mid-year with time
            datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc),  # Unix epoch
            datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc),  # Y2K
            datetime(2038, 1, 19, 3, 14, 7, tzinfo=timezone.utc),  # Near 32-bit limit
        ]

        for date in test_dates:
            proto_msg.Clear()
            proto_msg.created_at.FromDatetime(date)

            self.verify_roundtrip(
                proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
            )

    def test_timestamp_microsecond_precision(self):
        """Test Timestamp preserves microsecond precision."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Create timestamp with microseconds
        dt_with_micros = datetime(2024, 1, 1, 12, 0, 0, 123456, tzinfo=timezone.utc)
        proto_msg.created_at.FromDatetime(dt_with_micros)

        # Convert to JSON and back
        json_str = self.protobuf_to_json(proto_msg)
        pydantic_model = self.json_to_pydantic(
            json_str, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

        # Verify microseconds are preserved
        assert pydantic_model.created_at.microsecond == 123456

    def test_timestamp_json_format(self):
        """Test Timestamp JSON format is RFC3339."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Set specific timestamp
        dt = datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
        proto_msg.created_at.FromDatetime(dt)

        # Check JSON format
        json_str = self.protobuf_to_json(proto_msg)
        assert '"createdAt": "2024-01-15T10:30:00Z"' in json_str

    @pytest.mark.proto3_presence
    def test_timestamp_edge_cases(self):
        """Test Timestamp edge cases."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Far future date
        future_date = datetime(9999, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        proto_msg.created_at.FromDatetime(future_date)

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.proto3_presence
    def test_repeated_timestamps(self):
        """Test repeated Timestamp fields."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Add multiple timestamps
        timestamps = [
            datetime(2024, 1, 1, tzinfo=timezone.utc),
            datetime(2024, 2, 1, tzinfo=timezone.utc),
            datetime(2024, 3, 1, tzinfo=timezone.utc),
        ]

        for ts in timestamps:
            timestamp_msg = proto_msg.event_timestamps.add()
            timestamp_msg.FromDatetime(ts)

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    def test_timestamp_from_protobuf_to_pydantic(self):
        """Test conversion from protobuf Timestamp to Pydantic."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        proto_msg.created_at.FromDatetime(dt)

        # Convert to JSON then to Pydantic
        json_str = self.protobuf_to_json(proto_msg)
        pydantic_model = self.json_to_pydantic(
            json_str, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

        # Verify datetime is correct
        assert isinstance(pydantic_model.created_at, datetime)
        assert pydantic_model.created_at == dt

    @pytest.mark.proto3_presence
    def test_timestamp_from_pydantic_to_protobuf(self):
        """Test conversion from Pydantic to protobuf Timestamp."""
        # Create Pydantic model with timestamp
        dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        pydantic_model = well_known_types_roundtrip_p2p.WellKnownTypesMessage(
            created_at=dt
        )

        # Convert to JSON then to protobuf
        json_str = self.pydantic_to_json(pydantic_model)
        proto_msg = self.json_to_protobuf(
            json_str, well_known_types_roundtrip_pb2.WellKnownTypesMessage
        )

        # Verify timestamp is correct (ToDatetime returns timezone-naive by default)
        assert proto_msg.created_at.ToDatetime(tzinfo=timezone.utc) == dt

    @pytest.mark.proto3_presence
    def test_optional_timestamp(self):
        """Test optional Timestamp field handling."""
        # Test with timestamp set
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        if hasattr(proto_msg, "optional_timestamp"):
            dt = datetime(2024, 1, 1, tzinfo=timezone.utc)
            proto_msg.optional_timestamp.FromDatetime(dt)

            self.verify_roundtrip(
                proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
            )

    def test_timestamp_timezone_handling(self):
        """Test Timestamp timezone conversion."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Create datetime with UTC offset (no pytz needed)
        from datetime import timedelta

        offset = timedelta(hours=-5)  # Eastern time offset
        dt_eastern = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone(offset))

        # Convert to UTC for protobuf
        dt_utc = dt_eastern.astimezone(timezone.utc)
        proto_msg.created_at.FromDatetime(dt_utc)

        # Verify round-trip preserves UTC time
        json_str = self.protobuf_to_json(proto_msg)
        pydantic_model = self.json_to_pydantic(
            json_str, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

        assert pydantic_model.created_at == dt_utc
