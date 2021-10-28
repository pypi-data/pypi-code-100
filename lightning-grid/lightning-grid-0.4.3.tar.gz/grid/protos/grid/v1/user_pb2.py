# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grid/v1/user.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from grid.protos.grid.v1 import metadata_pb2 as grid_dot_v1_dot_metadata__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='grid/v1/user.proto',
  package='grid.v1',
  syntax='proto3',
  serialized_options=b'Z0github.com/gridai/grid/grid-backend/apis/grid/v1',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x12grid/v1/user.proto\x12\x07grid.v1\x1a\x16grid/v1/metadata.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x92\x01\n\x04User\x12-\n\x08metadata\x18\x01 \x01(\x0b\x32\x11.grid.v1.MetadataR\x08metadata\x12.\n\x07\x64\x65tails\x18\x02 \x01(\x0b\x32\x14.grid.v1.UserDetailsR\x07\x64\x65tails\x12+\n\x06status\x18\x03 \x01(\x0b\x32\x13.grid.v1.UserStatusR\x06status\"\x9b\x03\n\x0bUserDetails\x12#\n\rauth_provider\x18\x01 \x01(\tR\x0c\x61uthProvider\x12\x1a\n\x08username\x18\x02 \x01(\tR\x08username\x12\x1d\n\nfirst_name\x18\x03 \x01(\tR\tfirstName\x12\x1b\n\tlast_name\x18\x04 \x01(\tR\x08lastName\x12\x14\n\x05\x65mail\x18\x05 \x01(\tR\x05\x65mail\x12*\n\x08\x61pi_keys\x18\x06 \x03(\x0b\x32\x0f.grid.v1.ApiKeyR\x07\x61piKeys\x12\x1f\n\x0bpicture_url\x18\x07 \x01(\tR\npictureUrl\x12\x1a\n\x08internal\x18\x0b \x01(\x08R\x08internal\x12!\n\x0cphone_number\x18\x0c \x01(\tR\x0bphoneNumber\x12\x31\n\x08\x66\x65\x61tures\x18\r \x01(\x0b\x32\x15.grid.v1.UserFeaturesR\x08\x66\x65\x61tures\x12:\n\x0bpreferences\x18\x0e \x01(\x0b\x32\x18.grid.v1.UserPreferencesR\x0bpreferences\"1\n\x0cUserFeatures\x12!\n\x0c\x62yoc_enabled\x18\x01 \x01(\x08R\x0b\x62yocEnabled\"?\n\x0fUserPreferences\x12,\n\x12\x64\x65\x66\x61ult_cluster_id\x18\x02 \x01(\tR\x10\x64\x65\x66\x61ultClusterId\"\xca\x01\n\x06\x41piKey\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12#\n\rsecret_sha256\x18\x02 \x01(\x0cR\x0csecretSha256\x12\x39\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAt\x12\x37\n\tlast_used\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x08lastUsed\x12\x17\n\x07raw_key\x18\x05 \x01(\tR\x06rawKey\"\xa5\x01\n\x12VerificationStatus\x12\x1f\n\x0bis_verified\x18\x01 \x01(\x08R\nisVerified\x12\x31\n\x14verification_channel\x18\x02 \x01(\tR\x13verificationChannel\x12;\n\x0bverified_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nverifiedAt\"\xec\x01\n\nUserStatus\x12%\n\x0einstalled_grid\x18\x01 \x01(\x08R\rinstalledGrid\x12)\n\x10\x63ompleted_signup\x18\x02 \x01(\x08R\x0f\x63ompletedSignup\x12\x1f\n\x0b\x63li_version\x18\x03 \x01(\tR\ncliVersion\x12\x1d\n\nis_blocked\x18\x04 \x01(\x08R\tisBlocked\x12L\n\x13verification_status\x18\x05 \x01(\x0b\x32\x1b.grid.v1.VerificationStatusR\x12verificationStatusB2Z0github.com/gridai/grid/grid-backend/apis/grid/v1b\x06proto3'
  ,
  dependencies=[grid_dot_v1_dot_metadata__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_USER = _descriptor.Descriptor(
  name='User',
  full_name='grid.v1.User',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='metadata', full_name='grid.v1.User.metadata', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='metadata', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='details', full_name='grid.v1.User.details', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='details', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='grid.v1.User.status', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='status', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=89,
  serialized_end=235,
)


_USERDETAILS = _descriptor.Descriptor(
  name='UserDetails',
  full_name='grid.v1.UserDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='auth_provider', full_name='grid.v1.UserDetails.auth_provider', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='authProvider', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='username', full_name='grid.v1.UserDetails.username', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='username', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='first_name', full_name='grid.v1.UserDetails.first_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='firstName', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='last_name', full_name='grid.v1.UserDetails.last_name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='lastName', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='email', full_name='grid.v1.UserDetails.email', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='email', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='api_keys', full_name='grid.v1.UserDetails.api_keys', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='apiKeys', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='picture_url', full_name='grid.v1.UserDetails.picture_url', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='pictureUrl', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='internal', full_name='grid.v1.UserDetails.internal', index=7,
      number=11, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='internal', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='phone_number', full_name='grid.v1.UserDetails.phone_number', index=8,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='phoneNumber', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='features', full_name='grid.v1.UserDetails.features', index=9,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='features', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='preferences', full_name='grid.v1.UserDetails.preferences', index=10,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='preferences', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=238,
  serialized_end=649,
)


_USERFEATURES = _descriptor.Descriptor(
  name='UserFeatures',
  full_name='grid.v1.UserFeatures',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='byoc_enabled', full_name='grid.v1.UserFeatures.byoc_enabled', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='byocEnabled', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=651,
  serialized_end=700,
)


_USERPREFERENCES = _descriptor.Descriptor(
  name='UserPreferences',
  full_name='grid.v1.UserPreferences',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='default_cluster_id', full_name='grid.v1.UserPreferences.default_cluster_id', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='defaultClusterId', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=702,
  serialized_end=765,
)


_APIKEY = _descriptor.Descriptor(
  name='ApiKey',
  full_name='grid.v1.ApiKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='grid.v1.ApiKey.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='id', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='secret_sha256', full_name='grid.v1.ApiKey.secret_sha256', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='secretSha256', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='grid.v1.ApiKey.created_at', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='createdAt', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='last_used', full_name='grid.v1.ApiKey.last_used', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='lastUsed', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='raw_key', full_name='grid.v1.ApiKey.raw_key', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='rawKey', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=768,
  serialized_end=970,
)


_VERIFICATIONSTATUS = _descriptor.Descriptor(
  name='VerificationStatus',
  full_name='grid.v1.VerificationStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='is_verified', full_name='grid.v1.VerificationStatus.is_verified', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='isVerified', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='verification_channel', full_name='grid.v1.VerificationStatus.verification_channel', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='verificationChannel', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='verified_at', full_name='grid.v1.VerificationStatus.verified_at', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='verifiedAt', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=973,
  serialized_end=1138,
)


_USERSTATUS = _descriptor.Descriptor(
  name='UserStatus',
  full_name='grid.v1.UserStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='installed_grid', full_name='grid.v1.UserStatus.installed_grid', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='installedGrid', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='completed_signup', full_name='grid.v1.UserStatus.completed_signup', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='completedSignup', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cli_version', full_name='grid.v1.UserStatus.cli_version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='cliVersion', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='is_blocked', full_name='grid.v1.UserStatus.is_blocked', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='isBlocked', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='verification_status', full_name='grid.v1.UserStatus.verification_status', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='verificationStatus', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1141,
  serialized_end=1377,
)

_USER.fields_by_name['metadata'].message_type = grid_dot_v1_dot_metadata__pb2._METADATA
_USER.fields_by_name['details'].message_type = _USERDETAILS
_USER.fields_by_name['status'].message_type = _USERSTATUS
_USERDETAILS.fields_by_name['api_keys'].message_type = _APIKEY
_USERDETAILS.fields_by_name['features'].message_type = _USERFEATURES
_USERDETAILS.fields_by_name['preferences'].message_type = _USERPREFERENCES
_APIKEY.fields_by_name['created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_APIKEY.fields_by_name['last_used'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_VERIFICATIONSTATUS.fields_by_name['verified_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_USERSTATUS.fields_by_name['verification_status'].message_type = _VERIFICATIONSTATUS
DESCRIPTOR.message_types_by_name['User'] = _USER
DESCRIPTOR.message_types_by_name['UserDetails'] = _USERDETAILS
DESCRIPTOR.message_types_by_name['UserFeatures'] = _USERFEATURES
DESCRIPTOR.message_types_by_name['UserPreferences'] = _USERPREFERENCES
DESCRIPTOR.message_types_by_name['ApiKey'] = _APIKEY
DESCRIPTOR.message_types_by_name['VerificationStatus'] = _VERIFICATIONSTATUS
DESCRIPTOR.message_types_by_name['UserStatus'] = _USERSTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

User = _reflection.GeneratedProtocolMessageType('User', (_message.Message,), {
  'DESCRIPTOR' : _USER,
  '__module__' : 'grid.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:grid.v1.User)
  })
_sym_db.RegisterMessage(User)

UserDetails = _reflection.GeneratedProtocolMessageType('UserDetails', (_message.Message,), {
  'DESCRIPTOR' : _USERDETAILS,
  '__module__' : 'grid.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:grid.v1.UserDetails)
  })
_sym_db.RegisterMessage(UserDetails)

UserFeatures = _reflection.GeneratedProtocolMessageType('UserFeatures', (_message.Message,), {
  'DESCRIPTOR' : _USERFEATURES,
  '__module__' : 'grid.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:grid.v1.UserFeatures)
  })
_sym_db.RegisterMessage(UserFeatures)

UserPreferences = _reflection.GeneratedProtocolMessageType('UserPreferences', (_message.Message,), {
  'DESCRIPTOR' : _USERPREFERENCES,
  '__module__' : 'grid.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:grid.v1.UserPreferences)
  })
_sym_db.RegisterMessage(UserPreferences)

ApiKey = _reflection.GeneratedProtocolMessageType('ApiKey', (_message.Message,), {
  'DESCRIPTOR' : _APIKEY,
  '__module__' : 'grid.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:grid.v1.ApiKey)
  })
_sym_db.RegisterMessage(ApiKey)

VerificationStatus = _reflection.GeneratedProtocolMessageType('VerificationStatus', (_message.Message,), {
  'DESCRIPTOR' : _VERIFICATIONSTATUS,
  '__module__' : 'grid.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:grid.v1.VerificationStatus)
  })
_sym_db.RegisterMessage(VerificationStatus)

UserStatus = _reflection.GeneratedProtocolMessageType('UserStatus', (_message.Message,), {
  'DESCRIPTOR' : _USERSTATUS,
  '__module__' : 'grid.v1.user_pb2'
  # @@protoc_insertion_point(class_scope:grid.v1.UserStatus)
  })
_sym_db.RegisterMessage(UserStatus)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
