"""Default base model for protobuf_to_pydantic generated models."""

from typing import Any, TYPE_CHECKING

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


# Default base model to use if none is specified
default_base_model = ProtobufCompatibleBaseModel
