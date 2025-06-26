"""Default base model for protobuf_to_pydantic generated models."""

from typing import Any, Dict, Optional

from pydantic import AliasGenerator, BaseModel, ConfigDict, model_serializer
from pydantic.alias_generators import to_camel


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

    @model_serializer(mode="wrap")
    def serialize_model(self, nxt):
        output = nxt(self)
        if not hasattr(self, "_oneof_fields"):
            return output
        union_fields: dict[str, dict[str, dict[str, str]]] = self._oneof_fields  # type: ignore
        for field_name in union_fields.keys():
            if field_name not in output:
                continue
            field_value = output[field_name]
            output.pop(field_name)
            output.update(field_value)
        return output

    def model_dump(
        self,
        *,
        mode: str = "python",
        include: Optional[Any] = None,
        exclude: Optional[Any] = None,
        context: Optional[Dict[str, Any]] = None,
        by_alias: bool = False,
        exclude_unset: bool = True,  # Changed default to True
        exclude_defaults: bool = True,  # Changed default to True
        exclude_none: bool = True,  # Changed default to True
        round_trip: bool = False,
        warnings: bool = True,
        serialize_as_any: bool = False,
    ) -> Dict[str, Any]:
        """Override model_dump to exclude defaults and unset fields by default."""
        return super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )

    def model_dump_json(
        self,
        *,
        indent: Optional[int] = None,
        include: Optional[Any] = None,
        exclude: Optional[Any] = None,
        context: Optional[Dict[str, Any]] = None,
        by_alias: bool = False,
        exclude_unset: bool = True,  # Changed default to True
        exclude_defaults: bool = True,  # Changed default to True
        exclude_none: bool = True,  # Changed default to True
        round_trip: bool = False,
        warnings: bool = True,
        serialize_as_any: bool = False,
    ) -> str:
        """Override model_dump_json to exclude defaults and unset fields by default."""
        return super().model_dump_json(
            indent=indent,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )


# Default base model to use if none is specified
default_base_model = ProtobufCompatibleBaseModel
