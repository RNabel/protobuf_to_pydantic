# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic

from enum import Enum
from typing import Any

from pydantic_core import core_schema as cs


class FlexibleEnumMixin(Enum):
    """Accept enum member, name or int when used in Pydantic models.

    This mixin allows enum fields to accept:
    - Enum members (Status.ACTIVE)
    - String names ("ACTIVE")
    - Integer values (1)

    Works automatically with all Pydantic field types including:
    - Single enum fields
    - Optional enum fields
    - List[Enum] fields
    - Dict[str, Enum] fields
    - Nested model fields containing enums
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Any, handler: Any) -> Any:
        """Pydantic V2 core schema for flexible enum validation."""
        # Get the default Enum schema first
        enum_schema = handler(cls)

        # Convert before default validation
        def before(v: Any, info: Any = None) -> Any:
            if isinstance(v, cls):
                return v
            if isinstance(v, str):
                try:
                    return cls[v]  # Get enum by name
                except KeyError as exc:
                    raise ValueError(
                        f"{v!r} is not a valid name for {cls.__name__}"
                    ) from exc
            return cls(v)  # Let Enum raise ValueError if invalid int

        # Use chain validator to run our validator first, then the enum validator
        return cs.chain_schema(
            [cs.with_info_plain_validator_function(before), enum_schema]
        )
