import importlib
import inspect
import pathlib
import time
import warnings
from uuid import uuid4

from google.protobuf.message import Message

from protobuf_to_pydantic import (
    msg_to_pydantic_model,
    pydantic_model_to_py_file,
)
from protobuf_to_pydantic.template import Template


class CustomCommentTemplate(Template):
    def template_timestamp(self, length_str: str) -> int:
        timestamp: float = 1600000000
        if length_str == "10":
            return int(timestamp)
        elif length_str == "13":
            return int(timestamp * 100)
        else:
            raise KeyError(f"timestamp template not support value:{length_str}")


# use pydantic v1 method, pydantic will print warning, ignore!~
warnings.filterwarnings("ignore")

target_p: str = "proto_pydanticv2"

module = importlib.import_module(
    f"example.{target_p}.example.example_proto.demo.demo_pb2"
)
message_class_list = []
for module_name in dir(module):
    message_class = getattr(module, module_name)
    if not inspect.isclass(message_class):
        continue
    if not issubclass(message_class, Message):
        continue
    message_class_list.append(message_class)


def exp_time() -> float:
    return time.time()


now_path: pathlib.Path = pathlib.Path(__file__).absolute()


def gen_code() -> None:
    local_dict = {"exp_time": exp_time, "uuid4": uuid4}
    pydantic_model_to_py_file(
        str(now_path.parent.joinpath(target_p, "demo_gen_code_by_text_comment_pyi.py")),
        *[
            msg_to_pydantic_model(
                model,
                parse_msg_desc_method=module,
                local_dict=local_dict,
                template=CustomCommentTemplate,
            )
            for model in message_class_list
        ],
        module_path=str(now_path.parent),
    )
    pydantic_model_to_py_file(
        str(
            now_path.parent.joinpath(
                target_p, "demo_gen_code_by_text_comment_protobuf_field.py"
            )
        ),
        *[
            msg_to_pydantic_model(
                model,
                parse_msg_desc_method=str(now_path.parent.parent),
                local_dict=local_dict,
                template=CustomCommentTemplate,
            )
            for model in message_class_list
        ],
        module_path=str(now_path.parent),
    )
    pydantic_model_to_py_file(
        str(now_path.parent.joinpath(target_p, "demo_gen_code_by_text_comment_pyi.py")),
        *[
            msg_to_pydantic_model(
                model,
                parse_msg_desc_method=module,
                local_dict=local_dict,
                template=CustomCommentTemplate,
            )
            for model in message_class_list
        ],
    )
    pydantic_model_to_py_file(
        str(
            now_path.parent.joinpath(
                target_p, "demo_gen_code_by_text_comment_protobuf_field.py"
            )
        ),
        *[
            msg_to_pydantic_model(
                model,
                parse_msg_desc_method=str(now_path.parent.parent),
                local_dict=local_dict,
                template=CustomCommentTemplate,
            )
            for model in message_class_list
        ],
    )


if __name__ == "__main__":
    gen_code()
