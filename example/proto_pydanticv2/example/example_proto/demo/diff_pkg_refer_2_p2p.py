# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing

from google.protobuf.message import Message  # type: ignore
from pydantic import Field

from protobuf_to_pydantic.default_base_model import ProtobufCompatibleBaseModel

from .diff_pkg_refer_1_p2p import Demo1


class Demo2(ProtobufCompatibleBaseModel):
    myField: "typing.Dict[str, Demo1]" = Field(default_factory=dict)
