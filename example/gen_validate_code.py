import importlib
import inspect
import pathlib
import warnings

from google.protobuf import __version__
from google.protobuf.message import Message

from protobuf_to_pydantic import (
    msg_to_pydantic_model,
    pydantic_model_to_py_file,
)

# use pydantic v1 method, pydantic will print warning, ignore!~
warnings.filterwarnings("ignore")

target_p: str = "proto" if __version__ > "4.0.0" else "proto_3_20"
target_p += "_pydanticv2"

module = importlib.import_module(
    f"example.{target_p}.example.example_proto.validate.demo_pb2"
)
message_class_list = []
for module_name in dir(module):
    message_class = getattr(module, module_name)
    if not inspect.isclass(message_class):
        continue
    if not issubclass(message_class, Message):
        continue
    message_class_list.append(message_class)


now_path: pathlib.Path = pathlib.Path(__file__).absolute()


def gen_code() -> None:
    pydantic_model_to_py_file(
        str(now_path.parent.joinpath(target_p, "demo_gen_code_by_pgv.py")),
        *[
            msg_to_pydantic_model(model, parse_msg_desc_method="PGV")
            for model in message_class_list
        ],
        module_path=str(now_path.parent),
    )


if __name__ == "__main__":
    gen_code()
