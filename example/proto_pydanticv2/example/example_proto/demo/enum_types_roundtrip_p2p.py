# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing
from enum import IntEnum

from google.protobuf.message import Message  # type: ignore
from pydantic import ConfigDict, Field

from protobuf_to_pydantic.default_base_model import ProtobufCompatibleBaseModel
from protobuf_to_pydantic.flexible_enum_mixin import FlexibleEnumMixin


class Status(IntEnum, FlexibleEnumMixin):
    """
    Test enum types for roundtrip conversion
    """

    UNKNOWN = 0
    ACTIVE = 1
    INACTIVE = 2
    PENDING = 3
    COMPLETED = 4


class Priority(IntEnum, FlexibleEnumMixin):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    URGENT = 3


class ErrorCode(IntEnum, FlexibleEnumMixin):
    """
    Enum with non-consecutive values
    """

    ERROR_NONE = 0
    ERROR_INVALID_INPUT = 100
    ERROR_TIMEOUT = 200
    ERROR_INTERNAL = 500
    ERROR_UNKNOWN = 999


class EnumMessage(ProtobufCompatibleBaseModel):
    """
    Message with enum fields
    """

    model_config = ConfigDict(validate_default=True)
    status: Status = Field(default=0)
    priority: Priority = Field(default=0)
    error_code: ErrorCode = Field(default=0)
    # Optional enum field
    optional_status: typing.Optional[Status] = Field(default=0)
    # Repeated enum field
    priority_list: typing.List[Priority] = Field(default_factory=list)
    # Map with enum values
    status_map: "typing.Dict[str, Status]" = Field(default_factory=dict)


class ComplexEnumMessage(ProtobufCompatibleBaseModel):
    """
    Message with multiple enum references
    """

    class NestedEnum(ProtobufCompatibleBaseModel):
        """
        Nested message with enums
        """

        model_config = ConfigDict(validate_default=True)
        nested_status: Status = Field(default=0)
        nested_priority: Priority = Field(default=0)

    model_config = ConfigDict(validate_default=True)
    primary_status: Status = Field(default=0)
    status_history: typing.List[Status] = Field(default_factory=list)
    task_priorities: "typing.Dict[str, Priority]" = Field(default_factory=dict)
    last_error: typing.Optional[ErrorCode] = Field(default=0)
    nested: "ComplexEnumMessage.NestedEnum" = Field(default_factory=lambda: ComplexEnumMessage.NestedEnum())
    nested_list: typing.List["ComplexEnumMessage.NestedEnum"] = Field(default_factory=list)
