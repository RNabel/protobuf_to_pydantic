# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: example/example_proto/demo/basic_types_roundtrip.proto
# Protobuf Python Version: 6.31.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    0,
    '',
    'example/example_proto/demo/basic_types_roundtrip.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n6example/example_proto/demo/basic_types_roundtrip.proto\x12\troundtrip\"\xe4\x06\n\x11\x42\x61sicTypesMessage\x12\x13\n\x0bint32_field\x18\x01 \x01(\x05\x12\x13\n\x0bint64_field\x18\x02 \x01(\x03\x12\x14\n\x0cuint32_field\x18\x03 \x01(\r\x12\x14\n\x0cuint64_field\x18\x04 \x01(\x04\x12\x14\n\x0csint32_field\x18\x05 \x01(\x11\x12\x14\n\x0csint64_field\x18\x06 \x01(\x12\x12\x15\n\rfixed32_field\x18\x07 \x01(\x07\x12\x15\n\rfixed64_field\x18\x08 \x01(\x06\x12\x16\n\x0esfixed32_field\x18\t \x01(\x0f\x12\x16\n\x0esfixed64_field\x18\n \x01(\x10\x12\x13\n\x0b\x66loat_field\x18\x0b \x01(\x02\x12\x14\n\x0c\x64ouble_field\x18\x0c \x01(\x01\x12\x12\n\nbool_field\x18\r \x01(\x08\x12\x14\n\x0cstring_field\x18\x0e \x01(\t\x12\x13\n\x0b\x62ytes_field\x18\x0f \x01(\x0c\x12\x16\n\x0erepeated_int32\x18\x10 \x03(\x05\x12\x16\n\x0erepeated_int64\x18\x11 \x03(\x03\x12\x17\n\x0frepeated_uint32\x18\x12 \x03(\r\x12\x17\n\x0frepeated_uint64\x18\x13 \x03(\x04\x12\x17\n\x0frepeated_sint32\x18\x14 \x03(\x11\x12\x17\n\x0frepeated_sint64\x18\x15 \x03(\x12\x12\x18\n\x10repeated_fixed32\x18\x16 \x03(\x07\x12\x18\n\x10repeated_fixed64\x18\x17 \x03(\x06\x12\x19\n\x11repeated_sfixed32\x18\x18 \x03(\x0f\x12\x19\n\x11repeated_sfixed64\x18\x19 \x03(\x10\x12\x16\n\x0erepeated_float\x18\x1a \x03(\x02\x12\x17\n\x0frepeated_double\x18\x1b \x03(\x01\x12\x15\n\rrepeated_bool\x18\x1c \x03(\x08\x12\x17\n\x0frepeated_string\x18\x1d \x03(\t\x12\x16\n\x0erepeated_bytes\x18\x1e \x03(\x0c\x12\x1b\n\x0eoptional_int32\x18\x1f \x01(\x05H\x00\x88\x01\x01\x12\x1c\n\x0foptional_string\x18  \x01(\tH\x01\x88\x01\x01\x12\x1a\n\roptional_bool\x18! \x01(\x08H\x02\x88\x01\x01\x42\x11\n\x0f_optional_int32B\x12\n\x10_optional_stringB\x10\n\x0e_optional_bool\"\x86\x04\n\x10\x45\x64geCasesMessage\x12\x11\n\tmin_int32\x18\x01 \x01(\x05\x12\x11\n\tmax_int32\x18\x02 \x01(\x05\x12\x11\n\tmin_int64\x18\x03 \x01(\x03\x12\x11\n\tmax_int64\x18\x04 \x01(\x03\x12\x12\n\nmin_uint32\x18\x05 \x01(\r\x12\x12\n\nmax_uint32\x18\x06 \x01(\r\x12\x12\n\nmin_uint64\x18\x07 \x01(\x04\x12\x12\n\nmax_uint64\x18\x08 \x01(\x04\x12\x12\n\nzero_float\x18\t \x01(\x02\x12\x1b\n\x13negative_zero_float\x18\n \x01(\x02\x12\x16\n\x0einfinity_float\x18\x0b \x01(\x02\x12\x1f\n\x17negative_infinity_float\x18\x0c \x01(\x02\x12\x11\n\tnan_float\x18\r \x01(\x02\x12\x13\n\x0bzero_double\x18\x0e \x01(\x01\x12\x1c\n\x14negative_zero_double\x18\x0f \x01(\x01\x12\x17\n\x0finfinity_double\x18\x10 \x01(\x01\x12 \n\x18negative_infinity_double\x18\x11 \x01(\x01\x12\x12\n\nnan_double\x18\x12 \x01(\x01\x12\x14\n\x0c\x65mpty_string\x18\x13 \x01(\t\x12\x13\n\x0b\x65mpty_bytes\x18\x14 \x01(\x0c\x12\x16\n\x0eunicode_string\x18\x15 \x01(\t\x12\x14\n\x0c\x65moji_string\x18\x16 \x01(\tb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'example.example_proto.demo.basic_types_roundtrip_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_BASICTYPESMESSAGE']._serialized_start=70
  _globals['_BASICTYPESMESSAGE']._serialized_end=938
  _globals['_EDGECASESMESSAGE']._serialized_start=941
  _globals['_EDGECASESMESSAGE']._serialized_end=1459
# @@protoc_insertion_point(module_scope)
