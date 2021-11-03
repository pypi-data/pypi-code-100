#
# MIT License
#
# Copyright 2021 NXP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import logging
import click

import prettytable as pt
from mcutk.apps import appfactory
from mcutk.managers.conf_mgr import ConfMgr
from . import TOOLCHAINS

@click.command('config', short_help='configuration(\"~/.mcutk\") management')
@click.option('--show', is_flag=True, help='show configuration from \"~/.mcutk\"')
@click.option('--auto', is_flag=True, help='auto scan your system, then configure into \"~/.mcutk\"')
def cli(show, auto):
    """Configuration Management Command"""
    cfger = ConfMgr.load()

    if show:
        if cfger.is_empty:
            print("Need to initialize the mcutk")
            return
        else:
            cfger.show()

    if auto:
        print("Discover installed toolchains from your system ...\n")
        tb = pt.PrettyTable()
        tb.align = 'l'
        tb.field_names = ["name", "version", "path"]
        toolchains = list()

        for toolname in TOOLCHAINS:
            try:
                tool = appfactory(toolname)
                app = tool.get_latest()
                if app and app.is_ready:
                    toolchains.append(app)
                    tb.add_row([app.name, app.version, app.path])
                    cfger.set_app(app)
                else:
                    logging.debug("not found tool: %s", toolname)
            except:
                logging.exception("failed to discover tool %s", toolname)

        cfger.save()
        print(tb)
        print("\n\"{}\" has been updated successfully!\n".format(cfger.CONFIG_FILE))
