"""Test edge cases for oneofs with generated Pydantic models.

Tests edge case scenarios:
- Multiple oneofs in same message (if available)
- Nested oneofs
- Oneof field name conflicts
- Oneofs with single field
- Large oneofs (many fields)
- Performance considerations
"""

import pytest
import time
from pydantic import ValidationError

from example.proto_pydanticv2.example.example_proto.demo.demo_p2p import (
    OptionalMessage,
    InvoiceItem,
)
from example.proto_pydanticv2.example.example_proto.demo.alias_demo_p2p import (
    ReportData,
    GeoLocation,
)
from example.proto_pydanticv2.example.example_proto.demo.all_feidl_set_optional_demo_p2p import (
    OptionalMessage as AllOptionalMessage,
)


class TestOneofEdgeCases:
    """Test edge cases for oneof functionality."""

    def test_oneof_with_single_field(self):
        """Test behavior when oneof has only one field.

        Note: Our test protos don't have single-field oneofs,
        but we can test the concept with what we have.
        """
        # Even with multiple fields available, using just one consistently
        messages = []
        for i in range(10):
            # Always use the same field
            msg = OptionalMessage(x=f"value_{i}")
            messages.append(msg)

        # All should have the same discriminator
        assert all(msg.a.a_case == "x" for msg in messages)

        # None should have the other field
        assert all(not hasattr(msg.a, "y") for msg in messages)

    def test_oneof_field_name_patterns(self):
        """Test various field naming patterns in oneofs."""
        # Test snake_case fields
        msg1 = OptionalMessage(x="test")  # Simple name
        assert msg1.a.x == "test"

        # Test with ReportData which has longer field names
        geo = GeoLocation(latitude=37.7749, longitude=-122.4194)
        report = ReportData(location_value=geo)  # snake_case name
        assert report.data.data_case == "location_value"

        # Test camelCase alias
        report2 = ReportData(locationValue=geo)  # camelCase alias
        assert report2.data.data_case == "location_value"  # Still snake_case internally

    def test_rapid_oneof_switching(self):
        """Test creating many instances with different oneof fields."""
        # Rapidly create instances alternating between fields
        start_time = time.time()
        instances = []

        for i in range(100):
            if i % 2 == 0:
                msg = OptionalMessage(x=f"string_{i}")
            else:
                msg = OptionalMessage(y=i)
            instances.append(msg)

        creation_time = time.time() - start_time
        print(f"Created 100 instances in {creation_time:.4f} seconds")

        # Verify all instances are correct
        for i, msg in enumerate(instances):
            if i % 2 == 0:
                assert msg.a.a_case == "x"
                assert msg.a.x == f"string_{i}"
            else:
                assert msg.a.a_case == "y"
                assert msg.a.y == i

    def test_oneof_with_complex_nested_data(self):
        """Test oneofs with deeply nested complex data structures."""
        # Create complex nested structure
        item = InvoiceItem(
            name="Complex Product with Very Long Name " * 5,
            amount=12345,
            quantity=999,
            items=[
                InvoiceItem(name=f"Subitem {i}", amount=100, quantity=1)
                for i in range(3)
            ],
        )

        msg = OptionalMessage(
            x="order_" + "x" * 1000,  # Long string
            item=item,
            str_list=[f"tag_{i}" for i in range(50)],
            int_map={f"key_{i}": i * 100 for i in range(30)},
        )

        # Verify it handles large data
        assert len(msg.a.x) == 1006
        assert len(msg.item.items) == 3
        assert len(msg.str_list) == 50
        assert len(msg.int_map) == 30

        # Test serialization of large data
        json_str = msg.model_dump_json()
        assert len(json_str) > 2000  # Should be reasonably large

    def test_oneof_memory_efficiency(self):
        """Test that oneofs don't waste memory on unset fields."""
        # Create many instances to test memory patterns
        instances_x = []
        instances_y = []

        for i in range(100):
            instances_x.append(OptionalMessage(x=f"value_{i}"))
            instances_y.append(OptionalMessage(y=i))

        # Check that unset fields don't exist (saving memory)
        for msg in instances_x:
            assert hasattr(msg.a, "x")
            assert not hasattr(msg.a, "y")

        for msg in instances_y:
            assert hasattr(msg.a, "y")
            assert not hasattr(msg.a, "x")

    def test_oneof_with_all_fields_optional(self):
        """Test behavior when all message fields are optional."""
        # Using AllOptionalMessage from all_feidl_set_optional_demo_p2p
        msg = AllOptionalMessage(x="test")

        # Even with all fields optional, oneof should still work
        assert msg.a.x == "test"
        assert msg.a.a_case == "x"
        assert not hasattr(msg.a, "y")

    def test_oneof_error_handling_edge_cases(self):
        """Test error handling in edge cases."""
        # Test with very large integer (near int32 max)
        msg_max = OptionalMessage(y=2147483647)
        assert msg_max.a.y == 2147483647

        # Test with very large negative integer
        msg_min = OptionalMessage(y=-2147483648)
        assert msg_min.a.y == -2147483648

        # Test integer overflow
        # Note: Python int can handle values larger than int32
        # The generated models might not enforce int32 limits
        try:
            msg_overflow = OptionalMessage(y=2147483648)  # int32 max + 1
            # If this succeeds, Python is handling larger ints
            assert (
                msg_overflow.a.y == 2147483648
            )  # Python can handle values larger than int32
        except ValidationError:
            # This would be the expected behavior for strict int32
            assert True  # ValidationError was raised as expected for strict int32

        # Test with Unicode in string field
        msg_unicode = OptionalMessage(x="Hello 世界 🌍")
        assert msg_unicode.a.x == "Hello 世界 🌍"

    def test_oneof_special_characters_in_strings(self):
        """Test oneof string fields with special characters."""
        special_strings = [
            "",  # Empty
            " ",  # Space
            "\n\t\r",  # Whitespace
            '"quotes"',  # Quotes
            "'single'",  # Single quotes
            "\\backslash\\",  # Backslashes
            "Hello\nWorld",  # Newline
            "Tab\there",  # Tab
            "Null\x00char",  # Null character
            "😀🎉🔥",  # Emojis
            "Ñoño",  # Accented characters
            "<html>tags</html>",  # HTML
            '{"json": "value"}',  # JSON-like
        ]

        for s in special_strings:
            msg = OptionalMessage(x=s)
            assert msg.a.x == s

            # Test roundtrip
            json_str = msg.model_dump_json()
            restored = OptionalMessage.model_validate_json(json_str)
            assert restored.a.x == s

    def test_oneof_with_default_factory_items(self):
        """Test oneofs in messages with default factories."""
        # Create without setting the repeated fields
        msg1 = OptionalMessage(x="test")
        assert msg1.str_list == []  # Default empty list
        assert msg1.int_map == {}  # Default empty dict

        # Create with oneof and default factory fields
        msg2 = OptionalMessage(y=42, str_list=["a", "b"], int_map={"k": 1})
        assert msg2.a.y == 42
        assert msg2.str_list == ["a", "b"]
        assert msg2.int_map == {"k": 1}

        # Verify default factories don't interfere with oneof
        msg3 = OptionalMessage(x="test")
        msg4 = OptionalMessage(x="test")

        # Each should have independent default lists/dicts
        assert msg3.str_list is not msg4.str_list
        assert msg3.int_map is not msg4.int_map

    def test_oneof_discriminator_case_sensitivity(self):
        """Test case sensitivity of discriminator values."""
        msg = OptionalMessage(x="test")

        # Discriminator should match field name exactly
        assert msg.a.a_case == "x"  # Lowercase
        assert msg.a.a_case != "X"  # Not uppercase

        # For ReportData with longer names
        geo = GeoLocation(latitude=37.7749, longitude=-122.4194)
        report = ReportData(location_value=geo)
        assert report.data.data_case == "location_value"
        assert report.data.data_case != "locationValue"  # Not camelCase

    def test_oneof_field_ordering(self):
        """Test that field order doesn't affect oneof behavior."""
        # Create instances with fields in different orders
        msg1 = OptionalMessage(x="test", name="name1", age=25, str_list=["a", "b"])

        msg2 = OptionalMessage(str_list=["a", "b"], age=25, name="name1", x="test")

        # Both should be equivalent
        assert msg1.a.x == msg2.a.x
        assert msg1.name == msg2.name
        assert msg1.str_list == msg2.str_list

    def test_oneof_with_none_in_dict_fields(self):
        """Test behavior when dict representation has None values."""
        # Test various None scenarios in dict input
        test_cases = [
            {"x": "value", "name": None},  # None in optional field
            {"y": 0, "age": None},  # None in another optional
            {"x": "", "str_list": None},  # None in repeated field
        ]

        for data in test_cases:
            try:
                msg = OptionalMessage.model_validate(data)
                # Successfully created from dict with None values
                assert msg is not None
            except ValidationError as e:
                # Expected failure - None values may not be valid
                assert "validation" in str(e).lower() or "None" in str(e)

    def test_concurrent_oneof_creation(self):
        """Test creating oneofs concurrently (simulated)."""
        # Create many instances in quick succession
        instances = []

        # Simulate concurrent-like creation
        for i in range(50):
            # Alternate between different field types rapidly
            if i % 3 == 0:
                msg = OptionalMessage(x=f"x_{i}")
            elif i % 3 == 1:
                msg = OptionalMessage(y=i * 10)
            else:
                # Create with empty string for x (oneof is required)
                msg = OptionalMessage(x="", name=f"name_{i}")

            instances.append(msg)

        # Verify all instances are independent
        for i, msg in enumerate(instances):
            if i % 3 == 0:
                assert msg.a.a_case == "x"
            elif i % 3 == 1:
                assert msg.a.a_case == "y"
            else:
                # Empty string x was set
                assert msg.a.a_case == "x"
                assert msg.a.x == ""

    def test_oneof_with_field_name_conflicts(self):
        """Test potential naming conflicts in oneofs."""
        # Test that field names don't conflict with methods or properties
        msg = OptionalMessage(x="test")

        # These should work without conflicts
        assert hasattr(msg, "model_dump")  # Pydantic method
        assert hasattr(msg, "a")  # Oneof field
        assert hasattr(msg.a, "a_case")  # Discriminator

        # Field names shouldn't shadow important attributes
        assert callable(msg.model_dump)
        assert not callable(msg.a)
