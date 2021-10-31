# Copyright (C) 2021  Torgny Bjers <torgny@bjers.org>
# This file is released under the GNU GPL, version 3 or a later revision.
# For further details see the COPYING file

import argparse
import logging

from alot.helper import call_cmd_async, split_commandstring
from alot.commands import Command, registerCommand
from alot.settings.const import settings


MODE = 'global'

class CheckMailFailed(RuntimeError):
    pass

@registerCommand(MODE, 'checkmail')
class CheckMailCommand(Command):
    def __init__(self, thread=None, **kwargs):
        try:
            if 'checkmail' not in settings._config:
                raise Exception('Missing configuration [checkmail]')
            self.config = settings._config.get('checkmail')
        except Exception as e:
            if ui:
                ui.notify('Missing configuration [checkmail]', priority='error')
        Command.__init__(self, **kwargs)

    async def apply(self, ui):
        try:
            logging.info('checkmail starting...')
            if ui:
                widget = ui.notify('Checking mail...', priority='normal', timeout=-1, block=False)
            conf = settings._config.get('checkmail')
            cmdlist = split_commandstring(conf['command'])
            out, err, code = await call_cmd_async(cmdlist)
            if ui:
                ui.clear_notify([widget])
                if code == 0 and out.strip():
                    message = ''.join([c for c in out.replace('\n', ' ') if c not in ['\t', '\r', '\n']])
                    ui.notify(message, priority='normal', timeout=3, block=False)
            if code != 0:
                if ui:
                    ui.notify('Failed to check mail.', priority='error')
                raise Exception('syncmail returned with code {}{}'.format(code, ':\n' + err.strip() if err else '.'))
        except Exception as e:
            logging.error(str(e))
            raise CheckMailFailed(str(e))
        logging.info('Fetched mail successfully.')
        logging.info(out)
