from typing import Any, Dict, Type

from google.protobuf.any_pb2 import Any as AnyMessage
from google.protobuf.descriptor import FieldDescriptor

from protobuf_to_pydantic.util import DurationType, Timedelta, TimestampType, ValueType, datetime_utc_now

message_name_default_factory_dict: Dict[str, Any] = {
    "Timestamp": datetime_utc_now,
    "Struct": dict,
    "Duration": Timedelta,
    "Any": AnyMessage,
}
pydantic_field_v1_migration_v2_dict = {
    "min_items": "min_length",
    "max_items": "max_length",
    "allow_mutation": "frozen",
    "regex": "pattern",
    "const": None,
    "unique_items": None,
}
message_name_type_dict: Dict[str, Any] = {
    "Timestamp": TimestampType,
    "Struct": Dict[str, Any],
    "Empty": Any,
    "Duration": DurationType,
    "Any": AnyMessage,
    "Value": ValueType,
}
python_type_default_value_dict: Dict[type, Any] = {
    float: 0.0,
    int: 0,
    bool: False,
    str: "",
    bytes: b"",
}
protobuf_desc_python_type_dict: Dict[int, Type] = {
    FieldDescriptor.TYPE_DOUBLE: float,
    FieldDescriptor.TYPE_FLOAT: float,
    FieldDescriptor.TYPE_INT64: int,
    FieldDescriptor.TYPE_UINT64: int,
    FieldDescriptor.TYPE_INT32: int,
    FieldDescriptor.TYPE_FIXED64: int,
    FieldDescriptor.TYPE_FIXED32: int,
    FieldDescriptor.TYPE_BOOL: bool,
    FieldDescriptor.TYPE_STRING: str,
    FieldDescriptor.TYPE_BYTES: bytes,
    FieldDescriptor.TYPE_UINT32: int,
    FieldDescriptor.TYPE_SFIXED32: int,
    FieldDescriptor.TYPE_SFIXED64: int,
    FieldDescriptor.TYPE_SINT32: int,
    FieldDescriptor.TYPE_SINT64: int,
}
protobuf_common_type_dict: Dict[Any, str] = {
    FieldDescriptor.TYPE_DOUBLE: "double",
    FieldDescriptor.TYPE_FLOAT: "float",
    FieldDescriptor.TYPE_INT64: "int64",
    FieldDescriptor.TYPE_UINT64: "uint64",
    FieldDescriptor.TYPE_INT32: "int32",
    FieldDescriptor.TYPE_FIXED64: "fixed64",
    FieldDescriptor.TYPE_FIXED32: "fixed32",
    FieldDescriptor.TYPE_BOOL: "bool",
    FieldDescriptor.TYPE_STRING: "string",
    FieldDescriptor.TYPE_BYTES: "bytes",
    FieldDescriptor.TYPE_UINT32: "uint32",
    FieldDescriptor.TYPE_ENUM: "enum",
    FieldDescriptor.TYPE_SFIXED32: "sfixed32",
    FieldDescriptor.TYPE_SFIXED64: "sfixed64",
    FieldDescriptor.TYPE_SINT32: "sint32",
    FieldDescriptor.TYPE_SINT64: "sint64",
}
