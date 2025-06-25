# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing
from typing import Annotated, Any, Literal, Union

from google.protobuf.message import Message  # type: ignore
from pydantic import Field

from protobuf_to_pydantic.default_base_model import ProtobufCompatibleBaseModel
from protobuf_to_pydantic.tagged_union_mixin import TaggedUnionMixin


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


class ReportData(TaggedUnionMixin, ProtobufCompatibleBaseModel):
    """
    Annotations are used in runtime mode
    """

    data: ReportDataDataUnion

    _oneof_fields = {
        "data": {
            "aliases": {
                "locationValue": "location_value",
                "location_value": "location_value",
                "timeValue": "time_value",
                "time_value": "time_value",
            },
            "fields": ["location_value", "time_value"],
        }
    }


class GeoLocation(ProtobufCompatibleBaseModel):
    latitude: float = Field(default=0.0)
    longitude: float = Field(default=0.0)
    altitude_meters: typing.Optional[float] = Field(default=0.0)


class Report(ProtobufCompatibleBaseModel):
    source_id: typing.Optional[str] = Field(default="")
    data: ReportData = Field(default_factory=ReportData)
