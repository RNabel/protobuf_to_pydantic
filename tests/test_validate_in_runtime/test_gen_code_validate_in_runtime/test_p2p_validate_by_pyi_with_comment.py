from example.proto_pydanticv2.example.example_proto.p2p_validate_by_comment import (
    demo_pb2_by_pyi,  # type: ignore
)

from .test_p2p_validate import BaseGenCodeP2pModelValidator


class TestP2pModelValidator(BaseGenCodeP2pModelValidator):
    core_module = demo_pb2_by_pyi
