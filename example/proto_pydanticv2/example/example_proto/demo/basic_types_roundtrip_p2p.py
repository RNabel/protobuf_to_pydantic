# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 6.31.1
# Pydantic Version: 2.11.7
import typing

from google.protobuf.message import Message  # type: ignore
from pydantic import Field

from protobuf_to_pydantic.default_base_model import ProtobufCompatibleBaseModel


class BasicTypesMessage(ProtobufCompatibleBaseModel):
    """
    Message to test all basic protobuf types for round-trip conversion
    """

    # Numeric types
    int32_field: int = Field(default=0)
    int64_field: int = Field(default=0)
    uint32_field: int = Field(default=0)
    uint64_field: int = Field(default=0)
    sint32_field: int = Field(default=0)
    sint64_field: int = Field(default=0)
    fixed32_field: int = Field(default=0)
    fixed64_field: int = Field(default=0)
    sfixed32_field: int = Field(default=0)
    sfixed64_field: int = Field(default=0)
    # Floating point types
    float_field: float = Field(default=0.0)
    double_field: float = Field(default=0.0)
    # Boolean type
    bool_field: bool = Field(default=False)
    # String and bytes types
    string_field: str = Field(default="")
    bytes_field: bytes = Field(default=b"")
    # Repeated fields for each type
    repeated_int32: typing.List[int] = Field(default_factory=list)
    repeated_int64: typing.List[int] = Field(default_factory=list)
    repeated_uint32: typing.List[int] = Field(default_factory=list)
    repeated_uint64: typing.List[int] = Field(default_factory=list)
    repeated_sint32: typing.List[int] = Field(default_factory=list)
    repeated_sint64: typing.List[int] = Field(default_factory=list)
    repeated_fixed32: typing.List[int] = Field(default_factory=list)
    repeated_fixed64: typing.List[int] = Field(default_factory=list)
    repeated_sfixed32: typing.List[int] = Field(default_factory=list)
    repeated_sfixed64: typing.List[int] = Field(default_factory=list)
    repeated_float: typing.List[float] = Field(default_factory=list)
    repeated_double: typing.List[float] = Field(default_factory=list)
    repeated_bool: typing.List[bool] = Field(default_factory=list)
    repeated_string: typing.List[str] = Field(default_factory=list)
    repeated_bytes: typing.List[bytes] = Field(default_factory=list)
    # Optional fields for testing null handling
    optional_int32: typing.Optional[int] = Field(default=0)
    optional_string: typing.Optional[str] = Field(default="")
    optional_bool: typing.Optional[bool] = Field(default=False)


class EdgeCasesMessage(ProtobufCompatibleBaseModel):
    """
    Message for testing edge cases
    """

    # Min/max values for numeric types
    min_int32: int = Field(default=0)
    max_int32: int = Field(default=0)
    min_int64: int = Field(default=0)
    max_int64: int = Field(default=0)
    min_uint32: int = Field(default=0)
    max_uint32: int = Field(default=0)
    min_uint64: int = Field(default=0)
    max_uint64: int = Field(default=0)
    # Special float/double values
    zero_float: float = Field(default=0.0)
    negative_zero_float: float = Field(default=0.0)
    infinity_float: float = Field(default=0.0)
    negative_infinity_float: float = Field(default=0.0)
    nan_float: float = Field(default=0.0)
    zero_double: float = Field(default=0.0)
    negative_zero_double: float = Field(default=0.0)
    infinity_double: float = Field(default=0.0)
    negative_infinity_double: float = Field(default=0.0)
    nan_double: float = Field(default=0.0)
    # Empty string and bytes
    empty_string: str = Field(default="")
    empty_bytes: bytes = Field(default=b"")
    # Unicode strings
    unicode_string: str = Field(default="")
    emoji_string: str = Field(default="")
