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
from typing import List

from absolute_control.models import process
from psutil import AccessDenied, Popen, process_iter


def get_process_by_id(pid: int) -> process.Model:
    """
    Return a process with the given pid.

    Args:
        pid (int): The pid of the process to find.

    Returns:
        process.Model: The process with the given pid.
    """    
    for p in process_iter():
        if p.pid == pid:
            return process.Model.from_process(p)
    return None

def get_all_processes() -> List[process.Model]:
    """
    Return a list of all processes.

    Returns:
        List[process.Model]: A list of all processes.
    """
    return [process.Model.from_process(p) for p in process_iter()]

def get_processes_by_name(name: str) -> List[process.Model]:
    """
    Return a list of processes with the given name.

    Args:
        name (str): The name of the processes to find.

    Returns:
        List[process.Model]: A list of processes with the given name.
    """
    return [p for p in get_all_processes() if p.name == name]

def open_process_using_command(command: str) -> process.Model:
    """
    Open a process using the given command.

    Args:
        command (str): The command to use to open the process.

    Returns:
        process.Model: A process model with the given command.
    """
    return process.Model.from_process(Popen(command.split()))

def kill_process_by_id(pid: int) -> None:
    """
    Kill a process with the given pid.

    Args:
        pid (int): The pid of the process to kill.
    """    
    for p in process_iter():
        if p.pid == pid:
            p.kill()

def kill_processes_by_name(name: str) -> None:
    """
    Kills all processes with the given name.

    Args:
        name (str): The name of the processes to kill.
    """
    for p in process_iter():
        if p.name() == name:
            p.kill()

def kill_all_processes() -> None:
    """
    Kills all processes.

    Ignores when access is denied.
    """    
    for p in process_iter():
        try:
            p.kill()
        except AccessDenied:
            pass
