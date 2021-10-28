# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flyteidl/core/literals.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from flyteidl.core import types_pb2 as flyteidl_dot_core_dot_types__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='flyteidl/core/literals.proto',
  package='flyteidl.core',
  syntax='proto3',
  serialized_options=_b('Z4github.com/flyteorg/flyteidl/gen/pb-go/flyteidl/core'),
  serialized_pb=_b('\n\x1c\x66lyteidl/core/literals.proto\x12\rflyteidl.core\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x19\x66lyteidl/core/types.proto\"\xc8\x01\n\tPrimitive\x12\x11\n\x07integer\x18\x01 \x01(\x03H\x00\x12\x15\n\x0b\x66loat_value\x18\x02 \x01(\x01H\x00\x12\x16\n\x0cstring_value\x18\x03 \x01(\tH\x00\x12\x11\n\x07\x62oolean\x18\x04 \x01(\x08H\x00\x12.\n\x08\x64\x61tetime\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x12-\n\x08\x64uration\x18\x06 \x01(\x0b\x32\x19.google.protobuf.DurationH\x00\x42\x07\n\x05value\"\x06\n\x04Void\"B\n\x04\x42lob\x12-\n\x08metadata\x18\x01 \x01(\x0b\x32\x1b.flyteidl.core.BlobMetadata\x12\x0b\n\x03uri\x18\x03 \x01(\t\"5\n\x0c\x42lobMetadata\x12%\n\x04type\x18\x01 \x01(\x0b\x32\x17.flyteidl.core.BlobType\"$\n\x06\x42inary\x12\r\n\x05value\x18\x01 \x01(\x0c\x12\x0b\n\x03tag\x18\x02 \x01(\t\">\n\x06Schema\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\'\n\x04type\x18\x03 \x01(\x0b\x32\x19.flyteidl.core.SchemaType\"\xb4\x02\n\x06Scalar\x12-\n\tprimitive\x18\x01 \x01(\x0b\x32\x18.flyteidl.core.PrimitiveH\x00\x12#\n\x04\x62lob\x18\x02 \x01(\x0b\x32\x13.flyteidl.core.BlobH\x00\x12\'\n\x06\x62inary\x18\x03 \x01(\x0b\x32\x15.flyteidl.core.BinaryH\x00\x12\'\n\x06schema\x18\x04 \x01(\x0b\x32\x15.flyteidl.core.SchemaH\x00\x12(\n\tnone_type\x18\x05 \x01(\x0b\x32\x13.flyteidl.core.VoidH\x00\x12%\n\x05\x65rror\x18\x06 \x01(\x0b\x32\x14.flyteidl.core.ErrorH\x00\x12*\n\x07generic\x18\x07 \x01(\x0b\x32\x17.google.protobuf.StructH\x00\x42\x07\n\x05value\"\x9d\x01\n\x07Literal\x12\'\n\x06scalar\x18\x01 \x01(\x0b\x32\x15.flyteidl.core.ScalarH\x00\x12\x36\n\ncollection\x18\x02 \x01(\x0b\x32 .flyteidl.core.LiteralCollectionH\x00\x12(\n\x03map\x18\x03 \x01(\x0b\x32\x19.flyteidl.core.LiteralMapH\x00\x42\x07\n\x05value\"=\n\x11LiteralCollection\x12(\n\x08literals\x18\x01 \x03(\x0b\x32\x16.flyteidl.core.Literal\"\x90\x01\n\nLiteralMap\x12\x39\n\x08literals\x18\x01 \x03(\x0b\x32\'.flyteidl.core.LiteralMap.LiteralsEntry\x1aG\n\rLiteralsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.flyteidl.core.Literal:\x02\x38\x01\"E\n\x15\x42indingDataCollection\x12,\n\x08\x62indings\x18\x01 \x03(\x0b\x32\x1a.flyteidl.core.BindingData\"\x9c\x01\n\x0e\x42indingDataMap\x12=\n\x08\x62indings\x18\x01 \x03(\x0b\x32+.flyteidl.core.BindingDataMap.BindingsEntry\x1aK\n\rBindingsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12)\n\x05value\x18\x02 \x01(\x0b\x32\x1a.flyteidl.core.BindingData:\x02\x38\x01\"\xdc\x01\n\x0b\x42indingData\x12\'\n\x06scalar\x18\x01 \x01(\x0b\x32\x15.flyteidl.core.ScalarH\x00\x12:\n\ncollection\x18\x02 \x01(\x0b\x32$.flyteidl.core.BindingDataCollectionH\x00\x12\x31\n\x07promise\x18\x03 \x01(\x0b\x32\x1e.flyteidl.core.OutputReferenceH\x00\x12,\n\x03map\x18\x04 \x01(\x0b\x32\x1d.flyteidl.core.BindingDataMapH\x00\x42\x07\n\x05value\"C\n\x07\x42inding\x12\x0b\n\x03var\x18\x01 \x01(\t\x12+\n\x07\x62inding\x18\x02 \x01(\x0b\x32\x1a.flyteidl.core.BindingData\"*\n\x0cKeyValuePair\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\" \n\rRetryStrategy\x12\x0f\n\x07retries\x18\x05 \x01(\rB6Z4github.com/flyteorg/flyteidl/gen/pb-go/flyteidl/coreb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,google_dot_protobuf_dot_duration__pb2.DESCRIPTOR,google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,flyteidl_dot_core_dot_types__pb2.DESCRIPTOR,])




_PRIMITIVE = _descriptor.Descriptor(
  name='Primitive',
  full_name='flyteidl.core.Primitive',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='integer', full_name='flyteidl.core.Primitive.integer', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='float_value', full_name='flyteidl.core.Primitive.float_value', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='string_value', full_name='flyteidl.core.Primitive.string_value', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='boolean', full_name='flyteidl.core.Primitive.boolean', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='datetime', full_name='flyteidl.core.Primitive.datetime', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='duration', full_name='flyteidl.core.Primitive.duration', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='value', full_name='flyteidl.core.Primitive.value',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=170,
  serialized_end=370,
)


_VOID = _descriptor.Descriptor(
  name='Void',
  full_name='flyteidl.core.Void',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=372,
  serialized_end=378,
)


_BLOB = _descriptor.Descriptor(
  name='Blob',
  full_name='flyteidl.core.Blob',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='metadata', full_name='flyteidl.core.Blob.metadata', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='uri', full_name='flyteidl.core.Blob.uri', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=380,
  serialized_end=446,
)


_BLOBMETADATA = _descriptor.Descriptor(
  name='BlobMetadata',
  full_name='flyteidl.core.BlobMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='flyteidl.core.BlobMetadata.type', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=448,
  serialized_end=501,
)


_BINARY = _descriptor.Descriptor(
  name='Binary',
  full_name='flyteidl.core.Binary',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='flyteidl.core.Binary.value', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tag', full_name='flyteidl.core.Binary.tag', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=503,
  serialized_end=539,
)


_SCHEMA = _descriptor.Descriptor(
  name='Schema',
  full_name='flyteidl.core.Schema',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uri', full_name='flyteidl.core.Schema.uri', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='flyteidl.core.Schema.type', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=541,
  serialized_end=603,
)


_SCALAR = _descriptor.Descriptor(
  name='Scalar',
  full_name='flyteidl.core.Scalar',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='primitive', full_name='flyteidl.core.Scalar.primitive', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='blob', full_name='flyteidl.core.Scalar.blob', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='binary', full_name='flyteidl.core.Scalar.binary', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='schema', full_name='flyteidl.core.Scalar.schema', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='none_type', full_name='flyteidl.core.Scalar.none_type', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error', full_name='flyteidl.core.Scalar.error', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='generic', full_name='flyteidl.core.Scalar.generic', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='value', full_name='flyteidl.core.Scalar.value',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=606,
  serialized_end=914,
)


_LITERAL = _descriptor.Descriptor(
  name='Literal',
  full_name='flyteidl.core.Literal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='scalar', full_name='flyteidl.core.Literal.scalar', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='collection', full_name='flyteidl.core.Literal.collection', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='map', full_name='flyteidl.core.Literal.map', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='value', full_name='flyteidl.core.Literal.value',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=917,
  serialized_end=1074,
)


_LITERALCOLLECTION = _descriptor.Descriptor(
  name='LiteralCollection',
  full_name='flyteidl.core.LiteralCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='literals', full_name='flyteidl.core.LiteralCollection.literals', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1076,
  serialized_end=1137,
)


_LITERALMAP_LITERALSENTRY = _descriptor.Descriptor(
  name='LiteralsEntry',
  full_name='flyteidl.core.LiteralMap.LiteralsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='flyteidl.core.LiteralMap.LiteralsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='flyteidl.core.LiteralMap.LiteralsEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1213,
  serialized_end=1284,
)

_LITERALMAP = _descriptor.Descriptor(
  name='LiteralMap',
  full_name='flyteidl.core.LiteralMap',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='literals', full_name='flyteidl.core.LiteralMap.literals', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_LITERALMAP_LITERALSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1140,
  serialized_end=1284,
)


_BINDINGDATACOLLECTION = _descriptor.Descriptor(
  name='BindingDataCollection',
  full_name='flyteidl.core.BindingDataCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bindings', full_name='flyteidl.core.BindingDataCollection.bindings', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1286,
  serialized_end=1355,
)


_BINDINGDATAMAP_BINDINGSENTRY = _descriptor.Descriptor(
  name='BindingsEntry',
  full_name='flyteidl.core.BindingDataMap.BindingsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='flyteidl.core.BindingDataMap.BindingsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='flyteidl.core.BindingDataMap.BindingsEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1439,
  serialized_end=1514,
)

_BINDINGDATAMAP = _descriptor.Descriptor(
  name='BindingDataMap',
  full_name='flyteidl.core.BindingDataMap',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bindings', full_name='flyteidl.core.BindingDataMap.bindings', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_BINDINGDATAMAP_BINDINGSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1358,
  serialized_end=1514,
)


_BINDINGDATA = _descriptor.Descriptor(
  name='BindingData',
  full_name='flyteidl.core.BindingData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='scalar', full_name='flyteidl.core.BindingData.scalar', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='collection', full_name='flyteidl.core.BindingData.collection', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='promise', full_name='flyteidl.core.BindingData.promise', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='map', full_name='flyteidl.core.BindingData.map', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='value', full_name='flyteidl.core.BindingData.value',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=1517,
  serialized_end=1737,
)


_BINDING = _descriptor.Descriptor(
  name='Binding',
  full_name='flyteidl.core.Binding',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='var', full_name='flyteidl.core.Binding.var', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='binding', full_name='flyteidl.core.Binding.binding', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1739,
  serialized_end=1806,
)


_KEYVALUEPAIR = _descriptor.Descriptor(
  name='KeyValuePair',
  full_name='flyteidl.core.KeyValuePair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='flyteidl.core.KeyValuePair.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='flyteidl.core.KeyValuePair.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1808,
  serialized_end=1850,
)


_RETRYSTRATEGY = _descriptor.Descriptor(
  name='RetryStrategy',
  full_name='flyteidl.core.RetryStrategy',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='retries', full_name='flyteidl.core.RetryStrategy.retries', index=0,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1852,
  serialized_end=1884,
)

_PRIMITIVE.fields_by_name['datetime'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_PRIMITIVE.fields_by_name['duration'].message_type = google_dot_protobuf_dot_duration__pb2._DURATION
_PRIMITIVE.oneofs_by_name['value'].fields.append(
  _PRIMITIVE.fields_by_name['integer'])
_PRIMITIVE.fields_by_name['integer'].containing_oneof = _PRIMITIVE.oneofs_by_name['value']
_PRIMITIVE.oneofs_by_name['value'].fields.append(
  _PRIMITIVE.fields_by_name['float_value'])
_PRIMITIVE.fields_by_name['float_value'].containing_oneof = _PRIMITIVE.oneofs_by_name['value']
_PRIMITIVE.oneofs_by_name['value'].fields.append(
  _PRIMITIVE.fields_by_name['string_value'])
_PRIMITIVE.fields_by_name['string_value'].containing_oneof = _PRIMITIVE.oneofs_by_name['value']
_PRIMITIVE.oneofs_by_name['value'].fields.append(
  _PRIMITIVE.fields_by_name['boolean'])
_PRIMITIVE.fields_by_name['boolean'].containing_oneof = _PRIMITIVE.oneofs_by_name['value']
_PRIMITIVE.oneofs_by_name['value'].fields.append(
  _PRIMITIVE.fields_by_name['datetime'])
_PRIMITIVE.fields_by_name['datetime'].containing_oneof = _PRIMITIVE.oneofs_by_name['value']
_PRIMITIVE.oneofs_by_name['value'].fields.append(
  _PRIMITIVE.fields_by_name['duration'])
_PRIMITIVE.fields_by_name['duration'].containing_oneof = _PRIMITIVE.oneofs_by_name['value']
_BLOB.fields_by_name['metadata'].message_type = _BLOBMETADATA
_BLOBMETADATA.fields_by_name['type'].message_type = flyteidl_dot_core_dot_types__pb2._BLOBTYPE
_SCHEMA.fields_by_name['type'].message_type = flyteidl_dot_core_dot_types__pb2._SCHEMATYPE
_SCALAR.fields_by_name['primitive'].message_type = _PRIMITIVE
_SCALAR.fields_by_name['blob'].message_type = _BLOB
_SCALAR.fields_by_name['binary'].message_type = _BINARY
_SCALAR.fields_by_name['schema'].message_type = _SCHEMA
_SCALAR.fields_by_name['none_type'].message_type = _VOID
_SCALAR.fields_by_name['error'].message_type = flyteidl_dot_core_dot_types__pb2._ERROR
_SCALAR.fields_by_name['generic'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_SCALAR.oneofs_by_name['value'].fields.append(
  _SCALAR.fields_by_name['primitive'])
_SCALAR.fields_by_name['primitive'].containing_oneof = _SCALAR.oneofs_by_name['value']
_SCALAR.oneofs_by_name['value'].fields.append(
  _SCALAR.fields_by_name['blob'])
_SCALAR.fields_by_name['blob'].containing_oneof = _SCALAR.oneofs_by_name['value']
_SCALAR.oneofs_by_name['value'].fields.append(
  _SCALAR.fields_by_name['binary'])
_SCALAR.fields_by_name['binary'].containing_oneof = _SCALAR.oneofs_by_name['value']
_SCALAR.oneofs_by_name['value'].fields.append(
  _SCALAR.fields_by_name['schema'])
_SCALAR.fields_by_name['schema'].containing_oneof = _SCALAR.oneofs_by_name['value']
_SCALAR.oneofs_by_name['value'].fields.append(
  _SCALAR.fields_by_name['none_type'])
_SCALAR.fields_by_name['none_type'].containing_oneof = _SCALAR.oneofs_by_name['value']
_SCALAR.oneofs_by_name['value'].fields.append(
  _SCALAR.fields_by_name['error'])
_SCALAR.fields_by_name['error'].containing_oneof = _SCALAR.oneofs_by_name['value']
_SCALAR.oneofs_by_name['value'].fields.append(
  _SCALAR.fields_by_name['generic'])
_SCALAR.fields_by_name['generic'].containing_oneof = _SCALAR.oneofs_by_name['value']
_LITERAL.fields_by_name['scalar'].message_type = _SCALAR
_LITERAL.fields_by_name['collection'].message_type = _LITERALCOLLECTION
_LITERAL.fields_by_name['map'].message_type = _LITERALMAP
_LITERAL.oneofs_by_name['value'].fields.append(
  _LITERAL.fields_by_name['scalar'])
_LITERAL.fields_by_name['scalar'].containing_oneof = _LITERAL.oneofs_by_name['value']
_LITERAL.oneofs_by_name['value'].fields.append(
  _LITERAL.fields_by_name['collection'])
_LITERAL.fields_by_name['collection'].containing_oneof = _LITERAL.oneofs_by_name['value']
_LITERAL.oneofs_by_name['value'].fields.append(
  _LITERAL.fields_by_name['map'])
_LITERAL.fields_by_name['map'].containing_oneof = _LITERAL.oneofs_by_name['value']
_LITERALCOLLECTION.fields_by_name['literals'].message_type = _LITERAL
_LITERALMAP_LITERALSENTRY.fields_by_name['value'].message_type = _LITERAL
_LITERALMAP_LITERALSENTRY.containing_type = _LITERALMAP
_LITERALMAP.fields_by_name['literals'].message_type = _LITERALMAP_LITERALSENTRY
_BINDINGDATACOLLECTION.fields_by_name['bindings'].message_type = _BINDINGDATA
_BINDINGDATAMAP_BINDINGSENTRY.fields_by_name['value'].message_type = _BINDINGDATA
_BINDINGDATAMAP_BINDINGSENTRY.containing_type = _BINDINGDATAMAP
_BINDINGDATAMAP.fields_by_name['bindings'].message_type = _BINDINGDATAMAP_BINDINGSENTRY
_BINDINGDATA.fields_by_name['scalar'].message_type = _SCALAR
_BINDINGDATA.fields_by_name['collection'].message_type = _BINDINGDATACOLLECTION
_BINDINGDATA.fields_by_name['promise'].message_type = flyteidl_dot_core_dot_types__pb2._OUTPUTREFERENCE
_BINDINGDATA.fields_by_name['map'].message_type = _BINDINGDATAMAP
_BINDINGDATA.oneofs_by_name['value'].fields.append(
  _BINDINGDATA.fields_by_name['scalar'])
_BINDINGDATA.fields_by_name['scalar'].containing_oneof = _BINDINGDATA.oneofs_by_name['value']
_BINDINGDATA.oneofs_by_name['value'].fields.append(
  _BINDINGDATA.fields_by_name['collection'])
_BINDINGDATA.fields_by_name['collection'].containing_oneof = _BINDINGDATA.oneofs_by_name['value']
_BINDINGDATA.oneofs_by_name['value'].fields.append(
  _BINDINGDATA.fields_by_name['promise'])
_BINDINGDATA.fields_by_name['promise'].containing_oneof = _BINDINGDATA.oneofs_by_name['value']
_BINDINGDATA.oneofs_by_name['value'].fields.append(
  _BINDINGDATA.fields_by_name['map'])
_BINDINGDATA.fields_by_name['map'].containing_oneof = _BINDINGDATA.oneofs_by_name['value']
_BINDING.fields_by_name['binding'].message_type = _BINDINGDATA
DESCRIPTOR.message_types_by_name['Primitive'] = _PRIMITIVE
DESCRIPTOR.message_types_by_name['Void'] = _VOID
DESCRIPTOR.message_types_by_name['Blob'] = _BLOB
DESCRIPTOR.message_types_by_name['BlobMetadata'] = _BLOBMETADATA
DESCRIPTOR.message_types_by_name['Binary'] = _BINARY
DESCRIPTOR.message_types_by_name['Schema'] = _SCHEMA
DESCRIPTOR.message_types_by_name['Scalar'] = _SCALAR
DESCRIPTOR.message_types_by_name['Literal'] = _LITERAL
DESCRIPTOR.message_types_by_name['LiteralCollection'] = _LITERALCOLLECTION
DESCRIPTOR.message_types_by_name['LiteralMap'] = _LITERALMAP
DESCRIPTOR.message_types_by_name['BindingDataCollection'] = _BINDINGDATACOLLECTION
DESCRIPTOR.message_types_by_name['BindingDataMap'] = _BINDINGDATAMAP
DESCRIPTOR.message_types_by_name['BindingData'] = _BINDINGDATA
DESCRIPTOR.message_types_by_name['Binding'] = _BINDING
DESCRIPTOR.message_types_by_name['KeyValuePair'] = _KEYVALUEPAIR
DESCRIPTOR.message_types_by_name['RetryStrategy'] = _RETRYSTRATEGY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Primitive = _reflection.GeneratedProtocolMessageType('Primitive', (_message.Message,), dict(
  DESCRIPTOR = _PRIMITIVE,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.Primitive)
  ))
_sym_db.RegisterMessage(Primitive)

Void = _reflection.GeneratedProtocolMessageType('Void', (_message.Message,), dict(
  DESCRIPTOR = _VOID,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.Void)
  ))
_sym_db.RegisterMessage(Void)

Blob = _reflection.GeneratedProtocolMessageType('Blob', (_message.Message,), dict(
  DESCRIPTOR = _BLOB,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.Blob)
  ))
_sym_db.RegisterMessage(Blob)

BlobMetadata = _reflection.GeneratedProtocolMessageType('BlobMetadata', (_message.Message,), dict(
  DESCRIPTOR = _BLOBMETADATA,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.BlobMetadata)
  ))
_sym_db.RegisterMessage(BlobMetadata)

Binary = _reflection.GeneratedProtocolMessageType('Binary', (_message.Message,), dict(
  DESCRIPTOR = _BINARY,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.Binary)
  ))
_sym_db.RegisterMessage(Binary)

Schema = _reflection.GeneratedProtocolMessageType('Schema', (_message.Message,), dict(
  DESCRIPTOR = _SCHEMA,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.Schema)
  ))
_sym_db.RegisterMessage(Schema)

Scalar = _reflection.GeneratedProtocolMessageType('Scalar', (_message.Message,), dict(
  DESCRIPTOR = _SCALAR,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.Scalar)
  ))
_sym_db.RegisterMessage(Scalar)

Literal = _reflection.GeneratedProtocolMessageType('Literal', (_message.Message,), dict(
  DESCRIPTOR = _LITERAL,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.Literal)
  ))
_sym_db.RegisterMessage(Literal)

LiteralCollection = _reflection.GeneratedProtocolMessageType('LiteralCollection', (_message.Message,), dict(
  DESCRIPTOR = _LITERALCOLLECTION,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.LiteralCollection)
  ))
_sym_db.RegisterMessage(LiteralCollection)

LiteralMap = _reflection.GeneratedProtocolMessageType('LiteralMap', (_message.Message,), dict(

  LiteralsEntry = _reflection.GeneratedProtocolMessageType('LiteralsEntry', (_message.Message,), dict(
    DESCRIPTOR = _LITERALMAP_LITERALSENTRY,
    __module__ = 'flyteidl.core.literals_pb2'
    # @@protoc_insertion_point(class_scope:flyteidl.core.LiteralMap.LiteralsEntry)
    ))
  ,
  DESCRIPTOR = _LITERALMAP,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.LiteralMap)
  ))
_sym_db.RegisterMessage(LiteralMap)
_sym_db.RegisterMessage(LiteralMap.LiteralsEntry)

BindingDataCollection = _reflection.GeneratedProtocolMessageType('BindingDataCollection', (_message.Message,), dict(
  DESCRIPTOR = _BINDINGDATACOLLECTION,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.BindingDataCollection)
  ))
_sym_db.RegisterMessage(BindingDataCollection)

BindingDataMap = _reflection.GeneratedProtocolMessageType('BindingDataMap', (_message.Message,), dict(

  BindingsEntry = _reflection.GeneratedProtocolMessageType('BindingsEntry', (_message.Message,), dict(
    DESCRIPTOR = _BINDINGDATAMAP_BINDINGSENTRY,
    __module__ = 'flyteidl.core.literals_pb2'
    # @@protoc_insertion_point(class_scope:flyteidl.core.BindingDataMap.BindingsEntry)
    ))
  ,
  DESCRIPTOR = _BINDINGDATAMAP,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.BindingDataMap)
  ))
_sym_db.RegisterMessage(BindingDataMap)
_sym_db.RegisterMessage(BindingDataMap.BindingsEntry)

BindingData = _reflection.GeneratedProtocolMessageType('BindingData', (_message.Message,), dict(
  DESCRIPTOR = _BINDINGDATA,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.BindingData)
  ))
_sym_db.RegisterMessage(BindingData)

Binding = _reflection.GeneratedProtocolMessageType('Binding', (_message.Message,), dict(
  DESCRIPTOR = _BINDING,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.Binding)
  ))
_sym_db.RegisterMessage(Binding)

KeyValuePair = _reflection.GeneratedProtocolMessageType('KeyValuePair', (_message.Message,), dict(
  DESCRIPTOR = _KEYVALUEPAIR,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.KeyValuePair)
  ))
_sym_db.RegisterMessage(KeyValuePair)

RetryStrategy = _reflection.GeneratedProtocolMessageType('RetryStrategy', (_message.Message,), dict(
  DESCRIPTOR = _RETRYSTRATEGY,
  __module__ = 'flyteidl.core.literals_pb2'
  # @@protoc_insertion_point(class_scope:flyteidl.core.RetryStrategy)
  ))
_sym_db.RegisterMessage(RetryStrategy)


DESCRIPTOR._options = None
_LITERALMAP_LITERALSENTRY._options = None
_BINDINGDATAMAP_BINDINGSENTRY._options = None
# @@protoc_insertion_point(module_scope)
