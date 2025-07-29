from functools import partial
from typing import Callable

from protobuf_to_pydantic import msg_to_pydantic_model
from tests.base.base_demo_validate import (
    BaseTestAliasDemoValidator,
    BaseTestSingleConfigValidator,
)
from tests.base.base_p2p_validate import local_dict

from example.proto_pydanticv2.example.example_proto.demo import (
    alias_demo_pb2,
    single_config_pb2,
)


class TestAliasDemoValidator(BaseTestAliasDemoValidator):
    replace_message_fn: Callable = staticmethod(  # type: ignore
        partial(
            msg_to_pydantic_model,
            local_dict=local_dict,
            parse_msg_desc_method=alias_demo_pb2,
        )
    )

    def test_alias_demo(self) -> None:
        super()._test_alias_demo(alias_demo_pb2.Report)


class TestSingleConfigValidator(BaseTestSingleConfigValidator):
    replace_message_fn: Callable = staticmethod(  # type: ignore
        partial(
            msg_to_pydantic_model,
            comment_prefix="aha",
            parse_msg_desc_method=single_config_pb2,
        )
    )

    def test_user_message(self) -> None:
        super()._test_user_message(single_config_pb2.UserMessage)
