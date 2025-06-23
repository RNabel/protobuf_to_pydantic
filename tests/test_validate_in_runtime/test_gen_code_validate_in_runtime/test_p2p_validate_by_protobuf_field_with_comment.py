#  type: ignore
from typing import Any, Callable, Type

from google.protobuf import __version__

if __version__ > "4.0.0":
    from example.proto_pydanticv2.example.example_proto.p2p_validate_by_comment import (
        demo_pb2_by_protobuf,  # type: ignore
    )
else:
    from example.proto_3_20_pydanticv2.example.example_proto.p2p_validate_by_comment import demo_pb2_by_protobuf # type: ignore

from .test_p2p_validate import BaseGenCodeP2pModelValidator


class TestP2pModelValidator(BaseGenCodeP2pModelValidator):
    core_module = demo_pb2_by_protobuf
