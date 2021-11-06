# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2021 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
CORE Office commands
"""

import sys

from rattail import commands
from rattail_corepos import __version__
from rattail.util import load_object


def main(*args):
    """
    Entry point for 'core-office' commands
    """
    if args:
        args = list(args)
    else:
        args = sys.argv[1:]

    cmd = Command()
    cmd.run(*args)


class Command(commands.Command):
    """
    Primary command for CORE Office
    """
    name = 'core-office'
    version = __version__
    description = "core-office -- command line interface for CORE Office"
    long_description = ""


class ExportLaneOp(commands.ImportSubcommand):
    """
    Export "op" data from CORE Office to CORE Lane
    """
    name = 'export-lane-op'
    description = __doc__.strip()
    default_handler_spec = 'rattail_corepos.corepos.lane.importing.op.office:FromCoreOfficeToCoreLane'
    default_dbkey = 'default'

    def get_handler_factory(self, **kwargs):
        if self.config:
            spec = self.config.get('corepos.lane.importing', 'office.handler',
                                   default=self.default_handler_spec)
        else:
            # just use default, for sake of cmd line help
            spec = self.default_handler_spec
        return load_object(spec)

    def add_parser_args(self, parser):
        super(ExportLaneOp, self).add_parser_args(parser)
        parser.add_argument('--dbkey', metavar='KEY', default=self.default_dbkey,
                            help="Config key for database engine to be used as the "
                            "\"target\" CORE Lane DB, i.e. where data will be "
                            " exported.  This key must be defined in the "
                            " [rattail_corepos.db.lane_op] section of your "
                            "config file.")

    def get_handler_kwargs(self, **kwargs):
        if 'args' in kwargs:
            kwargs['dbkey'] = kwargs['args'].dbkey
        return kwargs
