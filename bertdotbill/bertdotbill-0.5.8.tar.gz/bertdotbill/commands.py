import base64
import json
import os
import re
import sys
from bertdotbill.config import ConfigUtil
from bertdotbill.logger import Logger
from bertdotbill.defaults import allowed_command_patterns

logger = Logger().init_logger(__name__)

class Commands:

  def __init__(self, settings, args, **kwargs):
    self.settings = settings
    self.args = args
    self.config_util = ConfigUtil()
    self.allowed_command_patterns = os.environ.get('ALLOWED_COMMAND_PATTERNS')
    if self.allowed_command_patterns:
      self.allowed_command_patterns = re.split('\\|', self.allowed_command_patterns)
    elif self.args.allowed_command_patterns:
      self.allowed_command_patterns = re.split('\\|', self.allowed_command_patterns)
    else:
      self.allowed_command_patterns = self.settings.get('allowed_command_patterns', allowed_command_patterns)
    self.allowed_command_patterns = re.compile('|'.join(self.allowed_command_patterns))

  def retrieve(self, **kwargs):
      logger.info('Retrieving available os commands')
      commands = self.settings.get('commands', {})
      encoded = kwargs.get('encoded')

      if isinstance(commands, dict):
        commands_platform_specific = [c for c in commands.get(sys.platform, [])]
        commands_common = [c for c in commands.get('common', [])]
        osCommand_list = commands_platform_specific + commands_common
        if len(osCommand_list) > 0:
          logger.debug('OS Command List is: %s' % osCommand_list)
        else:
          logger.warning('OS Command List is empty')
          return osCommand_list
        if encoded:
          osCommands_bytes = str(json.dumps(osCommand_list)).encode("ascii")
          encoded_osCommand_list = base64.b64encode(osCommands_bytes)
          encoded_osCommands = encoded_osCommand_list.decode("utf-8")
          return encoded_osCommands
        else: 
          return osCommand_list
      else:
        logger.warning("Improperly structured 'commands' config block, seek --help")

  def launch(self, command_key, args=None):
      
      osCommands = self.retrieve()
      logger.debug('Allowed command pattern is %s' % self.allowed_command_patterns)
      logger.info("Launching command mapped to '%s'" % command_key)
      cmd = None
      try:
        if isinstance(osCommands, list):
          for osCommandEntry in osCommands:
            for k,v in osCommandEntry.items():
              if k == command_key:
                cmd = v['cmd']
                if self.allowed_command_patterns.match(cmd):
                  logger.debug('Running command %s' % cmd)
                  os.system(cmd)
                else:
                  logger.warning('The command pattern "%s" is not allowed, please adjust your configuration file and/or seek --help' % cmd)
          if not cmd:
            logger.warning('No command key found for %s' % command_key)
            return False
        else:
          logger.warning("Improperly structured 'commands' config block, seek --help")
      except Exception as e:
        logger.error("I had a problem reading the command to be launched, check your config and/or seek --help")
