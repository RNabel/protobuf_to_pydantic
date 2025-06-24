"""
Test round-trip conversion for google.protobuf.Duration.

Tests Duration fields including negative durations, sub-second precision, and edge cases.
"""

from datetime import timedelta
from typing import List, Optional

from example.proto_pydanticv2.example.example_proto.demo import (
    well_known_types_roundtrip_pb2,
    well_known_types_roundtrip_p2p,
)
from ..common.base_test import RoundTripTestBase


class TestDuration(RoundTripTestBase):
    """Test round-trip conversion for google.protobuf.Duration."""

    def test_duration_basic(self):
        """Test basic Duration values."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        
        test_durations = [
            timedelta(0),                              # Zero duration
            timedelta(seconds=30),                     # 30 seconds
            timedelta(minutes=5),                      # 5 minutes
            timedelta(hours=2, minutes=30),            # 2.5 hours
            timedelta(days=1),                         # 1 day
            timedelta(days=7, hours=12),               # 1 week + 12 hours
        ]
        
        for duration in test_durations:
            proto_msg.Clear()
            proto_msg.duration.FromTimedelta(duration)
            
            self.verify_roundtrip(
                proto_msg,
                well_known_types_roundtrip_p2p.WellKnownTypesMessage
            )

    def test_duration_negative(self):
        """Test negative Duration values."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        
        negative_durations = [
            timedelta(seconds=-30),
            timedelta(minutes=-5),
            timedelta(hours=-1, minutes=-30),
            timedelta(days=-1),
        ]
        
        for duration in negative_durations:
            proto_msg.Clear()
            proto_msg.duration.FromTimedelta(duration)
            
            self.verify_roundtrip(
                proto_msg,
                well_known_types_roundtrip_p2p.WellKnownTypesMessage
            )

    def test_duration_subsecond_precision(self):
        """Test Duration with sub-second precision."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        
        subsecond_durations = [
            timedelta(seconds=1, microseconds=500000),   # 1.5 seconds
            timedelta(milliseconds=100),                  # 0.1 seconds
            timedelta(microseconds=123456),               # 123.456 milliseconds
            timedelta(microseconds=1),                    # 1 microsecond
        ]
        
        for duration in subsecond_durations:
            proto_msg.Clear()
            proto_msg.duration.FromTimedelta(duration)
            
            # Convert to JSON and back
            json_str = self.protobuf_to_json(proto_msg)
            pydantic_model = self.json_to_pydantic(
                json_str,
                well_known_types_roundtrip_p2p.WellKnownTypesMessage
            )
            
            # Verify precision is preserved
            assert pydantic_model.duration == duration

    def test_duration_json_format(self):
        """Test Duration JSON format."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        
        # Test various durations and their JSON representations
        test_cases = [
            (timedelta(seconds=30), '"30s"'),
            (timedelta(seconds=1, microseconds=500000), '"1.500s"'),
            (timedelta(seconds=-30), '"-30s"'),
            (timedelta(0), '"0s"'),
        ]
        
        for duration, expected_json in test_cases:
            proto_msg.Clear()
            proto_msg.duration.FromTimedelta(duration)
            
            json_str = self.protobuf_to_json(proto_msg)
            assert f'"duration": {expected_json}' in json_str

    def test_duration_edge_cases(self):
        """Test Duration edge cases."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        
        # Large duration (1 year)
        large_duration = timedelta(days=365)
        proto_msg.duration.FromTimedelta(large_duration)
        
        self.verify_roundtrip(
            proto_msg,
            well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )
        
        # Very small duration
        small_duration = timedelta(microseconds=1)
        proto_msg.Clear()
        proto_msg.duration.FromTimedelta(small_duration)
        
        self.verify_roundtrip(
            proto_msg,
            well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    def test_repeated_durations(self):
        """Test repeated Duration fields."""
        proto_msg = well_known_types_roundtrip_pb2.RepeatedWellKnownTypes()
        
        # Add multiple durations
        durations = [
            timedelta(minutes=5),
            timedelta(hours=1),
            timedelta(days=1),
            timedelta(seconds=-30),
        ]
        
        for duration in durations:
            duration_msg = proto_msg.durations.add()
            duration_msg.FromTimedelta(duration)
        
        self.verify_roundtrip(
            proto_msg,
            well_known_types_roundtrip_p2p.RepeatedWellKnownTypes
        )

    def test_duration_from_protobuf_to_pydantic(self):
        """Test conversion from protobuf Duration to Pydantic."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        duration = timedelta(hours=2, minutes=30)
        proto_msg.duration.FromTimedelta(duration)
        
        # Convert to JSON then to Pydantic
        json_str = self.protobuf_to_json(proto_msg)
        pydantic_model = self.json_to_pydantic(
            json_str,
            well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )
        
        # Verify duration is correct
        assert isinstance(pydantic_model.duration, timedelta)
        assert pydantic_model.duration == duration

    def test_duration_from_pydantic_to_protobuf(self):
        """Test conversion from Pydantic to protobuf Duration."""
        # Create Pydantic model with duration
        duration = timedelta(hours=1, minutes=30)
        pydantic_model = well_known_types_roundtrip_p2p.WellKnownTypesMessage(
            duration=duration
        )
        
        # Convert to JSON then to protobuf
        json_str = self.pydantic_to_json(pydantic_model)
        proto_msg = self.json_to_protobuf(
            json_str,
            well_known_types_roundtrip_pb2.WellKnownTypesMessage
        )
        
        # Verify duration is correct
        assert proto_msg.duration.ToTimedelta() == duration

    def test_optional_duration(self):
        """Test optional Duration field handling."""
        # Test with duration set
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        if hasattr(proto_msg, 'optional_duration'):
            duration = timedelta(minutes=10)
            proto_msg.optional_duration.FromTimedelta(duration)
            
            self.verify_roundtrip(
                proto_msg,
                well_known_types_roundtrip_p2p.WellKnownTypesMessage
            )

    def test_duration_arithmetic(self):
        """Test Duration values from arithmetic operations."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        
        # Duration from subtraction
        duration = timedelta(hours=3) - timedelta(minutes=30)
        proto_msg.duration.FromTimedelta(duration)
        
        self.verify_roundtrip(
            proto_msg,
            well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )
        
        # Duration from multiplication
        base_duration = timedelta(minutes=15)
        multiplied_duration = base_duration * 4  # 1 hour
        proto_msg.Clear()
        proto_msg.duration.FromTimedelta(multiplied_duration)
        
        self.verify_roundtrip(
            proto_msg,
            well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    def test_duration_seconds_nanos_split(self):
        """Test Duration with explicit seconds and nanos."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        
        # Set duration with 1.5 seconds (1 second + 500,000,000 nanos)
        proto_msg.duration.seconds = 1
        proto_msg.duration.nanos = 500000000
        
        # Convert to Pydantic and verify
        json_str = self.protobuf_to_json(proto_msg)
        pydantic_model = self.json_to_pydantic(
            json_str,
            well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )
        
        expected_duration = timedelta(seconds=1, microseconds=500000)
        assert pydantic_model.duration == expected_duration