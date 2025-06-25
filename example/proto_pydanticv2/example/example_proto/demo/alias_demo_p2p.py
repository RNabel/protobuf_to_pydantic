# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing
from typing import Annotated, Any, Literal, Union

from google.protobuf.message import Message  # type: ignore
from pydantic import Field

from protobuf_to_pydantic.default_base_model import ProtobufCompatibleBaseModel


class _ReportDataDataBase(ProtobufCompatibleBaseModel):
    """Base class for data oneof variants."""


class ReportDataDataLocation_Value(_ReportDataDataBase):
    """Variant when 'location_value' is set in data oneof."""

    data_case: Literal["location_value"] = "location_value"
    location_value: Any


class ReportDataDataTime_Value(_ReportDataDataBase):
    """Variant when 'time_value' is set in data oneof."""

    data_case: Literal["time_value"] = "time_value"
    time_value: Any


ReportDataDataUnion = Annotated[
    Union[ReportDataDataLocation_Value, ReportDataDataTime_Value], Field(discriminator="data_case")
]


class ReportData(ProtobufCompatibleBaseModel):
    """
    Annotations are used in runtime mode
    """

    data: ReportDataDataUnion


class GeoLocation(ProtobufCompatibleBaseModel):
    latitude: float = Field(default=0.0)
    longitude: float = Field(default=0.0)
    altitude_meters: typing.Optional[float] = Field(default=0.0)


class Report(ProtobufCompatibleBaseModel):
    source_id: typing.Optional[str] = Field(default="")
    data: ReportData = Field(default_factory=ReportData)
