"""
Base test classes for protobuf to pydantic testing.

Provides common test functionality through inheritance.
"""

import json
from typing import Any, Type, Optional, Dict
from google.protobuf import json_format
from google.protobuf.message import Message
from pydantic import BaseModel
from protobuf_to_pydantic import msg_to_pydantic_model


class RoundTripTestBase:
    """Base class for round-trip conversion tests."""

    @staticmethod
    def protobuf_to_json(
        msg: Message,
        use_integers_for_enums: bool = True,
        always_print_fields_with_no_presence: bool = True,
        preserving_proto_field_name: bool = False,
        sort_keys: bool = False,
        indent: Optional[int] = None,
    ) -> str:
        """Convert protobuf message to JSON string with configurable options."""
        return json_format.MessageToJson(
            msg,
            use_integers_for_enums=use_integers_for_enums,
            always_print_fields_with_no_presence=always_print_fields_with_no_presence,
            preserving_proto_field_name=preserving_proto_field_name,
            sort_keys=sort_keys,
            indent=indent,
        )

    @staticmethod
    def json_to_protobuf(json_str: str, msg_class: Type[Message]) -> Message:
        """Convert JSON string to protobuf message."""
        msg = msg_class()
        json_format.Parse(json_str, msg)
        return msg

    @staticmethod
    def pydantic_to_json(
        model: BaseModel,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> str:
        """Convert Pydantic model to JSON string with configurable options."""
        return model.model_dump_json(
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    @staticmethod
    def json_to_pydantic(json_str: str, model_class: Type[BaseModel]) -> BaseModel:
        """Convert JSON string to Pydantic model."""
        return model_class.model_validate_json(json_str)

    def verify_roundtrip(
        self,
        proto_msg: Message,
        pydantic_model_class: Type[BaseModel],
        use_integers_for_enums: bool = True,
        custom_assertions: Optional[callable] = None,
    ) -> None:
        """
        Verify that data survives the complete roundtrip.

        Args:
            proto_msg: The protobuf message to test
            pydantic_model_class: The corresponding Pydantic model class
            use_integers_for_enums: Whether to use integers for enum serialization
            custom_assertions: Optional function to perform custom assertions on the models
        """
        # Step 1: Protobuf -> JSON
        proto_json = self.protobuf_to_json(proto_msg, use_integers_for_enums)

        # Step 2: JSON -> Pydantic
        pydantic_model = self.json_to_pydantic(proto_json, pydantic_model_class)

        # Step 3: Pydantic -> JSON
        pydantic_json = self.pydantic_to_json(pydantic_model)

        # Step 4: JSON -> Protobuf
        reconstructed_msg = self.json_to_protobuf(pydantic_json, type(proto_msg))

        # Verify the round trip was successful
        final_json = self.protobuf_to_json(reconstructed_msg, use_integers_for_enums)

        # Compare JSONs
        original_dict = json.loads(proto_json)
        final_dict = json.loads(final_json)

        # Handle optional fields
        self._normalize_optional_fields(proto_msg, original_dict, final_dict)

        assert original_dict == final_dict, (
            f"Round-trip failed:\\nOriginal: {original_dict}\\nFinal: {final_dict}"
        )

        # Run custom assertions if provided
        if custom_assertions:
            custom_assertions(proto_msg, pydantic_model, reconstructed_msg)

    def _normalize_optional_fields(
        self, proto_msg: Message, original_dict: dict, final_dict: dict
    ) -> None:
        """Remove unset optional fields from final dict for comparison."""
        msg_descriptor = proto_msg.DESCRIPTOR
        optional_fields = set()

        for field in msg_descriptor.fields:
            if field.has_presence:
                json_name = (
                    field.json_name if hasattr(field, "json_name") else field.name
                )
                optional_fields.add(json_name)

        for key in list(final_dict.keys()):
            if key not in original_dict and key in optional_fields:
                final_dict.pop(key)


class ModelGenerationTestBase:
    """Base class for model generation tests."""

    @staticmethod
    def create_pydantic_model(
        msg_class: Type[Message],
        parse_msg_desc_method: str = "ignore",
        local_dict: Optional[Dict[str, Any]] = None,
    ) -> Type[BaseModel]:
        """Create a Pydantic model from a protobuf message class."""
        return msg_to_pydantic_model(
            msg_class,
            parse_msg_desc_method=parse_msg_desc_method,
            local_dict=local_dict,
        )

    @staticmethod
    def assert_field_exists(model_class: Type[BaseModel], field_name: str):
        """Assert that a field exists in the Pydantic model."""
        assert field_name in model_class.model_fields, (
            f"Field '{field_name}' not found in {model_class.__name__}"
        )

    @staticmethod
    def assert_field_type(
        model_class: Type[BaseModel], field_name: str, expected_type: Type
    ):
        """Assert that a field has the expected type."""
        field = model_class.model_fields.get(field_name)
        assert field is not None, f"Field '{field_name}' not found"
        # Handle Optional types and other complex type annotations
        field_type = field.annotation
        if hasattr(field_type, "__origin__"):
            # For generic types like Optional[str], List[int], etc.
            assert expected_type in field_type.__args__, (
                f"Field '{field_name}' type mismatch. "
                f"Expected {expected_type} in {field_type}"
            )
        else:
            assert field_type == expected_type, (
                f"Field '{field_name}' type mismatch. "
                f"Expected {expected_type}, got {field_type}"
            )


class ProtobufSpecComplianceTestBase:
    """Base class for protobuf specification compliance tests."""

    @staticmethod
    def assert_json_format_compliance(
        proto_msg: Message, expected_json: dict, use_integers_for_enums: bool = True
    ):
        """Assert that protobuf JSON format matches expected output."""
        json_str = json_format.MessageToJson(
            proto_msg,
            use_integers_for_enums=use_integers_for_enums,
            always_print_fields_with_no_presence=True,
        )
        actual_json = json.loads(json_str)

        assert actual_json == expected_json, (
            f"JSON format non-compliant:\\nActual: {actual_json}\\nExpected: {expected_json}"
        )

    @staticmethod
    def assert_accepts_json_input(
        msg_class: Type[Message],
        json_input: str,
        verify_func: Optional[callable] = None,
    ):
        """Assert that protobuf accepts specific JSON input."""
        try:
            msg = msg_class()
            json_format.Parse(json_input, msg)
            if verify_func:
                verify_func(msg)
        except json_format.ParseError as e:
            pytest.fail(f"Failed to parse valid JSON: {e}")


class ComprehensiveTestBase(
    RoundTripTestBase, ModelGenerationTestBase, ProtobufSpecComplianceTestBase
):
    """Comprehensive base class combining all test functionality."""

    pass
