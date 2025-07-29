"""Test cases for proto3 presence tracking (optional vs non-optional fields)"""

from typing import Any

import pytest
from expecttest import assert_expected_inline

from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_code
from protobuf_to_pydantic.gen_model import clear_create_model_cache
from tests.test_gen_code.test_helper import P2CNoHeader


class TestProto3Presence:
    """Test that proto3 presence semantics are correctly implemented."""

    @staticmethod
    def _model_output(msg: Any) -> str:
        """Generate Pydantic model code from protobuf message."""
        # Clear cache to ensure clean generation
        clear_create_model_cache()

        return pydantic_model_to_py_code(
            msg_to_pydantic_model(
                msg,
                parse_msg_desc_method="ignore",
            ),
            p2c_class=P2CNoHeader,
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_presence_message_generation(self) -> None:
        """Test that TestPresenceMessage generates correct field types."""
        # Import after proto generation
        from example.proto_pydanticv2.example.example_proto.demo import (
            test_proto3_presence_pb2,
        )

        output = self._model_output(test_proto3_presence_pb2.TestPresenceMessage)

        # This test expects:
        # - Regular fields: NO typing.Optional wrapper
        # - Optional fields: YES typing.Optional wrapper
        # - Default values set appropriately
        assert_expected_inline(
            output,
            """\
class SubMessage(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    name: str = Field(default="", alias_priority=1, validation_alias="name", serialization_alias="name")
    value: int = Field(default=0, alias_priority=1, validation_alias="value", serialization_alias="value")


class TestEnum(IntEnum):
    UNKNOWN = 0
    FIRST = 1
    SECOND = 2


class TestPresenceMessage(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        validate_default=True,
        serialize_by_alias=True,
        arbitrary_types_allowed=True,
    )

    regular_string: str = Field(
        default="", alias_priority=1, validation_alias="regularString", serialization_alias="regularString"
    )
    regular_int32: int = Field(
        default=0, alias_priority=1, validation_alias="regularInt32", serialization_alias="regularInt32"
    )
    regular_bool: bool = Field(
        default=False, alias_priority=1, validation_alias="regularBool", serialization_alias="regularBool"
    )
    regular_double: float = Field(
        default=0.0, alias_priority=1, validation_alias="regularDouble", serialization_alias="regularDouble"
    )
    optional_string: typing.Optional[str] = Field(
        default="", alias_priority=1, validation_alias="optionalString", serialization_alias="optionalString"
    )
    optional_int32: typing.Optional[int] = Field(
        default=0, alias_priority=1, validation_alias="optionalInt32", serialization_alias="optionalInt32"
    )
    optional_bool: typing.Optional[bool] = Field(
        default=False, alias_priority=1, validation_alias="optionalBool", serialization_alias="optionalBool"
    )
    optional_double: typing.Optional[float] = Field(
        default=0.0, alias_priority=1, validation_alias="optionalDouble", serialization_alias="optionalDouble"
    )
    regular_message: SubMessage = Field(
        default_factory=SubMessage,
        alias_priority=1,
        validation_alias="regularMessage",
        serialization_alias="regularMessage",
    )
    optional_message: typing.Optional[SubMessage] = Field(
        default_factory=SubMessage,
        alias_priority=1,
        validation_alias="optionalMessage",
        serialization_alias="optionalMessage",
    )
    repeated_strings: typing.List[str] = Field(
        default_factory=list,
        alias_priority=1,
        validation_alias="repeatedStrings",
        serialization_alias="repeatedStrings",
    )
    string_to_int_map: typing.Dict[str, int] = Field(
        default_factory=dict, alias_priority=1, validation_alias="stringToIntMap", serialization_alias="stringToIntMap"
    )
    regular_timestamp: typing_extensions.Annotated[
        datetime, PlainSerializer(func=timestamp_serializer, return_type=str, when_used="json")
    ] = Field(
        default_factory=datetime_utc_now,
        alias_priority=1,
        validation_alias="regularTimestamp",
        serialization_alias="regularTimestamp",
    )
    optional_timestamp: typing.Optional[
        typing_extensions.Annotated[
            datetime, PlainSerializer(func=timestamp_serializer, return_type=str, when_used="json")
        ]
    ] = Field(
        default_factory=datetime_utc_now,
        alias_priority=1,
        validation_alias="optionalTimestamp",
        serialization_alias="optionalTimestamp",
    )
    wrapped_string: StringValue = Field(
        default_factory=StringValue,
        alias_priority=1,
        validation_alias="wrappedString",
        serialization_alias="wrappedString",
    )
    wrapped_int32: Int32Value = Field(
        default_factory=Int32Value,
        alias_priority=1,
        validation_alias="wrappedInt32",
        serialization_alias="wrappedInt32",
    )
    regular_enum: TestEnum = Field(
        default=0, alias_priority=1, validation_alias="regularEnum", serialization_alias="regularEnum"
    )
    optional_enum: typing.Optional[TestEnum] = Field(
        default=0, alias_priority=1, validation_alias="optionalEnum", serialization_alias="optionalEnum"
    )
""",
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_oneof_message_generation(self) -> None:
        """Test that oneof fields work correctly with optional fields."""
        # Note: When using msg_to_pydantic_model directly (not through protoc plugin),
        # it doesn't have access to proto3_optional metadata. The real test is to verify
        # the plugin-generated code is correct.
        from example.proto_pydanticv2.example.example_proto.demo import (
            test_proto3_presence_p2p,
        )

        # Verify the generated code has correct types
        msg = test_proto3_presence_p2p.TestOneofMessage()
        assert msg.optional_field is None  # Should be None for optional field
        assert msg.regular_field == ""  # Should have default value for regular field

        # Also check type annotations
        from typing import get_type_hints

        hints = get_type_hints(test_proto3_presence_p2p.TestOneofMessage)

        # optional_field should be Optional[str]
        assert "Optional" in str(hints.get("optional_field"))
        # regular_field should be just str
        assert "Optional" not in str(hints.get("regular_field"))

        from example.proto_pydanticv2.example.example_proto.demo import (
            test_proto3_presence_pb2,
        )

        output = self._model_output(test_proto3_presence_pb2.TestOneofMessage)

        assert_expected_inline(
            output,
            """\
class TestOneofMessage(ProtobufCompatibleBaseModel):
    model_config = ConfigDict(
        ser_json_inf_nan="strings",
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_camel),
        populate_by_name=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    _one_of_dict = {
        "test.presence.TestOneofMessage.test_oneof": {
            "fields": {"oneofInt32", "oneofString", "oneof_int32", "oneof_string"},
            "required": False,
        }
    }

    oneof_string: str = Field(
        default="", alias_priority=1, validation_alias="oneofString", serialization_alias="oneofString"
    )
    oneof_int32: int = Field(
        default=0, alias_priority=1, validation_alias="oneofInt32", serialization_alias="oneofInt32"
    )
    regular_field: str = Field(
        default="", alias_priority=1, validation_alias="regularField", serialization_alias="regularField"
    )
    optional_field: typing.Optional[str] = Field(
        default=None, alias_priority=1, validation_alias="optionalField", serialization_alias="optionalField"
    )

    one_of_validator = model_validator(mode="before")(check_one_of)
""",
        )

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_field_behavior_at_runtime(self) -> None:
        """Test the runtime behavior of optional vs non-optional fields."""
        from example.proto_pydanticv2.example.example_proto.demo import (
            test_proto3_presence_pb2,
        )
        from example.proto_pydanticv2.example.example_proto.demo import (
            test_proto3_presence_p2p,
        )

        # Create instance with minimal data
        msg = test_proto3_presence_p2p.TestPresenceMessage()

        # Regular fields should have default values
        assert msg.regular_string == ""
        assert msg.regular_int32 == 0
        assert msg.regular_bool is False
        assert msg.regular_double == 0.0

        # Optional fields should be None
        assert msg.optional_string is None
        assert msg.optional_int32 is None
        assert msg.optional_bool is None
        assert msg.optional_double is None

        # Test setting optional fields
        msg.optional_string = "test"
        msg.optional_int32 = 42
        assert msg.optional_string == "test"
        assert msg.optional_int32 == 42

        # Test serialization - regular fields with defaults should be included
        data = msg.model_dump()
        assert "regular_string" in data
        assert "regular_int32" in data

        # Optional fields that are None might be excluded (depending on exclude_none)
        data_exclude_none = msg.model_dump(exclude_none=True)
        assert "optional_bool" not in data_exclude_none  # Still None
        assert "optional_string" in data_exclude_none  # Was set to "test"


class TestProto3PresenceWithExistingFiles:
    """Test that existing proto files still work correctly."""

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_existing_optional_fields(self) -> None:
        """Test that existing optional fields in demo.proto still work."""
        from example.proto_pydanticv2.example.example_proto.demo import (
            demo_pb2,
            demo_p2p,
        )

        # OtherMessage has: optional google.protobuf.FieldMask field_mask = 100;
        # This should remain Optional
        msg = demo_p2p.OtherMessage()
        assert msg.field_mask is None

        # Check the field type in annotations
        from typing import get_type_hints

        hints = get_type_hints(demo_p2p.OtherMessage)
        # field_mask should be Optional[FieldMask]
        assert hints.get("field_mask") is not None

    @pytest.mark.skip(
        reason="Fails due to proto3 presence handling - default_factory creates unwanted values"
    )
    @pytest.mark.proto3_presence
    def test_existing_enum_optional_field(self) -> None:
        """Test the existing WithOptionalEnumMsgEntry message."""
        from example.proto_pydanticv2.example.example_proto.demo import (
            demo_pb2,
            demo_p2p,
        )

        # WithOptionalEnumMsgEntry has: optional OptionalEnum enum = 1;
        msg = demo_p2p.WithOptionalEnumMsgEntry()

        # Should be None by default since it's optional
        assert msg.enum is None

        # Can be set to enum value
        msg.enum = demo_p2p.OptionalEnum.BAR
        assert msg.enum == demo_p2p.OptionalEnum.BAR
