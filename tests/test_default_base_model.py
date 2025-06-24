"""Test that the default ProtobufCompatibleBaseModel is used when no custom base is specified."""

import json
from typing import Any

from protobuf_to_pydantic import msg_to_pydantic_model
from protobuf_to_pydantic.default_base_model import ProtobufCompatibleBaseModel

# Create a simple test descriptor with float fields
def create_test_descriptor() -> Any:
    """Create a mock descriptor for testing."""
    from google.protobuf import descriptor_pb2
    from google.protobuf.message_factory import GetMessages
    
    # Create a simple proto definition
    proto = descriptor_pb2.FileDescriptorProto()
    proto.name = "test.proto"
    proto.package = "test"
    
    message = proto.message_type.add()
    message.name = "TestMessage"
    
    # Add float fields
    field = message.field.add()
    field.name = "float_value"
    field.number = 1
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_FLOAT
    
    field = message.field.add()
    field.name = "double_value"
    field.number = 2
    field.type = descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE
    
    # Get the message class
    messages = GetMessages([proto])
    return messages["test.TestMessage"]

def test_default_base_model_is_protobuf_compatible():
    """Test that models created without specifying a base use ProtobufCompatibleBaseModel."""
    TestMessage = create_test_descriptor()
    
    # Create a Pydantic model without specifying pydantic_base
    PydanticModel = msg_to_pydantic_model(
        TestMessage,
        parse_msg_desc_method="ignore"
    )
    
    # Check that it inherits from ProtobufCompatibleBaseModel
    assert issubclass(PydanticModel, ProtobufCompatibleBaseModel)
    
    # Verify the configuration is inherited
    assert PydanticModel.model_config.get("ser_json_inf_nan") == "strings"

def test_default_base_model_handles_special_floats():
    """Test that the default base model correctly handles special float values."""
    TestMessage = create_test_descriptor()
    
    # Create a Pydantic model
    PydanticModel = msg_to_pydantic_model(
        TestMessage,
        parse_msg_desc_method="ignore"
    )
    
    # Create instance with special float values
    instance = PydanticModel(
        float_value=float("inf"),
        double_value=float("-inf")
    )
    
    # Serialize to JSON
    json_str = instance.model_dump_json()
    json_data = json.loads(json_str)
    
    # Debug: print the actual keys
    print(f"JSON keys: {list(json_data.keys())}")
    print(f"JSON data: {json_data}")
    
    # The field names might be camelCase due to proto naming conventions
    float_key = "floatValue" if "floatValue" in json_data else "float_value"
    double_key = "doubleValue" if "doubleValue" in json_data else "double_value"
    
    # Verify special floats are serialized as strings
    assert json_data[float_key] == "Infinity"
    assert json_data[double_key] == "-Infinity"
    
    # Test NaN
    instance2 = PydanticModel(
        float_value=float("nan"),
        double_value=float("nan")
    )
    
    json_str2 = instance2.model_dump_json()
    json_data2 = json.loads(json_str2)
    
    assert json_data2[float_key] == "NaN"
    assert json_data2[double_key] == "NaN"

def test_plugin_config_uses_protobuf_compatible_base():
    """Test that the plugin config now defaults to ProtobufCompatibleBaseModel."""
    from protobuf_to_pydantic.plugin.config import ConfigModel
    
    config = ConfigModel()
    assert config.base_model_class == ProtobufCompatibleBaseModel

if __name__ == "__main__":
    test_default_base_model_is_protobuf_compatible()
    test_default_base_model_handles_special_floats()
    test_plugin_config_uses_protobuf_compatible_base()
    print("All tests passed!")