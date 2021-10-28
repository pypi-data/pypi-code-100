# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: language.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import plugin_pb2 as plugin__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='language.proto',
  package='pulumirpc',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x0elanguage.proto\x12\tpulumirpc\x1a\x0cplugin.proto\x1a\x1bgoogle/protobuf/empty.proto\"J\n\x19GetRequiredPluginsRequest\x12\x0f\n\x07project\x18\x01 \x01(\t\x12\x0b\n\x03pwd\x18\x02 \x01(\t\x12\x0f\n\x07program\x18\x03 \x01(\t\"J\n\x1aGetRequiredPluginsResponse\x12,\n\x07plugins\x18\x01 \x03(\x0b\x32\x1b.pulumirpc.PluginDependency\"\xa2\x02\n\nRunRequest\x12\x0f\n\x07project\x18\x01 \x01(\t\x12\r\n\x05stack\x18\x02 \x01(\t\x12\x0b\n\x03pwd\x18\x03 \x01(\t\x12\x0f\n\x07program\x18\x04 \x01(\t\x12\x0c\n\x04\x61rgs\x18\x05 \x03(\t\x12\x31\n\x06\x63onfig\x18\x06 \x03(\x0b\x32!.pulumirpc.RunRequest.ConfigEntry\x12\x0e\n\x06\x64ryRun\x18\x07 \x01(\x08\x12\x10\n\x08parallel\x18\x08 \x01(\x05\x12\x17\n\x0fmonitor_address\x18\t \x01(\t\x12\x11\n\tqueryMode\x18\n \x01(\x08\x12\x18\n\x10\x63onfigSecretKeys\x18\x0b \x03(\t\x1a-\n\x0b\x43onfigEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"*\n\x0bRunResponse\x12\r\n\x05\x65rror\x18\x01 \x01(\t\x12\x0c\n\x04\x62\x61il\x18\x02 \x01(\x08\x32\xf0\x01\n\x0fLanguageRuntime\x12\x63\n\x12GetRequiredPlugins\x12$.pulumirpc.GetRequiredPluginsRequest\x1a%.pulumirpc.GetRequiredPluginsResponse\"\x00\x12\x36\n\x03Run\x12\x15.pulumirpc.RunRequest\x1a\x16.pulumirpc.RunResponse\"\x00\x12@\n\rGetPluginInfo\x12\x16.google.protobuf.Empty\x1a\x15.pulumirpc.PluginInfo\"\x00\x62\x06proto3'
  ,
  dependencies=[plugin__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_GETREQUIREDPLUGINSREQUEST = _descriptor.Descriptor(
  name='GetRequiredPluginsRequest',
  full_name='pulumirpc.GetRequiredPluginsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='project', full_name='pulumirpc.GetRequiredPluginsRequest.project', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pwd', full_name='pulumirpc.GetRequiredPluginsRequest.pwd', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='program', full_name='pulumirpc.GetRequiredPluginsRequest.program', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=72,
  serialized_end=146,
)


_GETREQUIREDPLUGINSRESPONSE = _descriptor.Descriptor(
  name='GetRequiredPluginsResponse',
  full_name='pulumirpc.GetRequiredPluginsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='plugins', full_name='pulumirpc.GetRequiredPluginsResponse.plugins', index=0,
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
  serialized_start=148,
  serialized_end=222,
)


_RUNREQUEST_CONFIGENTRY = _descriptor.Descriptor(
  name='ConfigEntry',
  full_name='pulumirpc.RunRequest.ConfigEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='pulumirpc.RunRequest.ConfigEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='pulumirpc.RunRequest.ConfigEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=470,
  serialized_end=515,
)

_RUNREQUEST = _descriptor.Descriptor(
  name='RunRequest',
  full_name='pulumirpc.RunRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='project', full_name='pulumirpc.RunRequest.project', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stack', full_name='pulumirpc.RunRequest.stack', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pwd', full_name='pulumirpc.RunRequest.pwd', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='program', full_name='pulumirpc.RunRequest.program', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='args', full_name='pulumirpc.RunRequest.args', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='config', full_name='pulumirpc.RunRequest.config', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dryRun', full_name='pulumirpc.RunRequest.dryRun', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parallel', full_name='pulumirpc.RunRequest.parallel', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='monitor_address', full_name='pulumirpc.RunRequest.monitor_address', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='queryMode', full_name='pulumirpc.RunRequest.queryMode', index=9,
      number=10, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='configSecretKeys', full_name='pulumirpc.RunRequest.configSecretKeys', index=10,
      number=11, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_RUNREQUEST_CONFIGENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=225,
  serialized_end=515,
)


_RUNRESPONSE = _descriptor.Descriptor(
  name='RunResponse',
  full_name='pulumirpc.RunResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='pulumirpc.RunResponse.error', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bail', full_name='pulumirpc.RunResponse.bail', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=517,
  serialized_end=559,
)

_GETREQUIREDPLUGINSRESPONSE.fields_by_name['plugins'].message_type = plugin__pb2._PLUGINDEPENDENCY
_RUNREQUEST_CONFIGENTRY.containing_type = _RUNREQUEST
_RUNREQUEST.fields_by_name['config'].message_type = _RUNREQUEST_CONFIGENTRY
DESCRIPTOR.message_types_by_name['GetRequiredPluginsRequest'] = _GETREQUIREDPLUGINSREQUEST
DESCRIPTOR.message_types_by_name['GetRequiredPluginsResponse'] = _GETREQUIREDPLUGINSRESPONSE
DESCRIPTOR.message_types_by_name['RunRequest'] = _RUNREQUEST
DESCRIPTOR.message_types_by_name['RunResponse'] = _RUNRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetRequiredPluginsRequest = _reflection.GeneratedProtocolMessageType('GetRequiredPluginsRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETREQUIREDPLUGINSREQUEST,
  '__module__' : 'language_pb2'
  # @@protoc_insertion_point(class_scope:pulumirpc.GetRequiredPluginsRequest)
  })
_sym_db.RegisterMessage(GetRequiredPluginsRequest)

GetRequiredPluginsResponse = _reflection.GeneratedProtocolMessageType('GetRequiredPluginsResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETREQUIREDPLUGINSRESPONSE,
  '__module__' : 'language_pb2'
  # @@protoc_insertion_point(class_scope:pulumirpc.GetRequiredPluginsResponse)
  })
_sym_db.RegisterMessage(GetRequiredPluginsResponse)

RunRequest = _reflection.GeneratedProtocolMessageType('RunRequest', (_message.Message,), {

  'ConfigEntry' : _reflection.GeneratedProtocolMessageType('ConfigEntry', (_message.Message,), {
    'DESCRIPTOR' : _RUNREQUEST_CONFIGENTRY,
    '__module__' : 'language_pb2'
    # @@protoc_insertion_point(class_scope:pulumirpc.RunRequest.ConfigEntry)
    })
  ,
  'DESCRIPTOR' : _RUNREQUEST,
  '__module__' : 'language_pb2'
  # @@protoc_insertion_point(class_scope:pulumirpc.RunRequest)
  })
_sym_db.RegisterMessage(RunRequest)
_sym_db.RegisterMessage(RunRequest.ConfigEntry)

RunResponse = _reflection.GeneratedProtocolMessageType('RunResponse', (_message.Message,), {
  'DESCRIPTOR' : _RUNRESPONSE,
  '__module__' : 'language_pb2'
  # @@protoc_insertion_point(class_scope:pulumirpc.RunResponse)
  })
_sym_db.RegisterMessage(RunResponse)


_RUNREQUEST_CONFIGENTRY._options = None

_LANGUAGERUNTIME = _descriptor.ServiceDescriptor(
  name='LanguageRuntime',
  full_name='pulumirpc.LanguageRuntime',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=562,
  serialized_end=802,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetRequiredPlugins',
    full_name='pulumirpc.LanguageRuntime.GetRequiredPlugins',
    index=0,
    containing_service=None,
    input_type=_GETREQUIREDPLUGINSREQUEST,
    output_type=_GETREQUIREDPLUGINSRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Run',
    full_name='pulumirpc.LanguageRuntime.Run',
    index=1,
    containing_service=None,
    input_type=_RUNREQUEST,
    output_type=_RUNRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetPluginInfo',
    full_name='pulumirpc.LanguageRuntime.GetPluginInfo',
    index=2,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=plugin__pb2._PLUGININFO,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_LANGUAGERUNTIME)

DESCRIPTOR.services_by_name['LanguageRuntime'] = _LANGUAGERUNTIME

# @@protoc_insertion_point(module_scope)
