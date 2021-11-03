#!/bin/false
# -*- coding: utf-8 -*-

""" Tolls for JSON and YAML encoding/decoding. """


# ------------------------------------------------------------------------------------------------------------------------
# Main imports
# ------------------------------------------------------------------------------------------------------------------------
import datetime
from io import FileIO
import json
import os
from types import ModuleType
from typing import Any, Union, IO, Optional

# ------------------------------------------------------------------------------------------------------------------------
# Import checks
# ------------------------------------------------------------------------------------------------------------------------
try:
    import yaml
    HAVE_YAML = True
except ImportError:  # pragma: no cover
    HAVE_YAML = False

if HAVE_YAML:
    try:
        from yaml import CLoader as YamlLoader, CDumper as YamlDumper
    except ImportError:
        from yaml import Loader as YamlLoader, Dumper as YamlDumper

# ------------------------------------------------------------------------------------------------------------------------
# Debug functions
# ------------------------------------------------------------------------------------------------------------------------
"""
Global flag for whether or not to log encoding error debugging info when encoding fails.
This is initialized with the content of environment variable 'PTUTILS_ENABLE_ENCODER_DEBUG'.
"""
PTUTILS_ENABLE_ENCODER_DEBUG = (
    os.environ.get('PTUTILS_ENABLE_ENCODER_DEBUG', '').lower()
    in
    ['yes', 'true', 'on', 'enabled']
)


# ------------------------------------------------------------------------------------------------------------------------
def debug_encoder_failure(obj: Any) -> None:

    if PTUTILS_ENABLE_ENCODER_DEBUG:  # pragma: no cover
        # dont create a logger unless we need it...
        from ptutils.logging import getLogger
        logger = getLogger(__name__)

        # dump some useful information about the failure
        try:
            logger.debug('#' * 80)
            logger.debug('# JSON Encoding error. Unable to encode object as JSON.')
            logger.debug("# Object details:")
            logger.debug("#   class name:     %s" % type(obj).__name__)
            logger.debug("#   Representation: %s" % repr(obj))
            logger.debug("#   String:         %s" % str(obj))
            logger.debug('#' * 80)
        except:  # noqa E722 # pylint: disable=broad-except
            logger.exception("Error debugging object JSON serialization failure.")


# ------------------------------------------------------------------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------------------------------------------------------------------
def json_serial(obj: Any) -> Any:
    """
    JSON serialization helper for objects not serializable by default.

    Parameters
    ----------
    obj : Any
        The object to be serialized

    Returns
    -------
    Any
        An object which is serializable by the `json` python standard library.

    Raises
    ------
    TypeError
        If the object could not be converted to a serializable type.

    Notes
    -----
    This function provides serialization for `datetime.datetime`,
    `datetime.timedelta`, and `datetime.date`.
    For other types, a TypeError will be raised, and some debugging information
    about the encoding failure will be logged using `logger.debug`.

    """
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        return obj.total_seconds()

    debug_encoder_failure(obj)

    raise TypeError(f"Type {type(obj).__name__} not serializable.")


# ------------------------------------------------------------------------------------------------------------------------
def encode_json(obj: Any) -> str:
    """
    Encode the object as a JSON string

    Parameters
    ----------
    obj : Any
        The object to encode

    Returns
    -------
    str
        A JSON string representation of the object.
    """
    return json.dumps(obj, sort_keys=True, indent=4, separators=[', ', ': '], default=json_serial)


# ------------------------------------------------------------------------------------------------------------------------
def pretty_json(obj: Any) -> str:
    """
    Encode the object as a JSON string in human-friendly format.

    Parameters
    ----------
    obj : Any
        The object to encode

    Returns
    -------
    str
        A JSON string representation of the object.
    """
    return encode_json(obj)


# ------------------------------------------------------------------------------------------------------------------------
def decode_json(text: str) -> Any:
    """
    Encode a JSON string into a python object.

    Parameters
    ----------
    text : str
        The JSON text to parse.

    Returns
    -------
    Any
        The decoded object.
    """
    return json.loads(text)


# ------------------------------------------------------------------------------------------------------------------------
def require_yaml() -> ModuleType:
    """
    Ensure that YAML encoder is installed or else raise an exception.

    Returns
    -------
    ModuleType
        The yaml module itself.

    Raises
    ------
    Exception
        When YAML encoder can not be imported.
    """
    if not HAVE_YAML:  # pragma: no cover
        raise Exception("YAML encoder is not available. Try 'pip install pyyaml'")

    return yaml


# ------------------------------------------------------------------------------------------------------------------------
def decode_yaml(text_or_stream: Union[str, IO]) -> Any:
    """
    Decode a YAML string into a python object.

    Parameters
    ----------
    text_or_stream : Union[str, IO]
        Either a string literal containing YAML formatted markup, or an object
        providing the stream protocol whose contents will be read and then parsed.

    Returns
    -------
    Any
        The python object described by the yaml text.

    Raises
    ------
    Exception
        When YAML encoder can not be imported.
    """
    require_yaml()
    return yaml.load(text_or_stream, Loader=YamlLoader)


# ------------------------------------------------------------------------------------------------------------------------
def encode_yaml(obj: Any, filp: Optional[FileIO] = None) -> str:
    """
    Serialize an object to a YAML-formatted string.

    Parameters
    ----------
    obj : Any
        The object to be serialized.
    filp : FileIO, optional
        A file to write to insetead of returning a string

    Returns
    -------
    str
        The YAML-formatted string representation of `obj`

    Raises
    ------
    Exception
        When YAML encoder can not be imported.
    """
    require_yaml()
    if filp is not None:
        return yaml.dump(obj, filp, explicit_start=True, default_flow_style=False, Dumper=YamlDumper)
    else:
        return yaml.dump(obj, explicit_start=True, default_flow_style=False, Dumper=YamlDumper)


# ------------------------------------------------------------------------------------------------------------------------
def pretty_yaml(obj: Any) -> str:
    """
    Serialize an object to a human-friendly, YAML-formatted string.

    Parameters
    ----------
    obj : Any
        The object to be serialized.

    Returns
    -------
    str
        The YAML-formatted string representation of `obj`

    Raises
    ------
    Exception
        When YAML encoder can not be imported.
    """
    return encode_yaml(obj)
