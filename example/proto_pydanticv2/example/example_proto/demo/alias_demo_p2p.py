# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing

from google.protobuf.message import Message  # type: ignore
from pydantic import Field, model_validator

from protobuf_to_pydantic.customer_validator.v2 import check_one_of
from protobuf_to_pydantic.default_base_model import ProtobufCompatibleBaseModel
from protobuf_to_pydantic.util import TimestampType, datetime_utc_now


class GeoLocation(ProtobufCompatibleBaseModel):
    latitude: float = Field(default=0.0)
    longitude: float = Field(default=0.0)
    altitude_meters: typing.Optional[float] = Field(default=0.0)


class ReportData(ProtobufCompatibleBaseModel):
    """
    Annotations are used in runtime mode
    """

    _one_of_dict = {
        "ReportData.data": {"fields": {"locationValue", "location_value", "timeValue", "time_value"}, "required": True}
    }
    one_of_validator = model_validator(mode="before")(check_one_of)
    location_value: typing.Optional[GeoLocation] = Field(default_factory=GeoLocation)
    time_value: TimestampType = Field(default_factory=datetime_utc_now)


class Report(ProtobufCompatibleBaseModel):
    source_id: typing.Optional[str] = Field(default="")
    data: ReportData = Field(default_factory=ReportData)
