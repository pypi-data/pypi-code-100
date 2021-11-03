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

import sys
import logging
import click
from mcutk import __version__


class ComplexCLI(click.MultiCommand):

    COMMANDS = [
        'build',
        'scan',
        'config',
        # 'gdbserver',
        'flash'
    ]

    def list_commands(self, ctx):
        return self.COMMANDS

    def get_command(self, ctx, name):
        if sys.version_info[0] == 2:
            name = name.encode('ascii', 'replace')
        mod = __import__('mcutk.commands.' + name, None, None, ['cli'])
        return mod.cli



@click.command(cls=ComplexCLI, invoke_without_command=True, help="mcutk command line tool")
@click.option('-v', '--verbose', is_flag=True, help='show more console message')
@click.option('--version', is_flag=True, help="show mcutk version")
def main(version=False, verbose=False, debug=False):
    if verbose:
        logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.DEBUG)
    else:
        logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.WARNING)

    if version:
        click.echo(__version__)


if __name__ == '__main__':
    main()
