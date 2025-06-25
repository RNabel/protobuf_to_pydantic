# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing
from typing import Annotated, Any, Literal, Union

from google.protobuf.message import Message  # type: ignore
from pydantic import Field, model_validator

from protobuf_to_pydantic.default_base_model import ProtobufCompatibleBaseModel


class ReportDataDataTime_Value(ProtobufCompatibleBaseModel):
    """Variant when 'time_value' is set in data oneof."""

    data_case: Literal["time_value"] = Field(default="time_value", exclude=True)
    time_value: Any


class ReportDataDataLocation_Value(ProtobufCompatibleBaseModel):
    """Variant when 'location_value' is set in data oneof."""

    data_case: Literal["location_value"] = Field(default="location_value", exclude=True)
    location_value: Any


ReportDataDataUnion = Annotated[
    Union[ReportDataDataTime_Value, ReportDataDataLocation_Value], Field(discriminator="data_case")
]


class ReportData(ProtobufCompatibleBaseModel):
    """
    Annotations are used in runtime mode
    """

    data: ReportDataDataUnion

    def model_dump(self, **kwargs):
        """Override to handle oneof fields specially."""
        data = super().model_dump(**kwargs)
        result = {}

        for field_name, field_value in data.items():
            if field_name in ["data"]:
                # This is a oneof field - flatten it
                if isinstance(field_value, dict):
                    for k, v in field_value.items():
                        if not (k.endswith("_case") or k.startswith("__")):
                            result[k] = v
            else:
                result[field_name] = field_value

        return result

    def model_dump_json(self, **kwargs):
        """Override to use custom model_dump."""
        from pydantic_core import to_json

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

        # Handle data oneof
        if "data" not in data:
            # Check if any oneof field is present in flat format
            present_fields = [f for f in ["location_value", "time_value"] if f in data]
            if len(present_fields) > 1:
                raise ValueError(
                    f"Multiple fields from oneof 'data' specified: {', '.join(present_fields)}. Only one field allowed."
                )
            if present_fields:
                field = present_fields[0]
                data["data"] = {field: data.pop(field), "data_case": field}

        return data


class GeoLocation(ProtobufCompatibleBaseModel):
    latitude: float = Field(default=0.0)
    longitude: float = Field(default=0.0)
    altitude_meters: typing.Optional[float] = Field(default=0.0)


class Report(ProtobufCompatibleBaseModel):
    source_id: typing.Optional[str] = Field(default="")
    data: ReportData = Field(default_factory=ReportData)
