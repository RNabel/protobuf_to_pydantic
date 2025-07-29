import inspect
import json
import logging
import os
import re
import sys
from pydantic import AliasGenerator
from contextlib import contextmanager
from dataclasses import MISSING
from datetime import datetime, timedelta, timezone
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)

from pydantic import (
    BaseConfig,
    BaseModel,
    create_model,
    BeforeValidator,
    PlainSerializer,
)
from typing_extensions import Annotated


if TYPE_CHECKING:
    from pydantic.main import Model
    from pydantic.typing import AnyClassMethod

from google.protobuf import struct_pb2
from protobuf_to_pydantic.grpc_types import Duration, ProtobufRepeatedType, Timestamp


class Timedelta(timedelta):
    """Timedelta object supporting Protobuf.Duration of pydantic.field."""

    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Union[int, float, str, timedelta]) -> timedelta:
        if isinstance(v, timedelta):
            return v
        elif isinstance(v, str):
            # Handle protobuf duration format (e.g., "30s", "-30s", "1.123456s")
            if v.endswith("s"):
                try:
                    return timedelta(seconds=float(v[:-1]))
                except ValueError:
                    pass

            # Handle ISO 8601 duration format (e.g., "PT30S", "-PT30S", "PT1M30S")
            if v.startswith("PT") or v.startswith("-PT"):
                import re

                # Handle negative durations
                negative = v.startswith("-")
                if negative:
                    v = v[1:]  # Remove the leading "-"

                # Parse ISO 8601 duration
                match = re.match(
                    r"^PT(?:(\d+(?:\.\d+)?)H)?(?:(\d+(?:\.\d+)?)M)?(?:(\d+(?:\.\d+)?)S)?$",
                    v,
                )
                if match:
                    hours, minutes, seconds = match.groups()
                    total_seconds = 0
                    if hours:
                        total_seconds += float(hours) * 3600
                    if minutes:
                        total_seconds += float(minutes) * 60
                    if seconds:
                        total_seconds += float(seconds)

                    if negative:
                        total_seconds = -total_seconds

                    return timedelta(seconds=total_seconds)

            # Try to parse as a plain number (seconds)
            try:
                v = float(v)
            except ValueError:
                raise ValueError(f"Invalid duration format: {v}")

        return timedelta(seconds=v)


def duration_serializer(td: timedelta) -> str:
    """Serialize timedelta to protobuf duration format."""
    total_seconds = td.total_seconds()

    # Handle zero duration
    if total_seconds == 0:
        return "0s"

    # Format with up to 9 decimal places (nanosecond precision)
    # Remove trailing zeros and decimal point if not needed
    formatted = f"{total_seconds:.9f}".rstrip("0").rstrip(".")
    return f"{formatted}s"


DurationType = Annotated[
    timedelta,
    BeforeValidator(Timedelta.validate),
    PlainSerializer(duration_serializer, return_type=str, when_used="json"),
]


def datetime_utc_now() -> datetime:
    """Return current UTC time with timezone info."""
    return datetime.now(timezone.utc)


def timestamp_serializer(dt: datetime) -> str:
    """Serialize datetime to protobuf timestamp format (RFC3339)."""
    if dt.tzinfo is None:
        # If no timezone, assume UTC
        dt = dt.replace(tzinfo=timezone.utc)

    # Format as RFC3339 with timezone
    # Use isoformat() which handles the timezone correctly
    iso_str = dt.isoformat()

    # Replace +00:00 with Z for UTC (RFC3339 style)
    if iso_str.endswith("+00:00"):
        iso_str = iso_str[:-6] + "Z"

    return iso_str


TimestampType = Annotated[
    datetime, PlainSerializer(timestamp_serializer, return_type=str, when_used="json")
]


def value_validator(v: Any) -> Any:
    """Validate google.protobuf.Value field - accepts any JSON-serializable value."""
    # google.protobuf.Value supports: null, number, string, bool, struct (dict), list
    if v is None:
        return None
    elif isinstance(v, (bool, int, float, str)):
        return v
    elif isinstance(v, dict):
        # Recursively validate dict values
        return {key: value_validator(val) for key, val in v.items()}
    elif isinstance(v, (list, tuple)):
        # Recursively validate list items
        return [value_validator(item) for item in v]
    else:
        # For other types, try to convert to a JSON-serializable format
        try:
            import json

            # Test if it's JSON serializable
            json.dumps(v)
            return v
        except (TypeError, ValueError):
            # If not JSON serializable, convert to string representation
            return str(v)


ValueType = Annotated[
    Any,
    BeforeValidator(value_validator),
]


def camel_to_snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def create_pydantic_model(
    annotation_dict: Dict[str, Tuple[Type, Any]],
    class_name: str = "DynamicModel",
    pydantic_config: Optional[Type["BaseConfig"]] = None,
    pydantic_base: Union[None, Type["Model"], Tuple[Type["Model"], ...]] = None,
    pydantic_module: str = "pydantic.main",
    pydantic_validators: Optional[Dict[str, "AnyClassMethod"]] = None,
) -> Type["BaseModel"]:
    """pydantic self.pait_response_model helper
    if use create_model('DynamicModel', **annotation_dict), mypy will tip error
    """
    return create_model(  # type: ignore
        class_name,
        __config__=pydantic_config,
        __base__=pydantic_base,
        __module__=pydantic_module,
        __validators__=pydantic_validators,
        **annotation_dict,
    )


def replace_protobuf_type_to_python_type(value: Any) -> Any:
    """
    protobuf.Duration -> datetime.timedelta
    protobuf.Timestamp -> timestamp e.g 1600000000.000000
    like list type -> list
    other type -> raw...
    """
    if isinstance(value, Duration):
        return timedelta(microseconds=value.ToMicroseconds())
    elif isinstance(value, Timestamp):
        return value.ToMicroseconds() / 1000000
    elif isinstance(value, (list, *ProtobufRepeatedType)):
        return [replace_protobuf_type_to_python_type(i) for i in value]
    else:
        return value


def get_dict_from_comment(comment_prefix: str, comment: str) -> dict:
    _dict: dict = {}
    try:
        for line in comment.split("\n"):
            if line.startswith("#"):
                line = line[1:]
            line = line.strip()
            if not line.startswith(f"{comment_prefix}:"):
                continue
            line = line.replace(f"{comment_prefix}:", "")
            for key, value in json.loads(line.replace("\\\\", "\\")).items():
                if not _dict.get(key):
                    _dict[key] = value
                else:
                    if not isinstance(value, type(_dict[key])):
                        raise TypeError(
                            f"Two different types of values were detected for Key:{key}"
                        )
                    elif isinstance(value, list):
                        _dict[key].extend(value)
                    elif isinstance(value, dict):
                        _dict[key].update(value)
                    else:
                        raise TypeError(
                            f"A key:{key} that does not support merging has been detected"
                        )
    except Exception as e:
        logging.warning(f"Can not gen dict by desc:{comment}, error: {e}")
    return _dict  # type: ignore


def get_pyproject_content(pyproject_file_path: str) -> str:
    if not pyproject_file_path:
        for path in sys.path:
            pyproject_file_path = os.path.join(path, "pyproject.toml")
            if os.path.exists(pyproject_file_path):
                break
            pyproject_file_path = ""

    if pyproject_file_path:
        with open(pyproject_file_path, "r") as f:
            return "".join(f.readlines())
    return ""


# flake8: noqa: C901
def format_content(content_str: str, pyproject_file_path: str = "") -> str:
    pyproject_dict: dict = {}
    toml = None  # type: ignore

    try:
        import tomllib as toml  # type: ignore
    except ImportError:
        try:
            import toml  # type: ignore
        except ImportError:
            logging.warning(
                "The toml module is not installed and the configuration information cannot be obtained through"
                " pyproject.toml"
            )

    if toml:
        pyproject_content = get_pyproject_content(pyproject_file_path)
        if pyproject_content:
            pyproject_dict = toml.loads(pyproject_content)
    try:
        p2p_format_dict: dict = pyproject_dict["tool"]["protobuf-to-pydantic"]["format"]
    except KeyError:
        p2p_format_dict = {}

    try:
        import isort  # type: ignore
    except ImportError:
        pass
    else:
        if p2p_format_dict.get("isort", True):
            if pyproject_file_path:
                content_str = isort.code(
                    content_str, config=isort.Config(settings_file=pyproject_file_path)
                )
            else:
                content_str = isort.code(content_str)

    try:
        import autoflake  # type: ignore
    except ImportError:
        pass
    else:
        autoflake_dict: dict = {}
        try:
            for k, v in pyproject_dict["tool"]["autoflake"].items():
                k = k.replace("-", "_")
                if k not in inspect.signature(autoflake.fix_code).parameters.keys():
                    continue
                autoflake_dict[k] = v

        except KeyError:
            pass
        if p2p_format_dict.get("autoflake", True):
            if autoflake_dict:
                content_str = autoflake.fix_code(content_str, **autoflake_dict)
            else:
                content_str = autoflake.fix_code(content_str)

    try:
        import black  # type: ignore
    except ImportError:
        pass
    else:
        black_config_dict: dict = {}
        try:
            black_config_dict = {
                k.replace("-", "_"): v
                for k, v in pyproject_dict["tool"]["black"].items()
            }
            # target_version param replace
            target_versions = {
                getattr(black.TargetVersion, i.upper())
                for i in black_config_dict.pop("target_version", [])
            }
            if target_versions:
                black_config_dict["target_versions"] = target_versions

            black_config_dict = {
                k: v
                for k, v in black_config_dict.items()
                if k in black.Mode.__annotations__
            }
        except KeyError:
            pass
        if p2p_format_dict.get("black", True):
            if black_config_dict:
                content_str = black.format_str(
                    content_str, mode=black.Mode(**black_config_dict)
                )
            else:
                content_str = black.format_str(content_str, mode=black.Mode())
    return content_str


def check_dict_one_of(desc_dict: dict, key_list: List[str]) -> bool:
    """Check if the key also appears in the dict"""
    if (
        len(
            [
                desc_dict.get(key, None)
                for key in key_list
                if desc_dict.get(key, None)
                and desc_dict[key].__class__ != MISSING.__class__
            ]
        )
        > 1
    ):
        raise RuntimeError(f"Field:{key_list} cannot have both values: {desc_dict}")
    return True


@contextmanager
def use_worker_dir_in_ctx(worker_dir: Optional[str] = None) -> Generator:
    if worker_dir:
        parent_path_exist = worker_dir in sys.path
        if not parent_path_exist:
            sys.path.append(worker_dir)
            try:
                yield
            finally:
                sys.path.remove(worker_dir)
        else:
            yield
    else:
        yield


AliasGenType = Callable[[str], str] | AliasGenerator | None


def pydantic_allow_validation_field_handler(
    field_name: str,
    field_alias_name: Optional[str],
    allow_field_set: Set[str],
    model_config_dict: dict,
) -> None:
    """
    fix issue: #74 https://github.com/so1n/protobuf_to_pydantic/issues/74

    :param field_name: pydantic field name
    :param field_alias_name: pydantic field alias name
    :param allow_field_set: pydantic allow validation set
    :param model_config_dict: pydantic model config dict
    """
    if field_alias_name:
        allow_field_set.add(field_alias_name)
        if model_config_dict.get("populate_by_name") is not True:
            allow_field_set.remove(field_name)
        alias_generator: AliasGenType = model_config_dict.get("alias_generator")
        alias_generator_func: Optional[Callable] = None
        if isinstance(alias_generator, AliasGenerator):
            alias_generator_func = alias_generator.validation_alias
        elif callable(alias_generator):
            alias_generator_func = alias_generator
        else:
            alias_generator_func = None
        if alias_generator_func:
            allow_field_set.add(alias_generator_func(field_name))
    else:
        alias_generator_gte_26: Any = model_config_dict.get("alias_generator")
        if isinstance(alias_generator_gte_26, AliasGenerator):  # type: ignore
            alias_generator_func = alias_generator_gte_26.validation_alias
        else:
            alias_generator_func = alias_generator_gte_26
    if alias_generator_func:
        allow_field_set.add(alias_generator_func(field_name))
