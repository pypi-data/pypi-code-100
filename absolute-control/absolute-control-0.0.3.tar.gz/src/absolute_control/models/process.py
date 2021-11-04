# Copyright (c) 2021 Johnathan P. Irvin
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from dataclasses import dataclass
from subprocess import PIPE
from typing import List

from psutil import Popen


@dataclass
class Model:
    pid: int
    name: str
    cmdline: List[str]
    status: str
    username: str
    cpu_percent: float
    memory_percent: float
    stdin: PIPE
    stdout: PIPE
    stderr: PIPE

    @classmethod
    def from_process(cls, process: Popen) -> 'Model':
        """
        Create a Process model from a Popen object.

        Args:
            process (Popen): A Popen object.

        Returns:
            Model: A Process model.
        """
        return cls(
            pid=process.pid,
            name=process.name(),
            cmdline=process.cmdline(),
            status=process.status(),
            username=process.username(),
            cpu_percent=process.cpu_percent(),
            memory_percent=process.memory_percent(),
            stdin=process.stdin,
            stdout=process.stdout,
            stderr=process.stderr
        )
