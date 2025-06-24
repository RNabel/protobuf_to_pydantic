# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing
from datetime import datetime, timedelta

from google.protobuf.message import Message  # type: ignore
from pydantic import BeforeValidator, Field
from typing_extensions import Annotated

from protobuf_to_pydantic.default_base_model import ProtobufCompatibleBaseModel
from protobuf_to_pydantic.util import Timedelta


class WellKnownTypesMessage(ProtobufCompatibleBaseModel):
    """
    Message to test well-known protobuf types for round-trip conversion
    """

    # Timestamp fields
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime = Field(default_factory=datetime.now)
    # Duration fields
    timeout: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(default_factory=timedelta)
    processing_time: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(default_factory=timedelta)
    ttl: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(default_factory=timedelta)
    # Optional well-known types
    optional_timestamp: typing.Optional[datetime] = Field(default_factory=datetime.now)
    optional_duration: typing.Optional[Annotated[timedelta, BeforeValidator(Timedelta.validate)]] = Field(
        default_factory=timedelta
    )
    # Repeated well-known types
    event_timestamps: typing.List[datetime] = Field(default_factory=list)
    intervals: typing.List[Annotated[timedelta, BeforeValidator(Timedelta.validate)]] = Field(default_factory=list)
    # Map with well-known types as values
    timestamp_map: "typing.Dict[str, datetime]" = Field(default_factory=dict)
    duration_map: "typing.Dict[str, Annotated[timedelta, BeforeValidator(Timedelta.validate)]]" = Field(
        default_factory=dict
    )


class WellKnownEdgeCasesMessage(ProtobufCompatibleBaseModel):
    """
    Edge cases for well-known types
    """

    # Zero values
    zero_timestamp: datetime = Field(default_factory=datetime.now)
    zero_duration: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(default_factory=timedelta)
    # Max values
    max_timestamp: datetime = Field(default_factory=datetime.now)
    max_duration: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(default_factory=timedelta)
    # Negative duration (durations can be negative)
    negative_duration: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(default_factory=timedelta)
    # Timestamp with nanosecond precision
    precise_timestamp: datetime = Field(default_factory=datetime.now)
    # Duration with nanosecond precision
    precise_duration: Annotated[timedelta, BeforeValidator(Timedelta.validate)] = Field(default_factory=timedelta)
