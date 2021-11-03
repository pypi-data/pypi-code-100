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
import subprocess

from elftools.elf.constants import P_FLAGS
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection
from elftools.common.exceptions import ELFError

from mcutk.exceptions import ReadElfError
from mcutk.appbase import APPBase
from mcutk.apps import appfactory



def transform_elf_basic(type, in_file, out_file, executor=None):
    """Transform ELF to specific type by arm-none-eabi-objcopy.

    Supported types: bin, ihex, srec.

    Arguments:
        type {str} -- which type you want to convert.
        in_file {str} -- path to elf file.
        out_file {str} -- output file
        executor {str} -- path to arm-none-eabi-objcopy, if it is None,
                    program will use the default executor(mcutk/bin/)

    Raises:
        ReadElfError -- Unknown elf format will raise such error
        Exception -- Convert failed will raise exception

    Returns:
        bool
    """
    supported = {
        'bin': "binary",
        'ihex': 'ihex',
        'srec': 'srec'
    }

    if type not in supported:
        raise ValueError("unknown type, valid choices are: %s"%(str(supported)))

    if executor is None:
        executor = "arm-none-eabi-objcopy"

    try:
        with open(in_file, 'rb') as fileobj:
            elffile = ELFFile(fileobj)
            for header_name in elffile.header:
                print('{:<10s} -- {:<10s}'.format(header_name, str(elffile.header[header_name])))
    except ELFError:
        raise ReadElfError('read elf error!')

    type = supported.get(type, type)
    cmds = '{0} -O {1} {2} {3}'.format(executor, type, in_file, out_file)

    return subprocess.call(cmds, shell=True) == 0




def transform_elf(ide, type, in_file, out_file):
    """Transform ELF to specific type with toolchain method (app.transform_elf).

    Supported types: bin, ihex, srec.

    Arguments:
        ide {str} -- ide name or ide app instance.
        type {str} -- which type you want to convert.
        in_file {str} -- path to elf file.
        out_file {str} -- output file

    Raises:
        ReadElfError -- Unknown elf format will raise such error
        Exception -- Convert failed will raise exception

    Returns:
        bool -- success or not.
    """
    if isinstance(ide, APPBase):
        app_instance = ide
    else:
        app_instance = appfactory(ide).get_latest()

    if not (app_instance and app_instance.is_ready):
        raise ValueError('Fatal error, not found toolchain "%s" in system!'%ide)

    return app_instance.transform_elf(type, in_file, out_file)


class ElfFile(object):

    def __init__(self, elffile):
        self.elf = elffile
        self._fileobject = open(self.elf, 'rb')
        self.elffile = ELFFile(self._fileobject)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._fileobject.close()

    def get_symbol(self, name):
        """Find and return Symbol object."""
        symbol = None
        name = name.lower()
        for section in self.elffile.iter_sections():
            if not isinstance(section, SymbolTableSection):
                continue
            for sym in section.iter_symbols():
                if sym.name.lower() == name:
                    symbol = sym
                    break
        return symbol

    def get_section(self, name):
        """Find and return Section object."""
        section = None
        name = name.lower()
        for sec in self.elffile.iter_sections():
            if sec.name.lower() == name:
                section = sec
                break
        return section

    @property
    def sp(self):
        """
        Parse and return stack pointer from ELF file.

        ARM Cortex-m family contains a vector table at the begining of memory.
        Vector table is a table of information about the initial stack pointer
        value and various exception handler addresses. For more please refer to
        ARM vector reset.
        """

        segments = list()
        # Find base address of memory
        for segment in self.elffile.iter_segments():
            # execute section
            if segment.header.p_type == 'PT_LOAD' \
                and segment.header.p_filesz != 0 \
                and (segment.header.p_flags & P_FLAGS.PF_X):
                segments.append(segment['p_vaddr'])
        segments.sort()
        return segments[0]

    def get_segments(self):
        """Get segments for load.
        """
        segments = list()
        for segment in self.elffile.iter_segments():
            if segment.header.p_type == 'PT_LOAD' and segment.header.p_filesz != 0:
                logging.info("Writing segment Addr:0x%08x, Vaddr:0x%08x, size %d",
                    segment['p_paddr'], segment['p_vaddr'], segment.header.p_filesz)
                segments.append(segment)
        return segments

    def is_to_flash(self, flash_addr):
        """Retrun a boolean to identify ELF is put to flash.

        Arguments:
            flash_addr: flash start address

        Return:
            Boolean
        """
        # convert to int
        if isinstance(flash_addr, str):
            flash_addr = int(flash_addr, 16)

        to_flash = False
        segments = self.get_segments()
        # check segment addr if is hit the flash area
        for segment in segments:
            if segment['p_paddr'] >= flash_addr:
                to_flash = True
                break
        return to_flash
