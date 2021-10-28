# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grid/v1/metadata.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='grid/v1/metadata.proto',
  package='grid.v1',
  syntax='proto3',
  serialized_options=b'Z0github.com/gridai/grid/grid-backend/apis/grid/v1',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16grid/v1/metadata.proto\x12\x07grid.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"\x87\x04\n\x08Metadata\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12I\n\x12\x63reation_timestamp\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x11\x63reationTimestamp\x12I\n\x12\x64\x65letion_timestamp\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x11\x64\x65letionTimestamp\x12)\n\x10resource_version\x18\x05 \x01(\tR\x0fresourceVersion\x12\x35\n\x06labels\x18\x06 \x03(\x0b\x32\x1d.grid.v1.Metadata.LabelsEntryR\x06labels\x12\x44\n\x0b\x61nnotations\x18\x07 \x03(\x0b\x32\".grid.v1.Metadata.AnnotationsEntryR\x0b\x61nnotations\x12\x1e\n\nfinalizers\x18\x08 \x03(\tR\nfinalizers\x1a\x39\n\x0bLabelsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1a>\n\x10\x41nnotationsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x42\x32Z0github.com/gridai/grid/grid-backend/apis/grid/v1b\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_METADATA_LABELSENTRY = _descriptor.Descriptor(
  name='LabelsEntry',
  full_name='grid.v1.Metadata.LabelsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='grid.v1.Metadata.LabelsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='key', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='grid.v1.Metadata.LabelsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='value', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=467,
  serialized_end=524,
)

_METADATA_ANNOTATIONSENTRY = _descriptor.Descriptor(
  name='AnnotationsEntry',
  full_name='grid.v1.Metadata.AnnotationsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='grid.v1.Metadata.AnnotationsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='key', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='grid.v1.Metadata.AnnotationsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='value', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=526,
  serialized_end=588,
)

_METADATA = _descriptor.Descriptor(
  name='Metadata',
  full_name='grid.v1.Metadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='grid.v1.Metadata.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='id', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='grid.v1.Metadata.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='name', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='creation_timestamp', full_name='grid.v1.Metadata.creation_timestamp', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='creationTimestamp', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deletion_timestamp', full_name='grid.v1.Metadata.deletion_timestamp', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='deletionTimestamp', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='resource_version', full_name='grid.v1.Metadata.resource_version', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='resourceVersion', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='labels', full_name='grid.v1.Metadata.labels', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='labels', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='annotations', full_name='grid.v1.Metadata.annotations', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='annotations', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='finalizers', full_name='grid.v1.Metadata.finalizers', index=7,
      number=8, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='finalizers', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_METADATA_LABELSENTRY, _METADATA_ANNOTATIONSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=69,
  serialized_end=588,
)

_METADATA_LABELSENTRY.containing_type = _METADATA
_METADATA_ANNOTATIONSENTRY.containing_type = _METADATA
_METADATA.fields_by_name['creation_timestamp'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_METADATA.fields_by_name['deletion_timestamp'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_METADATA.fields_by_name['labels'].message_type = _METADATA_LABELSENTRY
_METADATA.fields_by_name['annotations'].message_type = _METADATA_ANNOTATIONSENTRY
DESCRIPTOR.message_types_by_name['Metadata'] = _METADATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Metadata = _reflection.GeneratedProtocolMessageType('Metadata', (_message.Message,), {

  'LabelsEntry' : _reflection.GeneratedProtocolMessageType('LabelsEntry', (_message.Message,), {
    'DESCRIPTOR' : _METADATA_LABELSENTRY,
    '__module__' : 'grid.v1.metadata_pb2'
    # @@protoc_insertion_point(class_scope:grid.v1.Metadata.LabelsEntry)
    })
  ,

  'AnnotationsEntry' : _reflection.GeneratedProtocolMessageType('AnnotationsEntry', (_message.Message,), {
    'DESCRIPTOR' : _METADATA_ANNOTATIONSENTRY,
    '__module__' : 'grid.v1.metadata_pb2'
    # @@protoc_insertion_point(class_scope:grid.v1.Metadata.AnnotationsEntry)
    })
  ,
  'DESCRIPTOR' : _METADATA,
  '__module__' : 'grid.v1.metadata_pb2'
  # @@protoc_insertion_point(class_scope:grid.v1.Metadata)
  })
_sym_db.RegisterMessage(Metadata)
_sym_db.RegisterMessage(Metadata.LabelsEntry)
_sym_db.RegisterMessage(Metadata.AnnotationsEntry)


DESCRIPTOR._options = None
_METADATA_LABELSENTRY._options = None
_METADATA_ANNOTATIONSENTRY._options = None
# @@protoc_insertion_point(module_scope)
