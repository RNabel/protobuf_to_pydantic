# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing

from google.protobuf.message import Message  # type: ignore
from pydantic import Field

from protobuf_to_pydantic.default_base_model import ProtobufCompatibleBaseModel


class ValueTestMessage(ProtobufCompatibleBaseModel):
    """
    Test message with google.protobuf.Value field
    """

    id: str = Field(default="")
    dynamic_value: typing.Optional[typing.Any] = Field(default=None)
    value_list: typing.List[typing.Any] = Field(default_factory=list)
    value_map: "typing.Dict[str, typing.Any]" = Field(default_factory=dict)
