"""Test to demonstrate the oneof roundtrip issue with Pydantic models."""

import json
from typing import List
from google.protobuf import json_format
from pydantic import BaseModel, Field, ValidationError

from example.proto_pydanticv2.example.example_proto.demo import demo_pb2
from example.proto_pydanticv2.demo_gen_code import OptionalMessage


def test_oneof_roundtrip_issue():
    """Demonstrates the issue where oneof fields don't roundtrip correctly.
    
    The issue occurs because when a Pydantic model with oneof fields is dumped to JSON
    and then loaded back, the structure changes in a way that breaks validation.
    """
    # Create a protobuf message with oneof field set
    proto_msg = demo_pb2.OptionalMessage()
    proto_msg.x = "test_value"  # This sets the oneof to use 'x'
    
    # Convert protobuf to JSON
    proto_json = json_format.MessageToJson(
        proto_msg, 
        always_print_fields_with_no_presence=True,
        use_integers_for_enums=True
    )
    print(f"Protobuf JSON: {proto_json}")
    
    # Load into Pydantic model
    pydantic_model = OptionalMessage.model_validate_json(proto_json)
    print(f"Pydantic model: {pydantic_model}")
    
    # Dump Pydantic model to JSON
    pydantic_json = pydantic_model.model_dump_json()
    print(f"Pydantic JSON: {pydantic_json}")
    
    # Try to load back into Pydantic model - this might fail
    try:
        roundtrip_model = OptionalMessage.model_validate_json(pydantic_json)
        print(f"Roundtrip successful: {roundtrip_model}")
    except Exception as e:
        print(f"Roundtrip failed: {type(e).__name__}: {e}")
        
    # Let's also examine the structure difference
    proto_dict = json.loads(proto_json)
    pydantic_dict = json.loads(pydantic_json)
    
    print(f"\nProtobuf dict structure: {proto_dict}")
    print(f"Pydantic dict structure: {pydantic_dict}")
    
    # The issue is likely that protobuf represents oneofs differently than Pydantic expects
    # Let's see if the structure changes when we have nested messages or arrays


def test_oneof_with_arrays_issue():
    """Test to demonstrate a generic issue where list fields receive dict structures.
    
    This simulates a structure where:
    - string_list expects List[str] but gets {'values': []}
    - number_list expects List[int] but gets {'items': []}
    """
    # Create a mock structure that demonstrates the issue
    mock_data = {
        "string_list": {"values": []},  # This structure causes the issue
        "number_list": {"items": []}
    }
    
    # This demonstrates the type of error that would occur
    print(f"\nMock data that would fail validation:")
    print(f"Data: {json.dumps(mock_data, indent=2)}")
    print("Expected: string_list should be a list, not a dict with 'values' key")
    print("Expected: number_list should be a list, not a dict with 'items' key")
    
    # The issue is that during serialization, oneof fields might be wrapped
    # in an extra object layer that isn't expected during deserialization


class GenericListModel(BaseModel):
    """Generic model to demonstrate the list/dict validation issue."""
    string_list: List[str] = Field(default_factory=list)
    number_list: List[int] = Field(default_factory=list)


def test_generic_list_validation_error():
    """Demonstrates validation error when list fields receive dict structures.
    
    When a Pydantic model expects List fields but receives dict structures
    with nested keys, validation fails.
    """
    # This is what the model expects
    correct_data = {
        "string_list": ["hello", "world"],
        "number_list": [123, 456]
    }
    
    # This works fine
    try:
        model1 = GenericListModel.model_validate(correct_data)
        print(f"Correct validation successful: {model1}")
        print(f"JSON dump: {model1.model_dump_json()}")
        
        # Roundtrip works with correct structure
        model2 = GenericListModel.model_validate_json(model1.model_dump_json())
        print(f"Roundtrip successful: {model2}")
    except ValidationError as e:
        print(f"Unexpected error with correct data: {e}")
    
    print("\n--- Now testing with problematic structure ---")
    
    # This is what might come from a protobuf with oneof or wrapped fields
    problematic_data = {
        "string_list": {"values": []},  # Dict instead of list
        "number_list": {"items": []}    # Dict instead of list
    }
    
    # This will fail validation
    try:
        model3 = GenericListModel.model_validate(problematic_data)
        print(f"Problematic validation successful: {model3}")
    except ValidationError as e:
        print(f"Validation error (expected): {e}")
        print("\nDetailed errors:")
        for error in e.errors():
            print(f"  - Field: {error['loc']}")
            print(f"    Type: {error['type']}")
            print(f"    Message: {error['msg']}")
            print(f"    Input: {error['input']}")


def analyze_oneof_serialization_issue():
    """Analyzes why oneof fields cause roundtrip issues.
    
    The core issue is that when Pydantic serializes a model with oneof fields,
    it includes ALL fields (even those not set in the oneof), which breaks
    the oneof validation on deserialization.
    """
    print("\n=== Analyzing oneof serialization behavior ===")
    
    # Create protobuf with oneof
    proto = demo_pb2.OptionalMessage()
    proto.x = "test"  # Only x is set in the oneof
    
    # Convert to dict via protobuf's JSON
    proto_dict = json.loads(json_format.MessageToJson(proto, always_print_fields_with_no_presence=True))
    print(f"Protobuf dict (only set fields): {proto_dict}")
    print(f"  - Contains 'x': {proto_dict.get('x')}")
    print(f"  - Contains 'y': {'y' in proto_dict}")
    
    # Load into Pydantic
    pydantic_model = OptionalMessage.model_validate(proto_dict)
    
    # Dump from Pydantic
    pydantic_dict = pydantic_model.model_dump()
    print(f"\nPydantic dict (all fields): {pydantic_dict}")
    print(f"  - Contains 'x': {pydantic_dict.get('x')}")
    print(f"  - Contains 'y': {pydantic_dict.get('y')}")
    
    print(f"\nThe issue: Pydantic includes both 'x' and 'y' in the output,")
    print(f"but the oneof validator expects only one to be set!")


if __name__ == "__main__":
    print("=== Testing oneof roundtrip issue ===")
    test_oneof_roundtrip_issue()
    
    print("\n=== Testing array field issue ===")
    test_oneof_with_arrays_issue()
    
    print("\n=== Testing generic list validation error ===")
    test_generic_list_validation_error()
    
    print("\n")
    analyze_oneof_serialization_issue()