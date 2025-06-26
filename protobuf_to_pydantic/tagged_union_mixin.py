"""Mixin for handling discriminated union (oneof) fields in protobuf-generated models."""

from typing import Any
from pydantic import model_validator
from pydantic_core import to_json


class TaggedUnionMixin:
    """Mixin that provides centralized handling for protobuf oneof fields as tagged unions."""

    def model_dump(self, **kwargs) -> dict[str, Any]:
        """Override to handle oneof fields specially for protobuf compatibility."""
        # Call parent's model_dump
        data = super().model_dump(**kwargs)  # type: ignore

        if not hasattr(self.__class__, "_oneof_fields"):
            return data

        # Get the actual value from ModelPrivateAttr if needed
        union_fields = self.__class__._oneof_fields  # type: ignore
        if hasattr(union_fields, "default"):
            union_fields = union_fields.default

        result = {}

        for field_name, field_value in data.items():
            if field_name in union_fields:
                # This is a oneof field - flatten it
                if isinstance(field_value, dict):
                    for k, v in field_value.items():
                        if not (k.endswith("_case") or k.startswith("__")):
                            result[k] = v
            else:
                result[field_name] = field_value

        return result

    def model_dump_json(self, **kwargs) -> str:
        """Override to use custom model_dump for JSON serialization."""
        # Extract indent before passing to model_dump
        indent = kwargs.pop("indent", None)
        data = self.model_dump(**kwargs)
        return to_json(data, indent=indent).decode()

    @model_validator(mode="before")
    @classmethod
    def _deserialize_oneofs(cls, data):
        """Handle oneof field deserialization from flat JSON."""
        if not isinstance(data, dict):
            return data

        if not hasattr(cls, "_oneof_fields"):
            return data

        # Get the actual value from ModelPrivateAttr if needed
        union_fields = cls._oneof_fields  # type: ignore
        if hasattr(union_fields, "default"):
            union_fields = union_fields.default

        # Process each discriminated union field
        for field_name, field_info in union_fields.items():
            if field_name not in data:
                field_aliases = field_info.get("aliases", {})

                # Check if any oneof field is present in flat format
                present_fields = []
                field_mapping = {}
                for key in data:
                    if data[key] is None:
                        continue
                    if key in field_aliases:
                        actual_field = field_aliases[key]
                        if actual_field in field_mapping:
                            # Same field specified via different alias
                            raise ValueError(
                                f"Field '{actual_field}' specified multiple times in oneof '{field_name}' "
                                f"using different aliases: '{field_mapping[actual_field]}' and '{key}'. "
                                f"Only one field allowed."
                            )

                        present_fields.append(actual_field)
                        field_mapping[actual_field] = key

                if len(present_fields) > 1:
                    raise ValueError(
                        f"Multiple fields from oneof '{field_name}' specified: {', '.join(present_fields)}. "
                        f"Only one field allowed."
                    )
                if present_fields:
                    actual_field = present_fields[0]
                    data_key = field_mapping[actual_field]
                    data[field_name] = {
                        actual_field: data.pop(data_key),
                        f"{field_name}_case": actual_field,
                    }

        return data
