import os
import logging
import configparser
import traceback
import re
import time
# import sys
from distutils.util import strtobool
_log = logging.getLogger('pf_common')

# logging and pi3d.Log combined cause a mess in logging...
# if 'pi3d.util.Log' not in sys.modules:
#  print('import logging')
#  import logging


# -----------------------------------------------------------------------------------------------------------------------
def convert_basic_data_type(string_val):
  try:
    return int(string_val)
  except ValueError:
    pass
  try:
    return float(string_val)
  except ValueError:
    pass
  try:
    return strtobool(string_val)    
  except ValueError:
    pass
  return string_val


# -----------------------------------------------------------------------------------------------------------------------
def get_secret(config, secret_name):
  logging.debug("secrets_path={}".format(get_config_param(config, 'secrets_path')))
  secrets_path = get_config_param(config, 'secrets_path')
  secret_found = False
  secret = ''
  for secrets_fname in secrets_path.split(':'):
    _log.debug("working on {}".format(secrets_fname))
    try:
      with open(secrets_fname) as sf:
        secrets_content = sf.read()
        secrets = list(filter(lambda x: re.match('^'+secret_name+':\s*(.*)', x), secrets_content.split('\n')))
        if len(secrets) == 1:  # make duplicate fail
          secret = re.sub('{}:\s+'.format(secret_name), '', secrets[0])
          _log.debug("detected secret '{}: {}' in file '{}'.".format(secret_name, secret, secrets_fname))
          secret_found = True
          break
        elif len(secrets) > 1:
          _log.error("Found {:d} password entries in file '{}', which exceeds the expected number of one.".format(len(
            secrets), secrets_fname))
          exit(1)
    except FileNotFoundError:
      pass
  if not secret_found:
    _log.error("required secret '{}' was not found.".format(secret_name))
    _log.info("make sure any of the files {} exists and contains an entry like '{}: your-password'.".format(
      secrets_path.replace(':', ', '), secret_name))
    exit(1)
  return secret


# -----------------------------------------------------------------------------------------------------------------------
def get_config_param(config, parameter):
  this_host = os.uname()[1]
  elements = []

  try:
    section = 'DEFAULT'
    if config.has_section(this_host):
      section = this_host

    # config.getlist() requires configparser.ConfigParser(converters=...), see
    # https://stackoverflow.com/a/53274707 for details.
    for par in config.getlist(section, parameter):  # From: https://stackoverflow.com/a/53274707
      elements.append(convert_basic_data_type(par))
  except KeyError:
    _log.error("KeyError - get_config_param(): neither [{}] nor [DEFAULT] define '{}'".format(this_host, parameter))
    raise
  except configparser.NoOptionError:
    _log.error("NoOptionError - get_config_param(): neither [{}] nor [DEFAULT] define '{}'".format(this_host, parameter))
    raise

  # resolve environment variables HOME, HOSTNAME and PF_ROOT
  for env_sym in [r'\$HOME', r'\$HOSTNAME', r'\$PF_ROOT']:
    for e in range(0, len(elements)):
      if isinstance(elements[e], str):
        m = re.search(env_sym, elements[e])
        if m:
          if os.path.expandvars(env_sym[1:]) == env_sym[1:] and env_sym[1:] == '$HOSTNAME':
             elements[e] = elements[e].replace(env_sym[1:], os.uname()[1])
             _log.debug("Symbol $HOSTNAME was resolved using os.uname()")
          else:
            elements[e] = elements[e].replace(env_sym[1:], os.path.expandvars(env_sym[1:]))

  value_is_secret = False
  # check for !SECRET reference and resolve if found
  for e in range(0, len(elements)):
    if isinstance(elements[e], str):
      if elements[e][:7].upper() == '!SECRET':
        value_is_secret = True
        _log.debug("detected '!SECRET' in parameter {}={}".format(parameter, elements[e]))
        elements[e] = get_secret(config, re.sub('^!SECRET\s+', '', elements[e], flags=re.IGNORECASE))

  if len(elements) == 1:
    pvalue = elements[0]
    if value_is_secret:  # xxx
      switch = "/var/tmp/.pf-show-secrets"
      if os.path.exists(switch) and os.path.getmtime(switch) + 600 < time.time():
        try:
          os.remove(switch)
        except PermissionError:
          _log.info("cannot remove file. Traceback:\n{}".format(traceback.format_exc()))
      if not os.path.exists(switch):
        hint = " # 'touch /var/tmp/.pf-show-secrets' to display secrets for the next 10 minutes."
        pvalue = elements[0] if os.path.exists(switch) else "'{}'{}".format(re.sub('.', '*', elements[0]), hint)
    _log.info("get_config_param(): [{}] {} = {}".format(section, parameter, pvalue))
    return elements[0]
  _log.info("get_config_param(): [{}] {} = {}".format(section, parameter, elements))
  return elements
