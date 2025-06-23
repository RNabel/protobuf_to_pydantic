import json
from typing import Any, Dict

from google.protobuf import json_format, __version__
from google.protobuf.message import Message
from pydantic import BaseModel

if __version__ > "4.0.0":
    from example.proto_pydanticv2.example.example_proto.demo import (
        basic_types_roundtrip_pb2,
    )
else:
    from example.proto_3_20_pydanticv2.example.example_proto.demo import (
        basic_types_roundtrip_pb2,
    )

from protobuf_to_pydantic import msg_to_pydantic_model

# Import the pre-generated Pydantic models
if __version__ > "4.0.0":
    from example.proto_pydanticv2.example.example_proto.demo import (
        basic_types_roundtrip_p2p,
    )
else:
    from example.proto_3_20_pydanticv2.example.example_proto.demo import (
        basic_types_roundtrip_p2p,
    )


class TestBasicTypesRoundTrip:
    """Test round-trip conversion between Protobuf messages and Pydantic models for all basic types."""

    @staticmethod
    def _create_pydantic_model(msg_class: Any) -> type[BaseModel]:
        """Create a Pydantic model from a protobuf message class."""
        return msg_to_pydantic_model(msg_class, parse_msg_desc_method="ignore")

    @staticmethod
    def _protobuf_to_json(msg: Message) -> str:
        """Convert protobuf message to JSON string."""
        return json_format.MessageToJson(
            msg, always_print_fields_with_no_presence=True, use_integers_for_enums=True
        )

    @staticmethod
    def _json_to_protobuf(json_str: str, msg_class: Any) -> Message:
        """Convert JSON string to protobuf message."""
        msg = msg_class()
        json_format.Parse(json_str, msg)
        return msg

    @staticmethod
    def _pydantic_to_json(model: BaseModel) -> str:
        """Convert Pydantic model to JSON string."""
        return model.model_dump_json(by_alias=True)

    @staticmethod
    def _json_to_pydantic(json_str: str, model_class: type[BaseModel]) -> BaseModel:
        """Convert JSON string to Pydantic model."""
        return model_class.model_validate_json(json_str)

    def _test_roundtrip(self, msg: Message, test_data: Dict[str, Any]) -> None:
        """Test round-trip conversion for a message with test data."""
        # Clear the message first
        msg.Clear()

        # Set test data on protobuf message
        for field, value in test_data.items():
            if hasattr(msg, field):
                field_descriptor = msg.DESCRIPTOR.fields_by_name[field]
                if field_descriptor.label == field_descriptor.LABEL_REPEATED:
                    # For repeated fields, extend the list
                    getattr(msg, field).extend(value)
                else:
                    setattr(msg, field, value)

        # Step 1: Protobuf -> JSON
        proto_json = self._protobuf_to_json(msg)

        # Step 2: Create Pydantic model and parse JSON
        model_class = self._create_pydantic_model(type(msg))
        pydantic_model = self._json_to_pydantic(proto_json, model_class)

        # Step 3: Pydantic -> JSON
        pydantic_json = self._pydantic_to_json(pydantic_model)

        # Step 4: JSON -> Protobuf
        reconstructed_msg = self._json_to_protobuf(pydantic_json, type(msg))

        # Verify the round trip was successful
        final_json = self._protobuf_to_json(reconstructed_msg)

        # Parse both JSONs to compare as dicts (to ignore ordering differences)
        original_dict = json.loads(proto_json)
        final_dict = json.loads(final_json)

        # For comparison, we need to handle optional fields properly
        # The Pydantic model will include optional fields with their defaults,
        # but the original protobuf might not have them set
        # So we normalize by only comparing fields that were in the original
        msg_descriptor = msg.DESCRIPTOR
        optional_fields = set()

        # Identify which fields are optional (have the optional label in proto3)
        for field in msg_descriptor.fields:
            if field.has_presence:
                # Convert field name to camelCase for JSON comparison
                json_name = (
                    field.json_name if hasattr(field, "json_name") else field.name
                )
                optional_fields.add(json_name)

        for key in list(final_dict.keys()):
            if key not in original_dict and key in optional_fields:
                # This is an optional field that wasn't set in the original
                final_dict.pop(key)

        assert original_dict == final_dict, (
            f"Round-trip failed:\nOriginal: {original_dict}\nFinal: {final_dict}"
        )

    def test_basic_int32(self):
        """Test int32 field round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            {"int32_field": 0},
            {"int32_field": 42},
            {"int32_field": -42},
            {"int32_field": 2147483647},  # max int32
            {"int32_field": -2147483648},  # min int32
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_basic_int64(self):
        """Test int64 field round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            {"int64_field": 0},
            {"int64_field": 42},
            {"int64_field": -42},
            {"int64_field": 9223372036854775807},  # max int64
            {"int64_field": -9223372036854775808},  # min int64
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_basic_uint32(self):
        """Test uint32 field round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            {"uint32_field": 0},
            {"uint32_field": 42},
            {"uint32_field": 4294967295},  # max uint32
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_basic_uint64(self):
        """Test uint64 field round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            {"uint64_field": 0},
            {"uint64_field": 42},
            {"uint64_field": 18446744073709551615},  # max uint64
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_basic_sint32(self):
        """Test sint32 field round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            {"sint32_field": 0},
            {"sint32_field": 42},
            {"sint32_field": -42},
            {"sint32_field": 2147483647},  # max sint32
            {"sint32_field": -2147483648},  # min sint32
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_basic_sint64(self):
        """Test sint64 field round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            {"sint64_field": 0},
            {"sint64_field": 42},
            {"sint64_field": -42},
            {"sint64_field": 9223372036854775807},  # max sint64
            {"sint64_field": -9223372036854775808},  # min sint64
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_basic_fixed32(self):
        """Test fixed32 field round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            {"fixed32_field": 0},
            {"fixed32_field": 42},
            {"fixed32_field": 4294967295},  # max fixed32
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_basic_fixed64(self):
        """Test fixed64 field round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            {"fixed64_field": 0},
            {"fixed64_field": 42},
            {"fixed64_field": 18446744073709551615},  # max fixed64
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_basic_sfixed32(self):
        """Test sfixed32 field round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            {"sfixed32_field": 0},
            {"sfixed32_field": 42},
            {"sfixed32_field": -42},
            {"sfixed32_field": 2147483647},  # max sfixed32
            {"sfixed32_field": -2147483648},  # min sfixed32
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_basic_sfixed64(self):
        """Test sfixed64 field round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            {"sfixed64_field": 0},
            {"sfixed64_field": 42},
            {"sfixed64_field": -42},
            {"sfixed64_field": 9223372036854775807},  # max sfixed64
            {"sfixed64_field": -9223372036854775808},  # min sfixed64
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_basic_float(self):
        """Test float field round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            {"float_field": 0.0},
            {"float_field": 3.14},
            {"float_field": -3.14},
            {"float_field": 1e-6},
            {"float_field": 1e6},
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_basic_double(self):
        """Test double field round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            {"double_field": 0.0},
            {"double_field": 3.141592653589793},
            {"double_field": -3.141592653589793},
            {"double_field": 1e-15},
            {"double_field": 1e15},
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_basic_bool(self):
        """Test bool field round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            {"bool_field": True},
            {"bool_field": False},
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_basic_string(self):
        """Test string field round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            {"string_field": ""},
            {"string_field": "hello"},
            {"string_field": "Hello, World!"},
            {"string_field": "Special chars: !@#$%^&*()"},
            {"string_field": "Unicode: αβγδε"},
            {"string_field": "Emoji: 😀🎉🚀"},
            {"string_field": "Escaped chars: \n\t\r\"'\\"},
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_basic_bytes(self):
        """Test bytes field round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            {"bytes_field": b""},
            {"bytes_field": b"hello"},
            {"bytes_field": b"\x00\x01\x02\x03\xff"},
            {"bytes_field": b"binary data \x00 with nulls"},
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_repeated_fields(self):
        """Test repeated fields round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            # Empty lists
            {"repeated_int32": []},
            {"repeated_string": []},
            {"repeated_bool": []},
            # Single element lists
            {"repeated_int32": [42]},
            {"repeated_string": ["hello"]},
            {"repeated_bool": [True]},
            # Multiple element lists
            {"repeated_int32": [1, 2, 3, -1, 0]},
            {"repeated_int64": [1000000000000, -1000000000000, 0]},
            {"repeated_uint32": [0, 1, 2, 3, 4294967295]},
            {"repeated_uint64": [0, 1, 2, 3, 18446744073709551614]},
            {"repeated_float": [0.0, 1.1, -2.2, 3.14159]},
            {"repeated_double": [0.0, 1.1, -2.2, 3.141592653589793]},
            {"repeated_bool": [True, False, True, False]},
            {"repeated_string": ["", "hello", "world", "unicode: αβγ", "emoji: 😀"]},
            {"repeated_bytes": [b"", b"hello", b"\x00\x01\x02", b"binary"]},
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_optional_fields(self):
        """Test optional fields round-trip."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_cases = [
            # Not set (should use defaults)
            {},
            # Set to non-default values
            {"optional_int32": 42},
            {"optional_string": "hello"},
            {"optional_bool": True},
            # Set to default-like values
            {"optional_int32": 0},
            {"optional_string": ""},
            {"optional_bool": False},
        ]

        for test_data in test_cases:
            self._test_roundtrip(msg, test_data)

    def test_all_fields_together(self):
        """Test all fields together in one message."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        test_data = {
            # Basic numeric types
            "int32_field": 42,
            "int64_field": 1000000000000,
            "uint32_field": 100,
            "uint64_field": 2000000000000,
            "sint32_field": -42,
            "sint64_field": -1000000000000,
            "fixed32_field": 1000,
            "fixed64_field": 3000000000000,
            "sfixed32_field": -1000,
            "sfixed64_field": -3000000000000,
            # Floating point
            "float_field": 3.14,
            "double_field": 3.141592653589793,
            # Boolean
            "bool_field": True,
            # String and bytes
            "string_field": "Hello, World! 😀",
            "bytes_field": b"binary data \x00\x01\x02",
            # Repeated fields
            "repeated_int32": [1, 2, 3],
            "repeated_string": ["a", "b", "c"],
            "repeated_bool": [True, False, True],
            # Optional fields
            "optional_int32": 999,
            "optional_string": "optional value",
            "optional_bool": False,
        }

        self._test_roundtrip(msg, test_data)

    def test_edge_cases(self):
        """Test edge cases with special values (excluding inf/nan due to Pydantic JSON limitations)."""
        msg = basic_types_roundtrip_pb2.EdgeCasesMessage()

        # Test min/max values but exclude special float values (inf/nan)
        # due to Pydantic JSON serialization limitations tracked in subtask 14.7
        test_data = {
            # Integer min/max values
            "min_int32": -2147483648,
            "max_int32": 2147483647,
            "min_int64": -9223372036854775808,
            "max_int64": 9223372036854775807,
            "min_uint32": 0,
            "max_uint32": 4294967295,
            "min_uint64": 0,
            "max_uint64": 18446744073709551614,  # max uint64 - 1 (to avoid float precision issues)
            # Regular float values (not special ones)
            "zero_float": 0.0,
            "negative_zero_float": -0.0,
            "zero_double": 0.0,
            "negative_zero_double": -0.0,
            # String edge cases
            "empty_string": "",
            "empty_bytes": b"",
            "unicode_string": "αβγδε АБВГД 中文 日本語",
            "emoji_string": "😀😁😂🤣😃😄😅😆😉😊",
        }

        self._test_roundtrip(msg, test_data)

    def test_field_name_conversion(self):
        """Test that field names are properly converted between camelCase and snake_case."""
        msg = basic_types_roundtrip_pb2.BasicTypesMessage()

        # Set some values
        msg.int32_field = 42
        msg.string_field = "test"
        msg.repeated_int32.extend([1, 2, 3])

        # Convert to JSON (should use camelCase)
        proto_json = self._protobuf_to_json(msg)
        json_dict = json.loads(proto_json)

        # Check that JSON uses camelCase
        assert "int32Field" in json_dict
        assert "stringField" in json_dict
        assert "repeatedInt32" in json_dict

        # Create Pydantic model and verify it can parse camelCase
        model_class = self._create_pydantic_model(type(msg))
        pydantic_model = self._json_to_pydantic(proto_json, model_class)

        # Verify Pydantic model has correct values
        assert pydantic_model.int32_field == 42
        assert pydantic_model.string_field == "test"
        assert pydantic_model.repeated_int32 == [1, 2, 3]

        # Convert back to JSON and verify camelCase is preserved
        pydantic_json = self._pydantic_to_json(pydantic_model)
        pydantic_dict = json.loads(pydantic_json)

        assert "int32Field" in pydantic_dict
        assert "stringField" in pydantic_dict
        assert "repeatedInt32" in pydantic_dict

    def test_protobuf_binary_to_pydantic_roundtrip(self):
        """Test round-trip conversion using protobuf binary serialization."""
        # Create and populate a protobuf message
        pb_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        pb_msg.int32_field = 42
        pb_msg.string_field = "Hello, World!"
        pb_msg.float_field = 3.14
        pb_msg.bool_field = True
        pb_msg.repeated_int32.extend([1, 2, 3])

        # Serialize to binary
        binary_data = pb_msg.SerializeToString()

        # Create a new protobuf message from binary
        pb_msg2 = basic_types_roundtrip_pb2.BasicTypesMessage()
        pb_msg2.ParseFromString(binary_data)

        # Convert to JSON then to Pydantic
        proto_json = self._protobuf_to_json(pb_msg2)
        model_class = self._create_pydantic_model(type(pb_msg2))
        pydantic_model = self._json_to_pydantic(proto_json, model_class)

        # Verify values
        assert pydantic_model.int32_field == 42
        assert pydantic_model.string_field == "Hello, World!"
        assert abs(pydantic_model.float_field - 3.14) < 0.0001
        assert pydantic_model.bool_field is True
        assert pydantic_model.repeated_int32 == [1, 2, 3]

        # Convert back to protobuf via JSON
        pydantic_json = self._pydantic_to_json(pydantic_model)
        pb_msg3 = self._json_to_protobuf(pydantic_json, type(pb_msg))

        # Verify the values are preserved (binary may differ due to optional fields)
        assert pb_msg3.int32_field == pb_msg.int32_field
        assert pb_msg3.string_field == pb_msg.string_field
        assert abs(pb_msg3.float_field - pb_msg.float_field) < 0.0001
        assert pb_msg3.bool_field == pb_msg.bool_field
        assert list(pb_msg3.repeated_int32) == list(pb_msg.repeated_int32)

    def test_static_pydantic_model_snake_case_input(self):
        """Test that static Pydantic models accept snake_case field names."""
        snake_case_data = {
            "int32_field": 100,
            "int64_field": 1000000,
            "string_field": "Static test",
            "bool_field": True,
            "float_field": 2.718,
            "repeated_string": ["a", "b", "c"],
            "optional_int32": 999,
        }

        # Create static Pydantic model with snake_case
        static_model = basic_types_roundtrip_p2p.BasicTypesMessage(**snake_case_data)

        # Verify values
        assert static_model.int32_field == 100
        assert static_model.int64_field == 1000000
        assert static_model.string_field == "Static test"
        assert static_model.bool_field is True
        assert static_model.float_field == 2.718
        assert static_model.repeated_string == ["a", "b", "c"]
        assert static_model.optional_int32 == 999

    def test_static_pydantic_model_camel_case_input(self):
        """Test that static Pydantic models accept camelCase field names via aliases."""
        camel_case_data = {
            "int32Field": 100,
            "int64Field": 1000000,
            "stringField": "Static test",
            "boolField": True,
            "floatField": 2.718,
            "repeatedString": ["a", "b", "c"],
            "optionalInt32": 999,
        }

        # Create static Pydantic model with camelCase
        static_model = basic_types_roundtrip_p2p.BasicTypesMessage(**camel_case_data)

        # Verify values
        assert static_model.int32_field == 100
        assert static_model.int64_field == 1000000
        assert static_model.string_field == "Static test"
        assert static_model.bool_field is True
        assert static_model.float_field == 2.718
        assert static_model.repeated_string == ["a", "b", "c"]
        assert static_model.optional_int32 == 999

    def test_static_pydantic_model_snake_and_camel_equivalence(self):
        """Test that models created with snake_case and camelCase inputs are equivalent."""
        test_data = {
            "snake": {
                "int32_field": 100,
                "string_field": "Test",
                "repeated_string": ["a", "b"],
            },
            "camel": {
                "int32Field": 100,
                "stringField": "Test",
                "repeatedString": ["a", "b"],
            },
        }

        snake_model = basic_types_roundtrip_p2p.BasicTypesMessage(**test_data["snake"])
        camel_model = basic_types_roundtrip_p2p.BasicTypesMessage(**test_data["camel"])

        # Verify both models have identical values
        assert snake_model.int32_field == camel_model.int32_field
        assert snake_model.string_field == camel_model.string_field
        assert snake_model.repeated_string == camel_model.repeated_string

    def test_static_pydantic_model_json_serialization_with_aliases(self):
        """Test JSON serialization with aliases produces camelCase output."""
        model = basic_types_roundtrip_p2p.BasicTypesMessage(
            int32_field=42,
            string_field="Test",
            repeated_int32=[1, 2, 3],
            optional_bool=True,
        )

        # Serialize with aliases
        json_output = model.model_dump_json(by_alias=True)
        json_dict = json.loads(json_output)

        # Verify camelCase keys
        assert "int32Field" in json_dict
        assert "stringField" in json_dict
        assert "repeatedInt32" in json_dict
        assert "optionalBool" in json_dict

        # Verify values
        assert json_dict["int32Field"] == 42
        assert json_dict["stringField"] == "Test"
        assert json_dict["repeatedInt32"] == [1, 2, 3]
        assert json_dict["optionalBool"] is True

    def test_static_pydantic_model_json_serialization_without_aliases(self):
        """Test JSON serialization without aliases produces snake_case output."""
        model = basic_types_roundtrip_p2p.BasicTypesMessage(
            int32_field=42,
            string_field="Test",
            repeated_int32=[1, 2, 3],
            optional_bool=True,
        )

        # Serialize without aliases
        json_output = model.model_dump_json(by_alias=False)
        json_dict = json.loads(json_output)

        # Verify snake_case keys
        assert "int32_field" in json_dict
        assert "string_field" in json_dict
        assert "repeated_int32" in json_dict
        assert "optional_bool" in json_dict

        # Verify values
        assert json_dict["int32_field"] == 42
        assert json_dict["string_field"] == "Test"
        assert json_dict["repeated_int32"] == [1, 2, 3]
        assert json_dict["optional_bool"] is True

    def test_static_pydantic_model_parse_camel_case_json(self):
        """Test that static models can parse JSON with camelCase field names."""
        camel_json = json.dumps(
            {
                "int32Field": 100,
                "stringField": "JSON test",
                "repeatedString": ["x", "y", "z"],
                "optionalInt32": 555,
            }
        )

        # Parse camelCase JSON
        model = basic_types_roundtrip_p2p.BasicTypesMessage.model_validate_json(
            camel_json
        )

        # Verify values
        assert model.int32_field == 100
        assert model.string_field == "JSON test"
        assert model.repeated_string == ["x", "y", "z"]
        assert model.optional_int32 == 555

    def test_static_pydantic_model_parse_snake_case_json(self):
        """Test that static models can parse JSON with snake_case field names."""
        snake_json = json.dumps(
            {
                "int32_field": 200,
                "string_field": "Snake JSON",
                "repeated_string": ["m", "n"],
                "optional_int32": 777,
            }
        )

        # Parse snake_case JSON
        model = basic_types_roundtrip_p2p.BasicTypesMessage.model_validate_json(
            snake_json
        )

        # Verify values
        assert model.int32_field == 200
        assert model.string_field == "Snake JSON"
        assert model.repeated_string == ["m", "n"]
        assert model.optional_int32 == 777

    def test_static_pydantic_model_protobuf_roundtrip(self):
        """Test full round-trip: Protobuf -> camelCase JSON -> Pydantic -> camelCase JSON -> Protobuf."""
        # Create protobuf message
        pb_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        pb_msg.int32_field = 42
        pb_msg.string_field = "Round trip test"
        pb_msg.bool_field = True
        pb_msg.repeated_int32.extend([1, 2, 3])
        pb_msg.optional_string = "Optional value"

        # Step 1: Protobuf to JSON (uses camelCase)
        proto_json = self._protobuf_to_json(pb_msg)
        proto_dict = json.loads(proto_json)

        # Verify protobuf JSON uses camelCase
        assert "int32Field" in proto_dict
        assert "stringField" in proto_dict
        assert "boolField" in proto_dict
        assert "repeatedInt32" in proto_dict
        assert "optionalString" in proto_dict

        # Step 2: Parse protobuf JSON into Pydantic model
        pydantic_model = (
            basic_types_roundtrip_p2p.BasicTypesMessage.model_validate_json(proto_json)
        )

        # Verify Pydantic model values
        assert pydantic_model.int32_field == 42
        assert pydantic_model.string_field == "Round trip test"
        assert pydantic_model.bool_field is True
        assert pydantic_model.repeated_int32 == [1, 2, 3]
        assert pydantic_model.optional_string == "Optional value"

        # Step 3: Serialize Pydantic to camelCase JSON
        pydantic_json = pydantic_model.model_dump_json(by_alias=True)

        # Step 4: Parse JSON back to protobuf
        pb_msg_final = self._json_to_protobuf(
            pydantic_json, basic_types_roundtrip_pb2.BasicTypesMessage
        )

        # Verify final protobuf matches original
        assert pb_msg_final.int32_field == pb_msg.int32_field
        assert pb_msg_final.string_field == pb_msg.string_field
        assert pb_msg_final.bool_field == pb_msg.bool_field
        assert list(pb_msg_final.repeated_int32) == list(pb_msg.repeated_int32)
        assert pb_msg_final.optional_string == pb_msg.optional_string

    def test_static_pydantic_model_compatibility_with_dynamic(self):
        """Test compatibility between static and dynamically generated Pydantic models."""
        # Create protobuf message
        pb_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        pb_msg.int32_field = 100
        pb_msg.int64_field = 1000000
        pb_msg.string_field = "Compatibility test"
        pb_msg.bool_field = True
        pb_msg.float_field = 2.718
        pb_msg.repeated_string.extend(["a", "b", "c"])
        pb_msg.optional_int32 = 999

        # Convert protobuf to JSON
        proto_json = self._protobuf_to_json(pb_msg)

        # Create static Pydantic model from protobuf JSON
        static_model = basic_types_roundtrip_p2p.BasicTypesMessage.model_validate_json(
            proto_json
        )

        # Create dynamic Pydantic model from protobuf
        dynamic_model_class = self._create_pydantic_model(type(pb_msg))
        dynamic_model = self._json_to_pydantic(proto_json, dynamic_model_class)

        # Compare values between static and dynamic models
        assert static_model.int32_field == dynamic_model.int32_field == 100
        assert static_model.int64_field == dynamic_model.int64_field == 1000000
        assert (
            static_model.string_field
            == dynamic_model.string_field
            == "Compatibility test"
        )
        assert static_model.bool_field == dynamic_model.bool_field is True
        assert abs(static_model.float_field - dynamic_model.float_field) < 0.0001
        assert (
            static_model.repeated_string
            == dynamic_model.repeated_string
            == ["a", "b", "c"]
        )
        assert static_model.optional_int32 == dynamic_model.optional_int32 == 999

    def test_cross_model_compatibility(self):
        """Test that dynamically generated and static Pydantic models can work together."""
        # Start with protobuf
        pb_msg = basic_types_roundtrip_pb2.BasicTypesMessage()
        pb_msg.int32_field = 42
        pb_msg.string_field = "Compatibility test"
        pb_msg.repeated_bool.extend([True, False, True])

        # Convert to JSON
        proto_json = self._protobuf_to_json(pb_msg)

        # Parse with dynamic model
        dynamic_model_class = self._create_pydantic_model(type(pb_msg))
        dynamic_model = self._json_to_pydantic(proto_json, dynamic_model_class)

        # Extract data from dynamic model (converting from camelCase)
        dynamic_dict = json.loads(self._pydantic_to_json(dynamic_model))

        # Convert camelCase keys to snake_case for static model
        snake_case_dict = {}
        for key, value in dynamic_dict.items():
            # Simple camelCase to snake_case conversion
            snake_key = "".join(
                ["_" + c.lower() if c.isupper() else c for c in key]
            ).lstrip("_")
            snake_case_dict[snake_key] = value

        # Create static model from the data
        static_model = basic_types_roundtrip_p2p.BasicTypesMessage(**snake_case_dict)

        # Verify values match
        assert static_model.int32_field == 42
        assert static_model.string_field == "Compatibility test"
        assert static_model.repeated_bool == [True, False, True]

    def test_special_float_values_protobuf_only(self):
        """Test that protobuf correctly handles special float values in binary serialization."""
        pb_msg = basic_types_roundtrip_pb2.EdgeCasesMessage()

        # Set special float values
        pb_msg.infinity_float = float("inf")
        pb_msg.negative_infinity_float = float("-inf")
        pb_msg.nan_float = float("nan")
        pb_msg.infinity_double = float("inf")
        pb_msg.negative_infinity_double = float("-inf")
        pb_msg.nan_double = float("nan")

        # Binary serialization round-trip
        binary_data = pb_msg.SerializeToString()
        pb_msg2 = basic_types_roundtrip_pb2.EdgeCasesMessage()
        pb_msg2.ParseFromString(binary_data)

        # Verify special values are preserved in binary serialization
        assert pb_msg2.infinity_float == float("inf")
        assert pb_msg2.negative_infinity_float == float("-inf")
        assert pb_msg2.infinity_double == float("inf")
        assert pb_msg2.negative_infinity_double == float("-inf")

        # NaN is special - it's not equal to itself, so we use isnan
        import math

        assert math.isnan(pb_msg2.nan_float)
        assert math.isnan(pb_msg2.nan_double)

    def test_special_float_values_json_handling(self):
        """Test how special float values are handled in JSON serialization."""
        pb_msg = basic_types_roundtrip_pb2.EdgeCasesMessage()

        # Set special float values
        pb_msg.infinity_float = float("inf")
        pb_msg.negative_infinity_float = float("-inf")
        pb_msg.nan_float = float("nan")

        # Convert to JSON
        proto_json = self._protobuf_to_json(pb_msg)
        json_dict = json.loads(proto_json)

        # Protobuf JSON format uses strings for special values
        assert json_dict.get("infinityFloat") == "Infinity"
        assert json_dict.get("negativeInfinityFloat") == "-Infinity"
        assert json_dict.get("nanFloat") == "NaN"

        # Test protobuf's ability to parse these back
        pb_msg2 = self._json_to_protobuf(proto_json, type(pb_msg))

        # Verify protobuf correctly parses the special string values
        assert pb_msg2.infinity_float == float("inf")
        assert pb_msg2.negative_infinity_float == float("-inf")
        import math

        assert math.isnan(pb_msg2.nan_float)

    def test_pydantic_special_float_values_limitation(self):
        """Document the known limitation with special float values in Pydantic JSON serialization.

        This test demonstrates that special float values (inf, -inf, nan) are not properly
        preserved through Pydantic JSON serialization. This is tracked in subtask 14.7.
        """
        pb_msg = basic_types_roundtrip_pb2.EdgeCasesMessage()

        # Set special float values
        pb_msg.infinity_float = float("inf")
        pb_msg.negative_infinity_float = float("-inf")
        pb_msg.nan_float = float("nan")

        # Convert to JSON (protobuf correctly serializes as strings)
        proto_json = self._protobuf_to_json(pb_msg)
        json_dict = json.loads(proto_json)
        assert json_dict["infinityFloat"] == "Infinity"
        assert json_dict["negativeInfinityFloat"] == "-Infinity"
        assert json_dict["nanFloat"] == "NaN"

        # Create Pydantic model and parse the JSON
        model_class = self._create_pydantic_model(type(pb_msg))
        pydantic_model = self._json_to_pydantic(proto_json, model_class)

        # Check that Pydantic correctly parses the special string values
        assert pydantic_model.infinity_float == float("inf")
        assert pydantic_model.negative_infinity_float == float("-inf")
        import math

        assert math.isnan(pydantic_model.nan_float)

        # Now convert back to JSON from Pydantic
        pydantic_json = self._pydantic_to_json(pydantic_model)
        pydantic_json_dict = json.loads(pydantic_json)

        # Document the limitation: Pydantic serializes special floats as None
        assert pydantic_json_dict["infinityFloat"] is None
        assert pydantic_json_dict["negativeInfinityFloat"] is None
        assert pydantic_json_dict["nanFloat"] is None

        # When converted back to protobuf, these become 0.0
        pb_msg2 = self._json_to_protobuf(pydantic_json, type(pb_msg))
        assert pb_msg2.infinity_float == 0.0
        assert pb_msg2.negative_infinity_float == 0.0
        assert pb_msg2.nan_float == 0.0

        # This is a known limitation that needs to be fixed (subtask 14.7)
