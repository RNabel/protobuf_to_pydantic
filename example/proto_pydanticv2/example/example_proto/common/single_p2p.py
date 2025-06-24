# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
from enum import IntEnum

from google.protobuf.message import Message  # type: ignore
from pydantic import Field

from protobuf_to_pydantic.default_base_model import ProtobufCompatibleBaseModel
from protobuf_to_pydantic.flexible_enum_mixin import FlexibleEnumMixin


class DemoEnum(IntEnum, FlexibleEnumMixin):
    zero = 0
    one = 1
    two = 3


class DemoMessage(ProtobufCompatibleBaseModel):
    earth: str = Field(default="")
    mercury: str = Field(default="")
    mars: str = Field(default="")
