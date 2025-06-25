"""
Test round-trip conversion for numeric protobuf types.

Tests int32, int64, uint32, uint64, sint32, sint64, fixed32, fixed64, sfixed32, sfixed64.
"""

from example.proto_pydanticv2.example.example_proto.demo import (
    basic_types_roundtrip_pb2,
    basic_types_roundtrip_p2p,
)
from ..common.base_test import RoundTripTestBase


class TestNumericTypes(RoundTripTestBase):
    """Test round-trip conversion for numeric protobuf types."""

    def _test_numeric_field(self, field_name: str, test_values: list) -> None:
        """Helper to test a numeric field with various values."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        for value in test_values:
            proto_msg.Clear()
            setattr(proto_msg, field_name, value)

            self.verify_roundtrip(
                proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage
            )

    def test_int32_roundtrip(self):
        """Test int32 field round-trip conversion."""
        test_values = [
            0,
            42,
            -42,
            2147483647,  # max int32
            -2147483648,  # min int32
        ]
        self._test_numeric_field("int32_field", test_values)

    def test_int64_roundtrip(self):
        """Test int64 field round-trip conversion."""
        test_values = [
            0,
            42,
            -42,
            9223372036854775807,  # max int64
            -9223372036854775808,  # min int64
        ]
        self._test_numeric_field("int64_field", test_values)

    def test_uint32_roundtrip(self):
        """Test uint32 field round-trip conversion."""
        test_values = [
            0,
            42,
            4294967295,  # max uint32
        ]
        self._test_numeric_field("uint32_field", test_values)

    def test_uint64_roundtrip(self):
        """Test uint64 field round-trip conversion."""
        test_values = [
            0,
            42,
            18446744073709551615,  # max uint64
        ]
        self._test_numeric_field("uint64_field", test_values)

    def test_sint32_roundtrip(self):
        """Test sint32 field round-trip conversion (zigzag encoding)."""
        test_values = [
            0,
            42,
            -42,
            2147483647,  # max sint32
            -2147483648,  # min sint32
        ]
        self._test_numeric_field("sint32_field", test_values)

    def test_sint64_roundtrip(self):
        """Test sint64 field round-trip conversion (zigzag encoding)."""
        test_values = [
            0,
            42,
            -42,
            9223372036854775807,  # max sint64
            -9223372036854775808,  # min sint64
        ]
        self._test_numeric_field("sint64_field", test_values)

    def test_fixed32_roundtrip(self):
        """Test fixed32 field round-trip conversion."""
        test_values = [
            0,
            42,
            4294967295,  # max fixed32
        ]
        self._test_numeric_field("fixed32_field", test_values)

    def test_fixed64_roundtrip(self):
        """Test fixed64 field round-trip conversion."""
        test_values = [
            0,
            42,
            18446744073709551615,  # max fixed64
        ]
        self._test_numeric_field("fixed64_field", test_values)

    def test_sfixed32_roundtrip(self):
        """Test sfixed32 field round-trip conversion."""
        test_values = [
            0,
            42,
            -42,
            2147483647,  # max sfixed32
            -2147483648,  # min sfixed32
        ]
        self._test_numeric_field("sfixed32_field", test_values)

    def test_sfixed64_roundtrip(self):
        """Test sfixed64 field round-trip conversion."""
        test_values = [
            0,
            42,
            -42,
            9223372036854775807,  # max sfixed64
            -9223372036854775808,  # min sfixed64
        ]
        self._test_numeric_field("sfixed64_field", test_values)

    def test_mixed_numeric_types(self):
        """Test message with multiple numeric fields set."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        # Set various numeric fields
        proto_msg.int32_field = 100
        proto_msg.int64_field = 1000000000000
        proto_msg.uint32_field = 200
        proto_msg.uint64_field = 2000000000000
        proto_msg.sint32_field = -300
        proto_msg.sint64_field = -3000000000000
        proto_msg.fixed32_field = 400
        proto_msg.fixed64_field = 4000000000000
        proto_msg.sfixed32_field = -500
        proto_msg.sfixed64_field = -5000000000000

        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

    def test_numeric_edge_cases(self):
        """Test numeric types with edge case values."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        # Test all zeros
        proto_msg.int32_field = 0
        proto_msg.int64_field = 0
        proto_msg.uint32_field = 0
        proto_msg.uint64_field = 0
        proto_msg.sint32_field = 0
        proto_msg.sint64_field = 0
        proto_msg.fixed32_field = 0
        proto_msg.fixed64_field = 0
        proto_msg.sfixed32_field = 0
        proto_msg.sfixed64_field = 0

        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)
