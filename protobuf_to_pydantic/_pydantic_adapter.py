from typing import Any, Callable, Dict, Optional, Type

from pydantic import BaseModel
from pydantic import field_validator as _field_validator
from pydantic import model_validator as _model_validator
from pydantic.fields import FieldInfo, PydanticUndefined  # type: ignore
from pydantic.functional_validators import FieldValidatorModes  # type: ignore
from typing_extensions import Literal


NoArgAnyCallable = Callable[[], Any]
PydanticUndefinedType = type(PydanticUndefined)


def get_model_config_value(model: Type[BaseModel], key: str) -> Any:
    return model.model_config.get(key)


def model_fields(model: Type[FieldInfo]) -> Dict[str, FieldInfo]:
    return model.model_fields  # type: ignore


def field_validator(
    field_name: str,
    *fields: str,
    mode: FieldValidatorModes = "after",
    check_fields: Optional[bool] = None,
    **kwargs: Any,  # ignore v1 param
) -> Callable:
    return _field_validator(field_name, *fields, mode=mode, check_fields=check_fields)


def model_validator(
    *,
    mode: Literal["wrap", "before", "after"],
    **kwargs: Any,  # ignore v1 param
) -> Callable:
    return _model_validator(mode=mode)
