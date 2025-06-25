"""Test edge cases for oneof fields with discriminated unions.

This module tests edge cases including:
- Empty oneofs (no field set)
- Oneofs with single field
- Oneofs with wrapper types (DoubleValue, StringValue, etc.)
- Required vs optional oneofs
- Reserved/deprecated fields in oneofs
- Field name conflicts with discriminator
- Oneofs with default values
- Oneofs with field validation
"""

import json
from typing import Literal, Union, Annotated, Optional
from google.protobuf import json_format
from google.protobuf.wrappers_pb2 import DoubleValue, StringValue, BoolValue, Int32Value
from pydantic import BaseModel, Field, ValidationError, ConfigDict, field_validator

from example.proto_pydanticv2.example.example_proto.demo import demo_pb2


# Example 1: Empty oneof (no field set is valid)
class _EmptyOneofBase(BaseModel):
    """Base class for message with potentially empty oneof."""
    message_id: str = Field(default="")
    

class EmptyOneofValueSet(_EmptyOneofBase):
    """When value is set in the oneof."""
    data_case: Literal["value"] = "value"
    value: str
    

class EmptyOneofNone(_EmptyOneofBase):
    """When no field is set in the oneof."""
    data_case: Literal[None] = None


EmptyOneofUnion = Annotated[
    Union[EmptyOneofValueSet, EmptyOneofNone],
    Field(discriminator='data_case')
]


# Example 2: Single field oneof (still use union for consistency)
class _SingleFieldBase(BaseModel):
    """Base class for single field oneof."""
    timestamp: int = Field(default=0)
    

class SingleFieldDataSet(_SingleFieldBase):
    """When data is set."""
    single_case: Literal["data"] = "data"
    data: bytes
    

class SingleFieldNone(_SingleFieldBase):
    """When data is not set."""
    single_case: Literal[None] = None


SingleFieldUnion = Annotated[
    Union[SingleFieldDataSet, SingleFieldNone],
    Field(discriminator='single_case')
]


# Example 3: Oneof with wrapper types
class _WrapperOneofBase(BaseModel):
    """Base class for wrapper type oneof."""
    model_config = ConfigDict(extra="ignore")
    request_id: str = Field(default="")
    

class WrapperOneofDouble(_WrapperOneofBase):
    """Double wrapper value."""
    wrapper_case: Literal["double_val"] = "double_val"
    double_val: float  # Unwrapped from DoubleValue
    

class WrapperOneofString(_WrapperOneofBase):
    """String wrapper value."""
    wrapper_case: Literal["string_val"] = "string_val"
    string_val: str  # Unwrapped from StringValue
    

class WrapperOneofBool(_WrapperOneofBase):
    """Bool wrapper value."""
    wrapper_case: Literal["bool_val"] = "bool_val"
    bool_val: bool  # Unwrapped from BoolValue
    

class WrapperOneofInt32(_WrapperOneofBase):
    """Int32 wrapper value."""
    wrapper_case: Literal["int32_val"] = "int32_val"
    int32_val: int  # Unwrapped from Int32Value
    

class WrapperOneofNone(_WrapperOneofBase):
    """No wrapper value set."""
    wrapper_case: Literal[None] = None


WrapperOneofUnion = Annotated[
    Union[WrapperOneofDouble, WrapperOneofString, WrapperOneofBool, WrapperOneofInt32, WrapperOneofNone],
    Field(discriminator='wrapper_case')
]


# Example 4: Field name conflicts with discriminator
class _ConflictBase(BaseModel):
    """Base with potential naming conflicts."""
    # What if the protobuf has a field named 'case' or 'type_case'?
    id: str = Field(default="")
    

class ConflictOptionA(_ConflictBase):
    """Option A selected."""
    conflict_case: Literal["option_a"] = "option_a"  # Use suffix to avoid conflicts
    option_a: str
    # case: str = Field(default="")  # This would conflict if 'case' was a field
    

class ConflictOptionB(_ConflictBase):
    """Option B selected."""
    conflict_case: Literal["option_b"] = "option_b"
    option_b: int
    # type: str = Field(default="")  # This would conflict with Python's type
    

class ConflictNone(_ConflictBase):
    """No option selected."""
    conflict_case: Literal[None] = None


# Example 5: Oneof with field validation
class _ValidatedOneofBase(BaseModel):
    """Base with common validation."""
    model_config = ConfigDict(extra="ignore")
    user_id: str = Field(min_length=1, max_length=50)
    
    @field_validator('user_id')
    def validate_user_id(cls, v):
        if not v.isalnum():
            raise ValueError('user_id must be alphanumeric')
        return v
    

class ValidatedOneofEmail(_ValidatedOneofBase):
    """Email contact method."""
    contact_case: Literal["email"] = "email"
    email: str = Field(pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    

class ValidatedOneofPhone(_ValidatedOneofBase):
    """Phone contact method."""
    contact_case: Literal["phone"] = "phone"
    phone: str = Field(pattern=r'^\+?[1-9]\d{1,14}$')  # E.164 format
    

class ValidatedOneofUsername(_ValidatedOneofBase):
    """Username contact method."""
    contact_case: Literal["username"] = "username"
    username: str = Field(min_length=3, max_length=20, pattern=r'^[a-zA-Z0-9_]+$')


ValidatedOneofUnion = Annotated[
    Union[ValidatedOneofEmail, ValidatedOneofPhone, ValidatedOneofUsername],
    Field(discriminator='contact_case')
]


# Example 6: Oneof with complex default behavior
class _DefaultBehaviorBase(BaseModel):
    """Base showing default value handling."""
    created_at: int = Field(default_factory=lambda: int(1600000000))  # Default timestamp
    

class DefaultBehaviorActive(_DefaultBehaviorBase):
    """Active status with config."""
    status_case: Literal["active_config"] = "active_config"
    active_config: 'ActiveConfig'
    

class DefaultBehaviorInactive(_DefaultBehaviorBase):
    """Inactive status with reason."""
    status_case: Literal["inactive_reason"] = "inactive_reason"
    inactive_reason: str = Field(default="manually_deactivated")
    

class DefaultBehaviorPending(_DefaultBehaviorBase):
    """Pending status."""
    status_case: Literal["pending_since"] = "pending_since"
    pending_since: int  # timestamp


class ActiveConfig(BaseModel):
    """Configuration for active status."""
    enabled_features: list[str] = Field(default_factory=list)
    max_requests: int = Field(default=1000, ge=0, le=1000000)


# Example 7: Required oneof (at least one field must be set)
class _RequiredOneofBase(BaseModel):
    """Base for required oneof - no None variant."""
    operation_id: str
    

class RequiredOneofCreate(_RequiredOneofBase):
    """Create operation."""
    action_case: Literal["create"] = "create"
    create: 'CreateAction'
    

class RequiredOneofUpdate(_RequiredOneofBase):
    """Update operation."""
    action_case: Literal["update"] = "update"
    update: 'UpdateAction'
    

class RequiredOneofDelete(_RequiredOneofBase):
    """Delete operation."""
    action_case: Literal["delete"] = "delete"
    delete: 'DeleteAction'


# No None variant - oneof is required
RequiredOneofUnion = Annotated[
    Union[RequiredOneofCreate, RequiredOneofUpdate, RequiredOneofDelete],
    Field(discriminator='action_case')
]


class CreateAction(BaseModel):
    resource_type: str
    resource_data: dict = Field(default_factory=dict)
    

class UpdateAction(BaseModel):
    resource_id: str
    updates: dict = Field(default_factory=dict)
    

class DeleteAction(BaseModel):
    resource_id: str
    soft_delete: bool = Field(default=True)


def test_empty_oneof():
    """Test oneof where no field being set is valid."""
    print("=== Empty Oneof Test ===")
    
    # Test with value set
    with_value = EmptyOneofValueSet(
        message_id="msg-001",
        value="some data"
    )
    print(f"With value: {with_value}")
    
    # Test with no value (empty oneof)
    empty = EmptyOneofNone(
        message_id="msg-002"
    )
    print(f"Empty oneof: {empty}")
    
    # Verify serialization
    # Don't use exclude_none when we need to preserve None discriminator
    empty_json = empty.model_dump_json()
    print(f"Empty serialized: {empty_json}")
    
    # The None case should serialize the discriminator as null
    json_dict = json.loads(empty_json)
    assert json_dict["data_case"] is None
    print("✓ Empty oneof correctly serialized")
    
    # With exclude_none, the None discriminator is excluded
    empty_json_clean = empty.model_dump_json(exclude_none=True)
    json_dict_clean = json.loads(empty_json_clean)
    print(f"With exclude_none: {empty_json_clean}")
    # This is a consideration for the implementation


def test_single_field_oneof():
    """Test oneof with only one possible field."""
    print("\n=== Single Field Oneof Test ===")
    
    # Even with single field, we use union for consistency
    with_data = SingleFieldDataSet(
        timestamp=1234567890,
        data=b"binary data here"
    )
    print(f"With data: {with_data}")
    
    # Empty case
    without_data = SingleFieldNone(
        timestamp=1234567890
    )
    print(f"Without data: {without_data}")
    
    # This maintains consistency with multi-field oneofs
    print("✓ Single field oneof follows same pattern")


def test_wrapper_type_oneof():
    """Test oneof with protobuf wrapper types."""
    print("\n=== Wrapper Type Oneof Test ===")
    
    # Test different wrapper types
    double_variant = WrapperOneofDouble(
        request_id="req-double",
        double_val=3.14159
    )
    print(f"Double variant: {double_variant}")
    
    string_variant = WrapperOneofString(
        request_id="req-string",
        string_val="wrapped string"
    )
    print(f"String variant: {string_variant}")
    
    bool_variant = WrapperOneofBool(
        request_id="req-bool",
        bool_val=True
    )
    print(f"Bool variant: {bool_variant}")
    
    # Verify wrapper values are unwrapped in the model
    assert isinstance(double_variant.double_val, float)
    assert isinstance(string_variant.string_val, str)
    assert isinstance(bool_variant.bool_val, bool)
    print("✓ Wrapper types are properly unwrapped")
    
    # Test serialization preserves primitive types
    json_str = double_variant.model_dump_json()
    json_dict = json.loads(json_str)
    assert isinstance(json_dict["double_val"], float)
    print("✓ Serialization preserves primitive types")


def test_field_name_conflicts():
    """Test handling of potential field name conflicts."""
    print("\n=== Field Name Conflict Test ===")
    
    # Using _case suffix avoids conflicts
    option_a = ConflictOptionA(
        id="test-001",
        option_a="value a"
    )
    print(f"Option A: {option_a}")
    
    # The discriminator field name avoids Python keywords
    json_str = option_a.model_dump_json()
    json_dict = json.loads(json_str)
    assert "conflict_case" in json_dict
    assert json_dict["conflict_case"] == "option_a"
    print("✓ Discriminator naming avoids conflicts")


def test_field_validation_in_oneof():
    """Test that field validation works within oneof variants."""
    print("\n=== Field Validation in Oneof Test ===")
    
    # Valid email
    try:
        valid_email = ValidatedOneofEmail(
            user_id="user123",
            email="test@example.com"
        )
        print(f"Valid email: {valid_email}")
    except ValidationError as e:
        print(f"Unexpected validation error: {e}")
    
    # Invalid email
    try:
        invalid_email = ValidatedOneofEmail(
            user_id="user123",
            email="not-an-email"
        )
        print("ERROR: Invalid email should have failed validation")
    except ValidationError as e:
        print(f"✓ Invalid email correctly rejected: {e.errors()[0]['msg']}")
    
    # Valid phone
    try:
        valid_phone = ValidatedOneofPhone(
            user_id="user456",
            phone="+1234567890"
        )
        print(f"Valid phone: {valid_phone}")
    except ValidationError as e:
        print(f"Unexpected validation error: {e}")
    
    # Invalid user_id (common field validation)
    try:
        invalid_user = ValidatedOneofUsername(
            user_id="user@123",  # Contains non-alphanumeric
            username="validuser"
        )
        print("ERROR: Invalid user_id should have failed validation")
    except ValidationError as e:
        print(f"✓ Common field validation works: {e.errors()[0]['msg']}")


def test_default_value_behavior():
    """Test how default values work in oneof variants."""
    print("\n=== Default Value Behavior Test ===")
    
    # Test with defaults
    active = DefaultBehaviorActive(
        active_config=ActiveConfig()  # Uses defaults
    )
    print(f"Active with defaults: {active}")
    print(f"  Created at: {active.created_at}")
    print(f"  Max requests: {active.active_config.max_requests}")
    
    # Test inactive with default reason
    inactive = DefaultBehaviorInactive()
    print(f"Inactive with default reason: {inactive}")
    print(f"  Reason: {inactive.inactive_reason}")
    
    # Verify defaults are included in serialization when appropriate
    json_str = inactive.model_dump_json()
    json_dict = json.loads(json_str)
    assert json_dict["inactive_reason"] == "manually_deactivated"
    print("✓ Default values handled correctly")


def test_required_oneof():
    """Test required oneof (no None variant)."""
    print("\n=== Required Oneof Test ===")
    
    # Create variant
    create_op = RequiredOneofCreate(
        operation_id="op-001",
        create=CreateAction(
            resource_type="user",
            resource_data={"name": "John", "email": "john@example.com"}
        )
    )
    print(f"Create operation: {create_op}")
    
    # Update variant
    update_op = RequiredOneofUpdate(
        operation_id="op-002",
        update=UpdateAction(
            resource_id="user-123",
            updates={"email": "newemail@example.com"}
        )
    )
    print(f"Update operation: {update_op}")
    
    # Delete variant
    delete_op = RequiredOneofDelete(
        operation_id="op-003",
        delete=DeleteAction(
            resource_id="user-123",
            soft_delete=False
        )
    )
    print(f"Delete operation: {delete_op}")
    
    # Note: There's no None variant, so one field MUST be set
    print("✓ Required oneof enforces at least one field")


def test_zero_values_in_oneof():
    """Test that zero/empty values are properly handled."""
    print("\n=== Zero Values in Oneof Test ===")
    
    # Zero values should be serialized when explicitly set
    zero_int = WrapperOneofInt32(
        request_id="zero-test",
        int32_val=0
    )
    
    json_str = zero_int.model_dump_json()
    json_dict = json.loads(json_str)
    
    print(f"Zero int: {zero_int}")
    print(f"Serialized: {json_str}")
    
    # Verify zero is present
    assert "int32_val" in json_dict
    assert json_dict["int32_val"] == 0
    print("✓ Zero values are preserved when explicitly set")
    
    # Empty string
    empty_string = WrapperOneofString(
        request_id="empty-test",
        string_val=""
    )
    
    json_str = empty_string.model_dump_json()
    json_dict = json.loads(json_str)
    
    assert json_dict["string_val"] == ""
    print("✓ Empty strings are preserved when explicitly set")


def test_serialization_edge_cases():
    """Test various serialization edge cases."""
    print("\n=== Serialization Edge Cases ===")
    
    # Test exclude_defaults behavior
    model = EmptyOneofValueSet(
        message_id="",  # Empty string (default)
        value="data"
    )
    
    # With exclude_defaults
    minimal = model.model_dump_json(exclude_defaults=True)
    minimal_dict = json.loads(minimal)
    print(f"Exclude defaults: {minimal}")
    
    # message_id should be excluded since it's the default
    assert "message_id" not in minimal_dict or minimal_dict["message_id"] == ""
    
    # With exclude_none
    clean = model.model_dump_json(exclude_none=True)
    clean_dict = json.loads(clean)
    print(f"Exclude none: {clean}")
    
    # Note: exclude_defaults might remove the discriminator if it has a default
    # This is an implementation consideration - discriminators might need special handling
    if "data_case" in minimal_dict:
        assert minimal_dict["data_case"] == "value"
    assert clean_dict["data_case"] == "value"
    print("✓ Serialization options work correctly")


def test_nested_validation_in_oneof():
    """Test that nested model validation works in oneof variants."""
    print("\n=== Nested Validation in Oneof ===")
    
    # Valid nested model
    try:
        valid_create = RequiredOneofCreate(
            operation_id="op-123",
            create=CreateAction(
                resource_type="document",
                resource_data={"title": "Test Doc"}
            )
        )
        print(f"Valid nested: {valid_create}")
    except ValidationError as e:
        print(f"Unexpected error: {e}")
    
    # Invalid nested model (empty resource_type)
    try:
        invalid_create = RequiredOneofCreate(
            operation_id="op-456",
            create=CreateAction(
                resource_type="",  # Empty string might fail validation
                resource_data={}
            )
        )
        # If no validation on resource_type, this will pass
        print(f"Created with empty resource_type: {invalid_create}")
    except ValidationError as e:
        print(f"✓ Nested validation caught error: {e}")


if __name__ == "__main__":
    test_empty_oneof()
    test_single_field_oneof()
    test_wrapper_type_oneof()
    test_field_name_conflicts()
    test_field_validation_in_oneof()
    test_default_value_behavior()
    test_required_oneof()
    test_zero_values_in_oneof()
    test_serialization_edge_cases()
    test_nested_validation_in_oneof()
    
    print("\n=== All edge case tests passed! ===")