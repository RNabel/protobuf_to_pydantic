"""Default base model for protobuf_to_pydantic generated models."""

from typing import Any, Dict, TYPE_CHECKING

from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

if TYPE_CHECKING:
    from google.protobuf import struct_pb2


class ProtobufCompatibleBaseModel(BaseModel):
    """Base model for protobuf-generated Pydantic models with protobuf-compatible settings"""

    model_config = ConfigDict(
        # Serialize inf/-inf/nan as "Infinity"/"-Infinity"/"NaN" strings
        # to match protobuf's JSON serialization format
        ser_json_inf_nan="strings",
        # Add alias generation settings
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_camel,
        ),
        populate_by_name=True,
    )
    
    @staticmethod
    def python_to_protobuf_value(python_value: Any, proto_value: "struct_pb2.Value") -> None:
        """Convert Python value to protobuf Value.
        
        This is a convenience method that delegates to the util function.
        
        Args:
            python_value: The Python value to convert
            proto_value: The protobuf Value message to populate
        """
        from protobuf_to_pydantic.util import python_value_to_protobuf_value
        python_value_to_protobuf_value(python_value, proto_value)
    
    @staticmethod
    def protobuf_value_to_python(proto_value: "struct_pb2.Value") -> Any:
        """Convert protobuf Value to Python value.
        
        This is a convenience method that delegates to the util function.
        
        Args:
            proto_value: The protobuf Value message to convert
            
        Returns:
            The corresponding Python value
        """
        from protobuf_to_pydantic.util import protobuf_value_to_python_value
        return protobuf_value_to_python_value(proto_value)


# Default base model to use if none is specified
default_base_model = ProtobufCompatibleBaseModel
