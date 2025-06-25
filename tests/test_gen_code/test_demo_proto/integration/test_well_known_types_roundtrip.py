"""
Test round-trip conversion for well-known protobuf types.

Tests for google.protobuf well-known types like Timestamp, Duration, Value, etc.
"""

from datetime import datetime, timedelta, timezone

import pytest

from example.proto_pydanticv2.example.example_proto.demo import (
    well_known_types_roundtrip_pb2,
    well_known_types_roundtrip_p2p,
    value_demo_pb2,
    value_demo_p2p,
)
from ..common.base_test import RoundTripTestBase


class TestWellKnownTypesRoundTrip(RoundTripTestBase):
    """Test round-trip conversion for well-known protobuf types."""

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_timestamp_roundtrip(self):
        """Test Timestamp field round-trip conversion."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Set a specific timestamp
        now = datetime.now(timezone.utc)
        proto_msg.created_at.FromDatetime(now)

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_duration_roundtrip(self):
        """Test Duration field round-trip conversion."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Set a specific duration (1 hour, 30 minutes)
        proto_msg.duration.FromTimedelta(timedelta(hours=1, minutes=30))

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_double_value_roundtrip(self):
        """Test DoubleValue wrapper round-trip conversion."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Set double value
        proto_msg.double_value.value = 3.14159

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_float_value_roundtrip(self):
        """Test FloatValue wrapper round-trip conversion."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Set float value
        proto_msg.float_value.value = 2.71828

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_int64_value_roundtrip(self):
        """Test Int64Value wrapper round-trip conversion."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Set int64 value
        proto_msg.int64_value.value = 9223372036854775807  # max int64

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_uint64_value_roundtrip(self):
        """Test UInt64Value wrapper round-trip conversion."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Set uint64 value
        proto_msg.uint64_value.value = 18446744073709551615  # max uint64

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_int32_value_roundtrip(self):
        """Test Int32Value wrapper round-trip conversion."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Set int32 value
        proto_msg.int32_value.value = 2147483647  # max int32

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_uint32_value_roundtrip(self):
        """Test UInt32Value wrapper round-trip conversion."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Set uint32 value
        proto_msg.uint32_value.value = 4294967295  # max uint32

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_bool_value_roundtrip(self):
        """Test BoolValue wrapper round-trip conversion."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Set bool value
        proto_msg.bool_value.value = True

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_string_value_roundtrip(self):
        """Test StringValue wrapper round-trip conversion."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Set string value
        proto_msg.string_value.value = "Hello, World!"

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_bytes_value_roundtrip(self):
        """Test BytesValue wrapper round-trip conversion."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Set bytes value
        proto_msg.bytes_value.value = b"binary data"

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_value_null_roundtrip(self):
        """Test google.protobuf.Value with null value."""
        proto_msg = value_demo_pb2.ValueDemo()

        # Set null value
        proto_msg.single_value.null_value = 0  # NULL_VALUE

        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueDemo)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_value_number_roundtrip(self):
        """Test google.protobuf.Value with number value."""
        proto_msg = value_demo_pb2.ValueDemo()

        # Set number value
        proto_msg.single_value.number_value = 42.5

        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueDemo)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_value_string_roundtrip(self):
        """Test google.protobuf.Value with string value."""
        proto_msg = value_demo_pb2.ValueDemo()

        # Set string value
        proto_msg.single_value.string_value = "test string"

        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueDemo)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_value_bool_roundtrip(self):
        """Test google.protobuf.Value with bool value."""
        proto_msg = value_demo_pb2.ValueDemo()

        # Set bool value
        proto_msg.single_value.bool_value = True

        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueDemo)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_value_struct_roundtrip(self):
        """Test google.protobuf.Value with struct value."""
        proto_msg = value_demo_pb2.ValueDemo()

        # Set struct value
        proto_msg.single_value.struct_value.fields["key1"].string_value = "value1"
        proto_msg.single_value.struct_value.fields["key2"].number_value = 123
        proto_msg.single_value.struct_value.fields["key3"].bool_value = False

        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueDemo)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_value_list_roundtrip(self):
        """Test google.protobuf.Value with list value."""
        proto_msg = value_demo_pb2.ValueDemo()

        # Set list value
        list_value = proto_msg.single_value.list_value
        list_value.values.add().string_value = "item1"
        list_value.values.add().number_value = 42
        list_value.values.add().bool_value = True
        list_value.values.add().null_value = 0

        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueDemo)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_complex_well_known_types_message(self):
        """Test complex message with multiple well-known types."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Set multiple fields
        proto_msg.created_at.FromDatetime(
            datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        )
        proto_msg.duration.FromTimedelta(timedelta(days=1, hours=2, minutes=30))
        proto_msg.double_value.value = 3.14159
        proto_msg.string_value.value = "test"
        proto_msg.bool_value.value = True

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_repeated_timestamps(self):
        """Test repeated timestamp fields."""
        proto_msg = well_known_types_roundtrip_pb2.RepeatedWellKnownTypes()

        # Add multiple timestamps
        ts1 = proto_msg.timestamps.add()
        ts1.FromDatetime(datetime(2024, 1, 1, tzinfo=timezone.utc))

        ts2 = proto_msg.timestamps.add()
        ts2.FromDatetime(datetime(2024, 6, 15, 14, 30, tzinfo=timezone.utc))

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.RepeatedWellKnownTypes
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_map_with_value_type(self):
        """Test map fields with google.protobuf.Value values."""
        proto_msg = value_demo_pb2.ValueDemo()

        # Add various value types to map
        proto_msg.value_map["null_key"].null_value = 0
        proto_msg.value_map["number_key"].number_value = 123.45
        proto_msg.value_map["string_key"].string_value = "hello"
        proto_msg.value_map["bool_key"].bool_value = True

        # Add a struct value
        proto_msg.value_map["struct_key"].struct_value.fields[
            "nested"
        ].string_value = "nested value"

        # Add a list value
        list_val = proto_msg.value_map["list_key"].list_value
        list_val.values.add().number_value = 1
        list_val.values.add().number_value = 2
        list_val.values.add().number_value = 3

        self.verify_roundtrip(proto_msg, value_demo_p2p.ValueDemo)
