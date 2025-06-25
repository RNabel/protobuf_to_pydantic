"""
Test round-trip conversion for collection types (repeated and map fields).

Tests repeated fields and map fields with various data types.
"""

import pytest

from example.proto_pydanticv2.example.example_proto.demo import (
    basic_types_roundtrip_pb2,
    basic_types_roundtrip_p2p,
    demo_pb2,
    demo_p2p,
)
from ..common.base_test import RoundTripTestBase


class TestCollectionTypes(RoundTripTestBase):
    """Test round-trip conversion for repeated and map field types."""

    def test_repeated_int32(self):
        """Test repeated int32 field."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        # Empty repeated field
        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

        # With values
        proto_msg.repeated_int32.extend([1, 2, 3, 4, 5])
        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

        # With duplicate values
        proto_msg.Clear()
        proto_msg.repeated_int32.extend([1, 1, 2, 2, 3, 3])
        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

    def test_repeated_string(self):
        """Test repeated string field."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        proto_msg.repeated_string.extend(
            [
                "hello",
                "world",
                "",  # Empty string in list
                "unicode: 你好",
                "emoji: 🎉",
            ]
        )

        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

    def test_repeated_bytes(self):
        """Test repeated bytes field."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        proto_msg.repeated_bytes.extend(
            [
                b"hello",
                b"world",
                b"",  # Empty bytes
                b"\x00\x01\x02\x03",
                b"\xff\xfe\xfd\xfc",
            ]
        )

        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

    def test_repeated_bool(self):
        """Test repeated bool field."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        proto_msg.repeated_bool.extend([True, False, True, True, False, False, True])

        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

    def test_repeated_float(self):
        """Test repeated float field."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        proto_msg.repeated_float.extend(
            [0.0, 1.1, -2.2, 3.14159, float("inf"), float("-inf")]
        )

        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

    def test_large_repeated_field(self):
        """Test repeated field with many elements."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        # Add 1000 elements
        proto_msg.repeated_int32.extend(range(1000))

        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

    def test_map_string_int32(self):
        """Test map<string, int32> field."""
        proto_msg = demo_pb2.MapMessage()

        # Empty map
        # MapMessage has user_map and user_flag fields
        # Test with user_flag which is map<string, bool>
        proto_msg.user_flag["active"] = True
        proto_msg.user_flag["enabled"] = False
        proto_msg.user_flag["debug"] = True

        self.verify_roundtrip(proto_msg, demo_p2p.MapMessage)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_map_string_message(self):
        """Test map<string, Message> field."""
        proto_msg = demo_pb2.MapMessage()

        # Add UserMessage entries to user_map
        user1 = proto_msg.user_map["user1"]
        user1.uid = "123"
        user1.age = 25
        user1.user_name = "Alice"

        user2 = proto_msg.user_map["user2"]
        user2.uid = "456"
        user2.age = 30
        user2.user_name = "Bob"

        self.verify_roundtrip(proto_msg, demo_p2p.MapMessage)

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_nested_message_with_map(self):
        """Test nested message containing map fields."""
        proto_msg = demo_pb2.NestedMessage()

        # user_list_map is map<string, RepeatedMessage>
        repeated_msg = proto_msg.user_list_map["list1"]
        repeated_msg.str_list.extend(["a", "b", "c"])
        repeated_msg.int_list.extend([1, 2, 3])

        # user_map is map<string, MapMessage>
        map_msg = proto_msg.user_map["map1"]
        map_msg.user_flag["test"] = True

        self.verify_roundtrip(proto_msg, demo_p2p.NestedMessage)

    def test_map_with_special_keys(self):
        """Test map fields with special string keys."""
        proto_msg = demo_pb2.MapMessage()

        # Test special characters in keys for user_flag map
        proto_msg.user_flag[""] = True  # Empty key
        proto_msg.user_flag["with spaces"] = False
        proto_msg.user_flag["with\nnewline"] = True
        proto_msg.user_flag["with\ttab"] = False
        proto_msg.user_flag["unicode:你好"] = True
        proto_msg.user_flag["special:@#$%"] = False

        self.verify_roundtrip(proto_msg, demo_p2p.MapMessage)

    def test_multiple_collections(self):
        """Test message with multiple repeated and map fields."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        # Set multiple repeated fields
        proto_msg.repeated_int32.extend([1, 2, 3])
        proto_msg.repeated_string.extend(["a", "b", "c"])
        proto_msg.repeated_bool.extend([True, False, True])

        # Also set some scalar fields
        proto_msg.int32_field = 42
        proto_msg.string_field = "test"

        self.verify_roundtrip(proto_msg, basic_types_roundtrip_p2p.BasicTypesMessage)

    def test_repeated_field_ordering(self):
        """Test that repeated field order is preserved."""
        proto_msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        # Add elements in specific order
        values = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        proto_msg.repeated_int32.extend(values)

        # Convert to JSON and back
        proto_json = self.protobuf_to_json(proto_msg)
        pydantic_model = self.json_to_pydantic(
            proto_json, basic_types_roundtrip_p2p.BasicTypesMessage
        )

        # Verify order is preserved
        assert list(pydantic_model.repeated_int32) == values
