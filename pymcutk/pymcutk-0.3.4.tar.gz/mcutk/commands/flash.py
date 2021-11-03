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

import os
import logging
import yaml
import click

from mcutk.apps import appfactory
from mcutk.board import Board
from mcutk.managers.debug_helper import Debughelper

LEVELS = {
    'warning': logging.WARNING,
    'debug': logging.DEBUG,
    'info': logging.INFO
}


@click.command('flash', short_help='flash debug file to board')
@click.argument('path', required=True, type=click.Path(exists=True))
@click.option('-u', '--usbid', help='unique usb id')
@click.option('-a', '--base-address', default=0, help='base address to load.')
@click.option('-c', '--config-file', help='load config from file.')
def cli(path, usbid, base_address, config_file):
    # config logging
    level = LEVELS.get('info', logging.INFO)
    format = '[%(levelname)s] %(message)s'
    logging.basicConfig(level=level, format=format)

    # get arm-none-eabi-gdb
    gdb = None
    armgcc = appfactory('armgcc').get_latest()
    if armgcc and armgcc.is_ready:
        gdb = os.path.join(armgcc.path, 'bin/arm-none-eabi-gdb')

    # load from config file
    device = dict()
    if config_file:
        with open(config_file) as file:
            config = yaml.safe_load(file)
            device = config.get('board')

    if usbid:
        device['usbid'] = usbid

    # prepare debugger and device
    debugger, device = Debughelper.choose_device(device)
    if not device:
        exit(1)

    board = Board(**device)
    board.debugger = debugger
    board.debugger.gdbpath = gdb
    click.secho(str(board), fg="yellow")

    if base_address:
        board.start_address = base_address

    ret = board.programming(path)
    if ret[0] == 0:
        click.secho('Flash programming successful!', fg="green")
        exit(0)
    else:
        click.secho('Flash programming failed!', fg="red")
        exit(1)