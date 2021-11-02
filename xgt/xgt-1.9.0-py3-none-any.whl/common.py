# -*- coding: utf-8 -*- --------------------------------------------------===#
#
#  Copyright 2018-2021 Trovares Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#===----------------------------------------------------------------------===#

import logging

import grpc

from . import DataService_pb2 as data_proto
from . import ErrorMessages_pb2 as err_proto

log = logging.getLogger(__name__)

BOOLEAN = 'boolean'
INT = 'int'
FLOAT = 'float'
DATE = 'date'
TIME = 'time'
DATETIME = 'datetime'
IPADDRESS = 'ipaddress'
TEXT = 'text'
LIST = 'list'

# Send in 2MB chunks (grpc recommends 16-64 KB, but this got the best performance locally)
# FYI: by default grpc only supports up to 4MB.
MAX_PACKET_SIZE = 2097152

class XgtError(Exception):
  """
  Base exception class from which all other xgt exceptions inherit. It is
  raised in error cases that don't have a specific xgt exception type.
  """
  def __init__(self, msg, trace=''):
    self.msg = msg
    self.trace = trace

    if log.getEffectiveLevel() >= logging.DEBUG:
      if self.trace != '':
        log.debug(self.trace)
      else:
        log.debug(self.msg)
    Exception.__init__(self, self.msg)

class XgtNotImplemented(XgtError):
  """Raised for functionality with pending implementation."""
class XgtInternalError(XgtError):
  """
  Intended for internal server purposes only. This exception should not become
  visible to the user.
  """
class XgtIOError(XgtError):
  """An I/O problem occurred either on the client or server side."""
  def __init__(self, msg, trace='', job = None):
    self._job = job
    XgtError.__init__(self, msg, trace)

  @property
  def job(self):
    """Job: Job associated with the load/insert operation if available. May be None."""
    return self._job
class XgtServerMemoryError(XgtError):
  """
  The server memory usage is close to or at capacity and work could be lost.
  """
class XgtConnectionError(XgtError):
  """
  The client cannot properly connect to the server. This can include a failure
  to connect due to an xgt module version error.
  """
class XgtSyntaxError(XgtError):
  """A query was provided with incorrect syntax."""
class XgtTypeError(XgtError):
  """
  An unexpected type was supplied.

  For queries, an invalid data type was used either as an entity or as a
  property. For frames, either an edge, vertex or table frames was expected
  but the wrong frame type or some other data type was provided. For
  properties, the property declaration establishes the expected data type. A
  type error is raise if the data type used is not appropriate.
  """
class XgtValueError(XgtError):
  """An invalid or unexpected value was provided."""
class XgtNameError(XgtError):
  """
  An unexpected name was provided. Typically can occur during object retrieval
  where the object name was not found.
  """
class XgtArithmeticError(XgtError):
  """An invalid arithmetic calculation was detected and cannot be handled."""
class XgtFrameDependencyError(XgtError):
  """
  The requested action will produce an invalid graph or break a valid graph.
  """
class XgtTransactionError(XgtError):
  """A Transaction was attempted but didn't complete."""
class XgtSecurityError(XgtError):
  """A security violation occured."""

# Validation support functions

def _validated_schema(obj):
  '''Takes a user-supplied object and returns a valid schema.

  Users can supply a variety of objects as valid schemas. To simplify internal
  processing, we canonicalize these into a list of string-type pairs,
  performing validation along the way.
  '''
  # Validate the shape first
  try:
    if len(obj) < 1:
      raise XgtTypeError('A schema must not be empty.')
    for col in obj:
      assert len(col) >= 2
      if (_validated_property_type(col[1]) == "LIST"):
        assert (len(col) <= 4 and len(col) >= 3)
      else:
        assert len(col) == 2
  except:
    raise XgtTypeError('A schema must be a non-empty list of (property, type) pairs.')
  # Looks good. Return a canonical schema.
  schema_returned = []
  for col in obj:
    val_type = _validated_property_type(col[1])
    if val_type != "LIST":
      schema_returned.append((_validated_property_name(col[0]), val_type))
    else:
      leaf_type = _validated_property_type(col[2])
      if (len(col) != 4):
        schema_returned.append((_validated_property_name(col[0]),
                               val_type, leaf_type))
      else:
        schema_returned.append((_validated_property_name(col[0]),
                                val_type, leaf_type, col[3]))
  return schema_returned

def _validated_frame_name(obj):
  '''Takes a user-supplied object and returns a unicode frame name string.'''
  _assert_isstring(obj)
  name = str(obj)
  if len(name) < 1:
    raise XgtNameError('Frame names cannot be empty.')
  if '.' in name:
    raise XgtNameError('Frame names cannot contain periods: '+name)
  return name

def _validated_namespace_name(obj):
  '''Takes a user-supplied object and returns a unicode frame name string.'''
  _assert_isstring(obj)
  name = str(obj)
  if len(name) < 1:
    raise XgtNameError('Namespace names cannot be empty.')
  if '.' in name:
    raise XgtNameError('Namespace names cannot contain periods: '+name)
  return name

def _validated_property_name(obj):
  '''Takes a user-supplied object and returns a unicode proprty name string.'''
  _assert_isstring(obj)
  return str(obj)

def _get_valid_property_types_to_create():
  return [BOOLEAN, INT, FLOAT, DATE, TIME, DATETIME, IPADDRESS, TEXT, LIST]

def _get_valid_property_types_for_return_only():
  return ['container_id', 'job_id']

def _validated_property_type(obj):
  '''Takes a user-supplied object and returns an xGT schema type.'''
  _assert_isstring(obj)
  prop_type = str(obj)
  valid_prop_types = _get_valid_property_types_to_create()
  if prop_type.lower() not in valid_prop_types:
    if prop_type.lower in _get_valid_property_types_for_return_only():
      raise XgtTypeError('Invalid property type "'+prop_type+'". This type '
                         'cannot be used when creating a frame.')
    else:
      raise XgtTypeError('Invalid property type "'+prop_type+'"')
  return prop_type.upper()

def _validate_opt_level(optlevel):
  """
  Valid optimization level values are:
    - 0: No optimization.
    - 1: General optimization.
    - 2: WHERE-clause optimization.
    - 3: Degree-cycle optimization.
    - 4: Query order optimization.
  """
  if isinstance(optlevel, int):
    if optlevel not in [0, 1, 2, 3, 4]:
      raise XgtValueError("Invalid optlevel '" + str(optlevel) +"'")
  else:
    raise XgtTypeError("optlevel must be an integer")
  return True

def _assert_noerrors(response):
  if len(response.error) > 0:
    error = response.error[0]
    try:
      error_code_name = err_proto.ErrorCodeEnum.Name(error.code)
      error_class = _code_error_map[error_code_name]
      raise error_class(error.message, error.detail)
    except XgtError:
      raise
    except Exception as ex:
      raise XgtError("Error detected while raising exception" +
                     str(ex), str(ex))

def _assert_isstring(value):
  if not isinstance(value, str):
    msg = str(value) + " is not a string"
    raise TypeError(msg)

_code_error_map = {
  'GENERIC_ERROR': XgtError,
  'NOT_IMPLEMENTED': XgtNotImplemented,
  'INTERNAL_ERROR': XgtInternalError,
  'IO_ERROR': XgtIOError,
  'SERVER_MEMORY_ERROR': XgtServerMemoryError,
  'CONNECTION_ERROR': XgtConnectionError,
  'SYNTAX_ERROR': XgtSyntaxError,
  'TYPE_ERROR': XgtTypeError,
  'VALUE_ERROR': XgtValueError,
  'NAME_ERROR': XgtNameError,
  'ARITHMETIC_ERROR': XgtArithmeticError,
  'FRAME_DEPENDENCY_ERROR': XgtFrameDependencyError,
  'TRANSACTION_ERROR': XgtTransactionError,
  'SECURITY_ERROR': XgtSecurityError,
}
