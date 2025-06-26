"""
Test round-trip conversion for google.protobuf wrapper types.

Tests wrapper types like DoubleValue, FloatValue, Int64Value, UInt64Value,
Int32Value, UInt32Value, BoolValue, StringValue, BytesValue.
"""

import math

import pytest

from example.proto_pydanticv2.example.example_proto.demo import (
    well_known_types_roundtrip_pb2,
    well_known_types_roundtrip_p2p,
)
from ..common.base_test import RoundTripTestBase


class TestWrapperTypes(RoundTripTestBase):
    """Test round-trip conversion for google.protobuf wrapper types."""

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_double_value(self):
        """Test DoubleValue wrapper."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        test_values = [
            0.0,
            3.141592653589793,
            -3.141592653589793,
            1e100,
            1e-100,
            float("inf"),
            float("-inf"),
        ]

        for value in test_values:
            proto_msg.Clear()
            proto_msg.double_value.value = value

            self.verify_roundtrip(
                proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
            )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_double_value_nan(self):
        """Test DoubleValue with NaN."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()
        proto_msg.double_value.value = float("nan")

        # Can't use normal roundtrip for NaN
        json_str = self.protobuf_to_json(proto_msg)
        pydantic_model = self.json_to_pydantic(
            json_str, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

        assert math.isnan(pydantic_model.double_value)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_float_value(self):
        """Test FloatValue wrapper."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        test_values = [
            0.0,
            3.14159,
            -3.14159,
            1e10,
            1e-10,
            float("inf"),
            float("-inf"),
        ]

        for value in test_values:
            proto_msg.Clear()
            proto_msg.float_value.value = value

            self.verify_roundtrip(
                proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
            )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_int64_value(self):
        """Test Int64Value wrapper."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        test_values = [
            0,
            42,
            -42,
            9223372036854775807,  # max int64
            -9223372036854775808,  # min int64
        ]

        for value in test_values:
            proto_msg.Clear()
            proto_msg.int64_value.value = value

            self.verify_roundtrip(
                proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
            )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_uint64_value(self):
        """Test UInt64Value wrapper."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        test_values = [
            0,
            42,
            18446744073709551615,  # max uint64
        ]

        for value in test_values:
            proto_msg.Clear()
            proto_msg.uint64_value.value = value

            self.verify_roundtrip(
                proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
            )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_int32_value(self):
        """Test Int32Value wrapper."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        test_values = [
            0,
            42,
            -42,
            2147483647,  # max int32
            -2147483648,  # min int32
        ]

        for value in test_values:
            proto_msg.Clear()
            proto_msg.int32_value.value = value

            self.verify_roundtrip(
                proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
            )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_uint32_value(self):
        """Test UInt32Value wrapper."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        test_values = [
            0,
            42,
            4294967295,  # max uint32
        ]

        for value in test_values:
            proto_msg.Clear()
            proto_msg.uint32_value.value = value

            self.verify_roundtrip(
                proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
            )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_bool_value(self):
        """Test BoolValue wrapper."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Test true
        proto_msg.bool_value.value = True
        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

        # Test false
        proto_msg.Clear()
        proto_msg.bool_value.value = False
        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_string_value(self):
        """Test StringValue wrapper."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        test_values = [
            "",
            "hello",
            "Hello, World!",
            "unicode: 你好世界",
            "emoji: 😀🎉",
            "multiline\nstring",
        ]

        for value in test_values:
            proto_msg.Clear()
            proto_msg.string_value.value = value

            self.verify_roundtrip(
                proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
            )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_bytes_value(self):
        """Test BytesValue wrapper."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        test_values = [
            b"",
            b"hello",
            b"binary\x00data",
            b"\xff\xfe\xfd\xfc",
            bytes(range(256)),
        ]

        for value in test_values:
            proto_msg.Clear()
            proto_msg.bytes_value.value = value

            self.verify_roundtrip(
                proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
            )

    def test_wrapper_null_representation(self):
        """Test wrapper types with null/unset values."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Don't set any wrapper fields
        # In proto3, unset wrapper fields should not appear in JSON
        json_str = self.protobuf_to_json(
            proto_msg, always_print_fields_with_no_presence=False
        )

        # Verify wrapper fields are not in JSON when unset
        assert "doubleValue" not in json_str
        assert "floatValue" not in json_str
        assert "int64Value" not in json_str
        assert "boolValue" not in json_str
        assert "stringValue" not in json_str

    @pytest.mark.skip(reason="Wrapper types are not supported yet")
    def test_wrapper_zero_values(self):
        """Test wrapper types with zero/empty values."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Set wrapper fields to zero/empty values
        proto_msg.double_value.value = 0.0
        proto_msg.int32_value.value = 0
        proto_msg.bool_value.value = False
        proto_msg.string_value.value = ""
        proto_msg.bytes_value.value = b""

        # These should be serialized since they're explicitly set
        json_str = self.protobuf_to_json(proto_msg)
        assert '"doubleValue": 0' in json_str
        assert '"int32Value": 0' in json_str
        assert '"boolValue": false' in json_str
        assert '"stringValue": ""' in json_str
        assert '"bytesValue": ""' in json_str

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_multiple_wrappers(self):
        """Test message with multiple wrapper types."""
        proto_msg = well_known_types_roundtrip_pb2.WellKnownTypesMessage()

        # Set multiple wrapper fields
        proto_msg.double_value.value = 3.14159
        proto_msg.int64_value.value = 1234567890
        proto_msg.bool_value.value = True
        proto_msg.string_value.value = "test"

        self.verify_roundtrip(
            proto_msg, well_known_types_roundtrip_p2p.WellKnownTypesMessage
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_wrapper_from_pydantic(self):
        """Test creating wrapper types from Pydantic models."""
        # Create Pydantic model with wrapper values
        pydantic_model = well_known_types_roundtrip_p2p.WellKnownTypesMessage(
            double_value=2.71828, int32_value=42, bool_value=True, string_value="hello"
        )

        # Convert to JSON then to protobuf
        json_str = self.pydantic_to_json(pydantic_model)
        proto_msg = self.json_to_protobuf(
            json_str, well_known_types_roundtrip_pb2.WellKnownTypesMessage
        )

        # Verify values
        assert proto_msg.double_value.value == 2.71828
        assert proto_msg.int32_value.value == 42
        assert proto_msg.bool_value.value == True
        assert proto_msg.string_value.value == "hello"
