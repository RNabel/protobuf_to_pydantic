"""Test showing how oneofs could be modeled as discriminated unions in Pydantic.

Based on research findings:
- Use WhichOneof() instead of HasField() for better performance
- Use base classes for common fields to avoid duplication
- Follow protobuf naming convention: <oneof_name>_case for discriminator
- Support Pydantic v2 Annotated syntax for discriminated unions
"""

import json
from typing import Literal, Union, Annotated
from google.protobuf import json_format
from pydantic import BaseModel, Field, ValidationError, ConfigDict

from example.proto_pydanticv2.example.example_proto.demo import demo_pb2


# Current implementation (problematic)
class OptionalMessageCurrent(BaseModel):
    """Current implementation - all fields exist simultaneously."""
    model_config = ConfigDict(populate_by_name=True)
    
    x: str = Field(default="")
    y: int = Field(default=0)
    name: str = Field(default="")
    age: int = Field(default=0)
    
    # The oneof validator would be applied here, but it causes issues


# Base class approach - avoids duplicating common fields
class _OptionalMessageBase(BaseModel):
    """Base class containing common fields outside the oneof."""
    name: str = Field(default="")
    age: int = Field(default=0)


# Discriminated union approach - Option 1: Using Literal discriminator
class OptionalMessageX(_OptionalMessageBase):
    """When 'x' is chosen in the oneof."""
    a_case: Literal["x"] = "x"  # Following protobuf convention: <oneof_name>_case
    x: str


class OptionalMessageY(_OptionalMessageBase):
    """When 'y' is chosen in the oneof."""
    a_case: Literal["y"] = "y"  # The oneof in demo.proto is named 'a'
    y: int


class OptionalMessageNone(_OptionalMessageBase):
    """When no oneof field is set."""
    a_case: Literal[None] = None  # None instead of "none" for clarity


# Pydantic v2 style discriminated union using Annotated
OptionalMessageUnion = Annotated[
    Union[OptionalMessageX, OptionalMessageY, OptionalMessageNone],
    Field(discriminator='a_case')
]

# For backward compatibility or when the message itself needs methods
class OptionalMessage(BaseModel):
    """Wrapper that contains the discriminated union."""
    root: OptionalMessageUnion


# Discriminated union approach - Option 2: Using field presence as discriminator
class OptionalMessageFieldX(BaseModel):
    """When 'x' field is present."""
    x: str
    y: None = None  # Explicitly None when not set
    name: str = Field(default="")
    age: int = Field(default=0)


class OptionalMessageFieldY(BaseModel):
    """When 'y' field is present."""
    x: None = None  # Explicitly None when not set
    y: int
    name: str = Field(default="")
    age: int = Field(default=0)


class OptionalMessageFieldNone(BaseModel):
    """When neither x nor y is set."""
    x: None = None
    y: None = None
    name: str = Field(default="")
    age: int = Field(default=0)


# Using Field discriminator (Pydantic v2 style)
OptionalMessageFieldBased = Union[
    OptionalMessageFieldX,
    OptionalMessageFieldY,
    OptionalMessageFieldNone
]


def test_current_approach_issues():
    """Demonstrate issues with the current approach."""
    print("=== Current Approach Issues ===")
    
    # Create protobuf with oneof
    proto = demo_pb2.OptionalMessage()
    proto.x = "test_value"
    
    # Convert to JSON
    proto_json = json_format.MessageToJson(proto, always_print_fields_with_no_presence=True)
    proto_dict = json.loads(proto_json)
    print(f"Protobuf JSON: {proto_dict}")
    
    # Create Pydantic model
    model = OptionalMessageCurrent(**proto_dict)
    print(f"Pydantic model: {model}")
    
    # The issue: both x and y are in the output
    output = model.model_dump()
    print(f"Model dump: {output}")
    print(f"Problem: Both 'x' and 'y' are present, violating oneof constraint!")


def test_discriminated_union_with_literal():
    """Test discriminated union approach with literal discriminator."""
    print("\n=== Discriminated Union with Literal ===")
    
    # Case 1: x is set
    proto = demo_pb2.OptionalMessage()
    proto.x = "test_value"
    proto_json = json_format.MessageToJson(proto, always_print_fields_with_no_presence=True)
    proto_dict = json.loads(proto_json)
    
    # Use WhichOneof for cleaner detection
    active_field = proto.WhichOneof("a")
    proto_dict["a_case"] = active_field
    
    if active_field == "x":
        model = OptionalMessageX(**proto_dict)
    elif active_field == "y":
        model = OptionalMessageY(**proto_dict)
    else:
        model = OptionalMessageNone(**proto_dict)
    
    print(f"Model type: {type(model).__name__}")
    print(f"Model: {model}")
    
    # Serialize and deserialize
    json_str = model.model_dump_json()
    print(f"JSON: {json_str}")
    
    # Deserialize back - need to parse as the union type
    # In real use, this would be handled by the union type
    parsed_dict = json.loads(json_str)
    if parsed_dict.get("a_case") == "x":
        parsed = OptionalMessageX.model_validate_json(json_str)
    elif parsed_dict.get("a_case") == "y":
        parsed = OptionalMessageY.model_validate_json(json_str)
    elif parsed_dict.get("a_case") is None:
        parsed = OptionalMessageNone.model_validate_json(json_str)
    else:
        print(f"Unknown a_case value: {parsed_dict.get('a_case')}")
        return
    print(f"Roundtrip successful! Parsed as: {type(parsed).__name__}")
    
    # Case 2: y is set
    print("\n--- Case 2: y is set ---")
    proto2 = demo_pb2.OptionalMessage()
    proto2.y = 42
    proto_json2 = json_format.MessageToJson(proto2, always_print_fields_with_no_presence=True)
    proto_dict2 = json.loads(proto_json2)
    
    active_field2 = proto2.WhichOneof("a")
    proto_dict2["a_case"] = active_field2
    if active_field2 == "y":
        model2 = OptionalMessageY(**proto_dict2)
    
    print(f"Model type: {type(model2).__name__}")
    print(f"Model: {model2}")
    print(f"Only 'y' is present, oneof constraint maintained!")


def test_field_based_discriminated_union():
    """Test discriminated union using field presence as discriminator."""
    print("\n=== Field-Based Discriminated Union ===")
    
    # Case 1: x is set
    data1 = {"x": "test_value", "name": "Alice"}
    
    # This will automatically match OptionalMessageFieldX because x is not None
    try:
        model1 = OptionalMessageFieldX(**data1)
        print(f"Model 1: {model1}")
        print(f"Serialized: {model1.model_dump_json()}")
        
        # Roundtrip
        roundtrip1 = OptionalMessageFieldX.model_validate_json(model1.model_dump_json())
        print(f"Roundtrip successful: {roundtrip1}")
    except ValidationError as e:
        print(f"Validation error: {e}")
    
    # Case 2: y is set
    print("\n--- Case 2: y is set ---")
    data2 = {"y": 42, "age": 25}
    
    model2 = OptionalMessageFieldY(**data2)
    print(f"Model 2: {model2}")
    print(f"Only y is set, x is None: {model2.x is None}")


def demonstrate_union_validation():
    """Show how Pydantic handles union validation."""
    print("\n=== Union Validation Demo ===")
    
    # Test data that should match different union members
    test_cases = [
        {"x": "hello", "name": "Test1"},  # Should match OptionalMessageFieldX
        {"y": 100, "age": 30},            # Should match OptionalMessageFieldY
        {"name": "Test3", "age": 20},    # Should match OptionalMessageFieldNone
    ]
    
    for i, data in enumerate(test_cases):
        print(f"\nTest case {i+1}: {data}")
        
        # Try each union member
        for model_class in [OptionalMessageFieldX, OptionalMessageFieldY, OptionalMessageFieldNone]:
            try:
                model = model_class(**data)
                print(f"  ✓ Matched {model_class.__name__}")
                break
            except ValidationError:
                print(f"  ✗ Did not match {model_class.__name__}")


def show_protobuf_to_discriminated_union_conversion():
    """Show how to convert from protobuf to discriminated union."""
    print("\n=== Protobuf to Discriminated Union Conversion ===")
    
    def protobuf_to_discriminated_model(proto_msg):
        """Convert a protobuf message to the appropriate discriminated union model.
        
        Uses WhichOneof() for better performance and cleaner code.
        """
        # Convert to JSON with default=False to avoid noise
        proto_json = json_format.MessageToJson(
            proto_msg, 
            always_print_fields_with_no_presence=False
        )
        proto_dict = json.loads(proto_json)
        
        # Use WhichOneof to determine active field (more efficient than HasField)
        active_field = proto_msg.WhichOneof("a")  # "a" is the oneof name
        
        # Add discriminator based on active field
        proto_dict["a_case"] = active_field
        
        # Create appropriate model variant
        if active_field == "x":
            return OptionalMessageX(**proto_dict)
        elif active_field == "y":
            return OptionalMessageY(**proto_dict)
        else:
            return OptionalMessageNone(**proto_dict)
    
    # Test with different protobuf configurations
    test_protos = [
        ("x is set", lambda p: setattr(p, "x", "hello")),
        ("y is set", lambda p: setattr(p, "y", 42)),
        ("nothing set", lambda p: None),
    ]
    
    for desc, setup in test_protos:
        proto = demo_pb2.OptionalMessage()
        setup(proto)
        
        model = protobuf_to_discriminated_model(proto)
        print(f"\n{desc}:")
        print(f"  Model type: {type(model).__name__}")
        print(f"  Model data: {model.model_dump()}")
        
        # Verify roundtrip works
        json_str = model.model_dump_json()
        # Verify serialization excludes None fields
        json_dict = json.loads(json_str)
        print(f"  JSON: {json_str}")
        print(f"  Fields in JSON: {list(json_dict.keys())}")


def test_pydantic_discriminated_union():
    """Test Pydantic's built-in discriminated union feature."""
    print("\n=== Pydantic Discriminated Union ===")
    
    # Test case 1: Create with x set
    data1 = {"a_case": "x", "x": "hello world", "name": "Alice"}
    model1 = OptionalMessage.model_validate({"root": data1})
    print(f"Model 1: {model1}")
    print(f"Root type: {type(model1.root).__name__}")
    print(f"Root data: {model1.root}")
    
    # Serialize with exclude_none for clean output
    json_str = model1.model_dump_json(exclude_none=True)
    print(f"JSON: {json_str}")
    
    # Pydantic automatically handles the discrimination
    parsed = OptionalMessage.model_validate_json(json_str)
    print(f"Parsed type: {type(parsed.root).__name__}")
    print(f"Roundtrip successful!")
    
    # Test case 2: Create with y set
    print("\n--- Test case 2: y set ---")
    data2 = {"a_case": "y", "y": 42, "age": 25}
    model2 = OptionalMessage.model_validate({"root": data2})
    print(f"Model 2 root type: {type(model2.root).__name__}")
    print(f"Model 2 data: {model2.root}")
    
    # Test case 3: Invalid discriminator
    print("\n--- Test case 3: Invalid data ---")
    try:
        invalid_data = {"a_case": "x", "y": 42}  # Mismatch!
        invalid_model = OptionalMessage.model_validate({"root": invalid_data})
    except ValidationError as e:
        print(f"Validation error (expected): {e}")
        

def compare_approaches():
    """Compare the current approach vs discriminated union approach."""
    print("\n=== Comparison: Current vs Discriminated Union ===")
    
    # Create a protobuf message
    proto = demo_pb2.OptionalMessage()
    proto.x = "test"
    proto.name = "Bob"
    
    proto_json = json_format.MessageToJson(proto, always_print_fields_with_no_presence=True)
    proto_dict = json.loads(proto_json)
    
    print("Original protobuf data:")
    print(f"  Fields: {proto_dict}")
    print(f"  Has x: {proto.HasField('x')}")
    print(f"  Has y: {proto.HasField('y')}")
    
    # Current approach
    print("\n1. Current approach (problematic):")
    current_model = OptionalMessageCurrent(**proto_dict)
    current_output = current_model.model_dump()
    print(f"  Output: {current_output}")
    print(f"  Problem: Both x={current_output['x']} and y={current_output['y']} in output")
    
    # Discriminated union approach
    print("\n2. Discriminated union approach (solution):")
    # Use WhichOneof for cleaner code
    active_field = proto.WhichOneof("a")
    proto_dict["a_case"] = active_field
    
    # Create the discriminated union variant
    if active_field == "x":
        variant = OptionalMessageX(**proto_dict)
    elif active_field == "y":
        variant = OptionalMessageY(**proto_dict)
    else:
        variant = OptionalMessageNone(**proto_dict)
    
    union_model = OptionalMessage(root=variant)
    union_output = union_model.model_dump(exclude_none=True)
    print(f"  Output: {union_output}")
    print(f"  Success: Only the active oneof field is included!")
    
    # Show that roundtrip works
    print("\n3. Roundtrip test:")
    roundtrip_json = union_model.model_dump_json(exclude_none=True)
    roundtrip_model = OptionalMessage.model_validate_json(roundtrip_json)
    print(f"  Roundtrip successful!")
    print(f"  Type preserved: {type(roundtrip_model.root).__name__}")


def test_discriminated_union_serialization_modes():
    """Test different JSON serialization modes for discriminated unions."""
    print("\n=== Serialization Modes ===")
    
    # Create a model with some fields set
    model = OptionalMessageX(x="test", name="Alice", age=30)
    
    # Default serialization
    print("Default serialization:")
    default_json = model.model_dump_json()
    print(f"  JSON: {default_json}")
    
    # With exclude_none=True (recommended)
    print("\nWith exclude_none=True:")
    clean_json = model.model_dump_json(exclude_none=True)
    print(f"  JSON: {clean_json}")
    
    # With exclude_defaults=True
    print("\nWith exclude_defaults=True:")
    minimal_json = model.model_dump_json(exclude_defaults=True)
    print(f"  JSON: {minimal_json}")
    
    # Verify all can roundtrip
    for desc, json_str in [("default", default_json), 
                           ("exclude_none", clean_json),
                           ("exclude_defaults", minimal_json)]:
        try:
            parsed = OptionalMessageX.model_validate_json(json_str)
            print(f"  {desc} roundtrip: ✓")
        except Exception as e:
            print(f"  {desc} roundtrip: ✗ - {e}")


def test_whichoneof_efficiency():
    """Demonstrate WhichOneof vs HasField efficiency."""
    print("\n=== WhichOneof vs HasField ===")
    
    # Create messages with different oneofs set
    messages = [
        (demo_pb2.OptionalMessage(), "empty"),
    ]
    
    msg_x = demo_pb2.OptionalMessage()
    msg_x.x = "test"
    messages.append((msg_x, "x set"))
    
    msg_y = demo_pb2.OptionalMessage()
    msg_y.y = 42
    messages.append((msg_y, "y set"))
    
    for msg, desc in messages:
        print(f"\n{desc}:")
        
        # Using WhichOneof (efficient)
        active = msg.WhichOneof("a")
        print(f"  WhichOneof('a'): {repr(active)}")
        
        # Using HasField (less efficient for multiple checks)
        has_x = msg.HasField("x")
        has_y = msg.HasField("y")
        print(f"  HasField('x'): {has_x}, HasField('y'): {has_y}")
        
        # They should match
        if active == "x":
            assert has_x and not has_y
        elif active == "y":
            assert has_y and not has_x
        elif active is None:
            assert not has_x and not has_y


def test_config_dict_usage():
    """Test ConfigDict settings for forward compatibility."""
    print("\n=== ConfigDict for Forward Compatibility ===")
    
    # Model with extra="ignore" for forward compatibility
    class FutureProofModel(_OptionalMessageBase):
        model_config = ConfigDict(extra="ignore")
        a_case: Literal["x"] = "x"
        x: str
    
    # Test with extra fields (simulating future proto additions)
    data_with_extras = {
        "a_case": "x",
        "x": "test",
        "name": "Bob",
        "age": 25,
        "future_field": "ignored",  # This would be a new field
        "another_new_field": 123
    }
    
    try:
        model = FutureProofModel(**data_with_extras)
        print(f"  Model created successfully with extra fields ignored")
        print(f"  Model data: {model.model_dump()}")
        print(f"  Extra fields were ignored: ✓")
    except ValidationError as e:
        print(f"  Failed with extra fields: {e}")


if __name__ == "__main__":
    test_current_approach_issues()
    test_discriminated_union_with_literal()
    test_field_based_discriminated_union()
    demonstrate_union_validation()
    show_protobuf_to_discriminated_union_conversion()
    test_pydantic_discriminated_union()
    compare_approaches()
    
    # New tests based on research
    test_discriminated_union_serialization_modes()
    test_whichoneof_efficiency()
    test_config_dict_usage()