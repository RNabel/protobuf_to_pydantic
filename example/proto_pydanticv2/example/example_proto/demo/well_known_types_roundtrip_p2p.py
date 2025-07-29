# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing
from datetime import timedelta

from google.protobuf.message import Message  # type: ignore
from pydantic import Field

from protobuf_to_pydantic.default_base_model import ProtobufCompatibleBaseModel
from protobuf_to_pydantic.util import DurationType, TimestampType, datetime_utc_now


class WellKnownTypesMessage(ProtobufCompatibleBaseModel):
    """
    Message to test well-known protobuf types for round-trip conversion
    """

    # Timestamp fields
    created_at: TimestampType = Field(default_factory=datetime_utc_now)
    updated_at: TimestampType = Field(default_factory=datetime_utc_now)
    expires_at: TimestampType = Field(default_factory=datetime_utc_now)
    # Duration fields
    timeout: DurationType = Field(default_factory=timedelta)
    processing_time: DurationType = Field(default_factory=timedelta)
    ttl: DurationType = Field(default_factory=timedelta)
    # Optional well-known types
    optional_timestamp: typing.Optional[TimestampType] = Field(default=None)
    optional_duration: typing.Optional[DurationType] = Field(default=None)
    # Repeated well-known types
    event_timestamps: typing.List[TimestampType] = Field(default_factory=list)
    intervals: typing.List[DurationType] = Field(default_factory=list)
    # Map with well-known types as values
    timestamp_map: "typing.Dict[str, TimestampType]" = Field(default_factory=dict)
    duration_map: "typing.Dict[str, DurationType]" = Field(default_factory=dict)


class WellKnownEdgeCasesMessage(ProtobufCompatibleBaseModel):
    """
    Edge cases for well-known types
    """

    # Zero values
    zero_timestamp: TimestampType = Field(default_factory=datetime_utc_now)
    zero_duration: DurationType = Field(default_factory=timedelta)
    # Max values
    max_timestamp: TimestampType = Field(default_factory=datetime_utc_now)
    max_duration: DurationType = Field(default_factory=timedelta)
    # Negative duration (durations can be negative)
    negative_duration: DurationType = Field(default_factory=timedelta)
    # Timestamp with nanosecond precision
    precise_timestamp: TimestampType = Field(default_factory=datetime_utc_now)
    # Duration with nanosecond precision
    precise_duration: DurationType = Field(default_factory=timedelta)
