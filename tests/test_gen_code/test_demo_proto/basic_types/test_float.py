"""
Test round-trip conversion for floating-point protobuf types.

Tests float and double types including special values (inf, -inf, nan).
"""

import math
import sys
from typing import Any, Dict

from google.protobuf.internal import type_checkers
from example.proto_pydanticv2.example.example_proto.demo import (
    basic_types_roundtrip_pb2,
    basic_types_roundtrip_p2p,
)
from ..common.base_test import RoundTripTestBase

# Float32 constants - using values that work with protobuf's JSON serialization
# The actual protobuf _FLOAT_MAX gets rounded during JSON serialization to a slightly
# larger value, so we use a smaller value to avoid this issue
FLOAT32_MAX = 3.4e+38  # Safely below protobuf's _FLOAT_MAX to avoid JSON rounding issues
FLOAT32_MIN = -3.4e+38


class TestFloatingPointTypes(RoundTripTestBase):
    """Test round-trip conversion for floating-point protobuf types."""

    def test_float_roundtrip(self):
        """Test float field round-trip conversion."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        
        test_values = [
            0.0,
            3.14159,
            -3.14159,
            1e-10,
            1e10,
            float('inf'),
            float('-inf'),
            # Note: NaN requires special handling as NaN != NaN
        ]
        
        for value in test_values:
            proto_msg.Clear()
            proto_msg.float_field = value
            
            self.verify_roundtrip(
                proto_msg,
                basic_types_roundtrip_p2p.BasicTypesMessage
            )

    def test_float_nan_roundtrip(self):
        """Test float NaN value round-trip conversion."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        proto_msg.float_field = float('nan')
        
        # Can't use normal verify_roundtrip for NaN since NaN != NaN
        # Convert to JSON and back, then check that result is also NaN
        proto_json = self.protobuf_to_json(proto_msg)
        pydantic_model = self.json_to_pydantic(
            proto_json, 
            basic_types_roundtrip_p2p.BasicTypesMessage
        )
        
        assert math.isnan(pydantic_model.float_field)
        
        # Convert back to protobuf
        pydantic_json = self.pydantic_to_json(pydantic_model)
        reconstructed_msg = self.json_to_protobuf(
            pydantic_json, 
            basic_types_roundtrip_pb2.BasicTypesMessage
        )
        
        assert math.isnan(reconstructed_msg.float_field)

    def test_double_roundtrip(self):
        """Test double field round-trip conversion."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        
        test_values = [
            0.0,
            3.141592653589793,
            -3.141592653589793,
            1e-100,
            1e100,
            float('inf'),
            float('-inf'),
        ]
        
        for value in test_values:
            proto_msg.Clear()
            proto_msg.double_field = value
            
            self.verify_roundtrip(
                proto_msg,
                basic_types_roundtrip_p2p.BasicTypesMessage
            )

    def test_double_nan_roundtrip(self):
        """Test double NaN value round-trip conversion."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        proto_msg.double_field = float('nan')
        
        # Can't use normal verify_roundtrip for NaN since NaN != NaN
        # Convert to JSON and back, then check that result is also NaN
        proto_json = self.protobuf_to_json(proto_msg)
        pydantic_model = self.json_to_pydantic(
            proto_json, 
            basic_types_roundtrip_p2p.BasicTypesMessage
        )
        
        assert math.isnan(pydantic_model.double_field)
        
        # Convert back to protobuf
        pydantic_json = self.pydantic_to_json(pydantic_model)
        reconstructed_msg = self.json_to_protobuf(
            pydantic_json, 
            basic_types_roundtrip_pb2.BasicTypesMessage
        )
        
        assert math.isnan(reconstructed_msg.double_field)

    def test_float_precision_boundaries(self):
        """Test float precision boundaries."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        
        # Test values at float precision boundaries
        # Using protobuf's internal limits which are slightly smaller than theoretical float32 limits
        test_values = [
            FLOAT32_MAX,    # Max float32 value accepted by protobuf
            FLOAT32_MIN,    # Min float32 value accepted by protobuf
            1.175494e-38,   # Near smallest positive normalized float
            -1.175494e-38,  # Near smallest negative normalized float
        ]
        
        for value in test_values:
            proto_msg.Clear()
            proto_msg.float_field = value
            
            self.verify_roundtrip(
                proto_msg,
                basic_types_roundtrip_p2p.BasicTypesMessage
            )

    def test_double_precision_boundaries(self):
        """Test double precision boundaries."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        
        # Test values at double precision boundaries
        test_values = [
            1.7976931348623157e308,   # Near max double
            -1.7976931348623157e308,  # Near min double
            2.2250738585072014e-308,  # Near smallest positive normalized double
            -2.2250738585072014e-308, # Near smallest negative normalized double
        ]
        
        for value in test_values:
            proto_msg.Clear()
            proto_msg.double_field = value
            
            self.verify_roundtrip(
                proto_msg,
                basic_types_roundtrip_p2p.BasicTypesMessage
            )

    def test_mixed_float_double(self):
        """Test message with both float and double fields."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        
        proto_msg.float_field = 3.14159
        proto_msg.double_field = 2.718281828459045
        
        self.verify_roundtrip(
            proto_msg,
            basic_types_roundtrip_p2p.BasicTypesMessage
        )

    def test_special_float_values_json_format(self):
        """Test special float values serialize correctly to JSON."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        
        # Test infinity
        proto_msg.float_field = float('inf')
        json_str = self.protobuf_to_json(proto_msg)
        assert '"floatField": "Infinity"' in json_str
        
        # Test negative infinity
        proto_msg.float_field = float('-inf')
        json_str = self.protobuf_to_json(proto_msg)
        assert '"floatField": "-Infinity"' in json_str
        
        # Test NaN
        proto_msg.float_field = float('nan')
        json_str = self.protobuf_to_json(proto_msg)
        assert '"floatField": "NaN"' in json_str