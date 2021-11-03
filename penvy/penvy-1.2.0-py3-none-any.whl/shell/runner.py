import io
import os
import subprocess


def run_and_read_line(command: str, shell=False):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=shell)
    line = io.TextIOWrapper(proc.stdout, encoding="utf-8").read().rstrip()

    if not line:
        raise Exception(f"No output returned to stdout for: {command}")

    return line


def run_shell_command(command: str, cwd: str = os.getcwd(), shell=False):
    proc = subprocess.Popen(command, cwd=cwd, shell=shell)
    proc.communicate()

    if proc.returncode > 0:
        raise Exception(f"Shell command failed with code: {proc.returncode}")
