from tests.base.base_demo_validate import (
    BaseTestAliasDemoValidator,
    BaseTestAllFieldSetOptionalDemoValidator,
    BaseTestCustomCommentHandler,
    BaseTestSingleConfigValidator,
)

from example.proto_pydanticv2.example.example_proto.demo import (  # type: ignore[no-redef]
    alias_demo_p2p,
    custom_comment_handler_p2p,
    single_config_p2p,
)


class TestAliasDemoValidator(BaseTestAliasDemoValidator):
    def test_alias_demo(self) -> None:
        super()._test_alias_demo(alias_demo_p2p.Report)


class TestSingleConfigValidator(BaseTestSingleConfigValidator):
    def test_user_message(self) -> None:
        super()._test_user_message(single_config_p2p.UserMessage)


class TestTestCustomCommentHandler(BaseTestCustomCommentHandler):
    def test_user_message(self) -> None:
        super()._test_user_message(custom_comment_handler_p2p.UserMessage)
