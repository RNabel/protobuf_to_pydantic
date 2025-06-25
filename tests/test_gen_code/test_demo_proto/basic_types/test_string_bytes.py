"""
Test round-trip conversion for string and bytes protobuf types.

Tests string and bytes fields including edge cases like empty strings,
unicode characters, and binary data.
"""

from example.proto_pydanticv2.example.example_proto.demo import (
    basic_types_roundtrip_pb2,
    basic_types_roundtrip_p2p,
)
from ..common.base_test import RoundTripTestBase


class TestStringBytesTypes(RoundTripTestBase):
    """Test round-trip conversion for string and bytes protobuf types."""

    def test_string_roundtrip(self):
        """Test string field round-trip conversion."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        test_values = [
            "",  # Empty string
            "hello",  # Simple ASCII
            "Hello, World!",  # ASCII with punctuation
            "test\nwith\nnewlines",  # Newlines
            "test\twith\ttabs",  # Tabs
            "unicode: 你好世界",  # Unicode characters
            "emoji: 😀🎉🌟",  # Emoji
            "special: @#$%^&*()",  # Special characters
            " leading and trailing spaces ",
            "a" * 1000,  # Long string
        ]

        for value in test_values:
            proto_msg.Clear()
            proto_msg.string_field = value

            self.verify_roundtrip(
                proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage
            )

    def test_bytes_roundtrip(self):
        """Test bytes field round-trip conversion."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        test_values = [
            b"",  # Empty bytes
            b"hello",  # Simple ASCII bytes
            b"Hello, World!",  # ASCII bytes with punctuation
            b"\x00\x01\x02\x03",  # Binary data with null bytes
            b"\xff\xfe\xfd\xfc",  # High byte values
            bytes(range(256)),  # All byte values
            b"test\nwith\nnewlines",
            b"a" * 1000,  # Long bytes
        ]

        for value in test_values:
            proto_msg.Clear()
            proto_msg.bytes_field = value

            self.verify_roundtrip(
                proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage
            )

    def test_string_escaping(self):
        """Test string fields with characters that need escaping."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        test_values = [
            '"quotes"',
            "'single quotes'",
            "\\backslash\\",
            "/forward/slash/",
            "\r\ncarriage return and newline",
            "null\x00character",  # Null character in string
            '{"json": "like"}',
            "<html>tags</html>",
        ]

        for value in test_values:
            proto_msg.Clear()
            proto_msg.string_field = value

            self.verify_roundtrip(
                proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage
            )

    def test_unicode_normalization(self):
        """Test unicode string normalization."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        # Test various unicode normalization forms
        test_values = [
            "café",  # NFC form
            "café",  # NFD form (e + combining acute)
            "Ω",  # Greek letter omega
            "🇺🇸",  # Flag emoji (regional indicators)
            "👨‍👩‍👧‍👦",  # Family emoji with ZWJ
            "\u200b",  # Zero-width space
            "A\u0300",  # A with combining grave accent
        ]

        for value in test_values:
            proto_msg.Clear()
            proto_msg.string_field = value

            self.verify_roundtrip(
                proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage
            )

    def test_bytes_base64_encoding(self):
        """Test bytes field base64 encoding in JSON."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        proto_msg.bytes_field = b"Hello, World!"

        # Check that bytes are base64 encoded in JSON
        json_str = self.protobuf_to_json(proto_msg)
        assert '"bytesField": "SGVsbG8sIFdvcmxkIQ=="' in json_str

        # Verify round-trip
        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

    def test_mixed_string_bytes(self):
        """Test message with both string and bytes fields."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        proto_msg.string_field = "Hello, 世界! 🌍"
        proto_msg.bytes_field = b"\x00\x01\x02\x03\xff\xfe\xfd\xfc"

        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

    def test_empty_vs_unset_string(self):
        """Test distinction between empty string and unset string."""
        # Create message with empty string
        proto_msg1 = basic_types_roundtrip_pb2.BasicTypesMessage()
        proto_msg1.string_field = ""

        # Create message with unset string (will have default empty string)
        proto_msg2 = basic_types_roundtrip_pb2.BasicTypesMessage()

        # Both should round-trip successfully
        self.verify_roundtrip(proto_msg1, basic_types_roundtrip_p2p.BasicTypesMessage)

        self.verify_roundtrip(proto_msg2, basic_types_roundtrip_p2p.BasicTypesMessage)

    def test_string_field_max_length(self):
        """Test string field with maximum reasonable length."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        # Test with a reasonably large string (10KB)
        large_string = "x" * 10240
        proto_msg.string_field = large_string

        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)
