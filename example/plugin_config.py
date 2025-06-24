import logging
import time
from typing import Dict, List, Type
from uuid import uuid4

from google.protobuf.any_pb2 import Any  # type: ignore
from pydantic import confloat, conint
from pydantic.fields import FieldInfo

from protobuf_to_pydantic.plugin.config import SubConfigModel
from protobuf_to_pydantic.template import Template

from . import (
    all_field_set_option_config,
    custom_comment_handler_pkg_plugin_config,
    populate_by_name_plugin_config,
    single_config_pkg_plugin_config,
)

logging.basicConfig(
    format="[%(asctime)s %(levelname)s] %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


class CustomerField(FieldInfo):
    pass


def customer_any() -> Any:
    return Any  # type: ignore


class CustomCommentTemplate(Template):
    def template_timestamp(self, length_str: str) -> int:
        timestamp: float = 1600000000
        if length_str == "10":
            return int(timestamp)
        elif length_str == "13":
            return int(timestamp * 100)
        else:
            raise KeyError(f"timestamp template not support value:{length_str}")


def exp_time() -> float:
    return time.time()


local_dict = {
    "CustomerField": CustomerField,
    "confloat": confloat,
    "conint": conint,
    "customer_any": customer_any,
    "exp_time": exp_time,
    "uuid4": uuid4,
}
comment_prefix = "p2p"
template: Type[Template] = CustomCommentTemplate
ignore_pkg_list: List[str] = ["validate", "p2p_validate"]
pkg_config: Dict[str, SubConfigModel] = {
    "all_field_set_optional": SubConfigModel(
        module=all_field_set_option_config, use_root_config=True
    ),
    "alias_demo": SubConfigModel(module=populate_by_name_plugin_config),
    "single_config": SubConfigModel(module=single_config_pkg_plugin_config),
    "custom_comment_handler": SubConfigModel(
        module=custom_comment_handler_pkg_plugin_config, use_root_config=True
    ),
}
