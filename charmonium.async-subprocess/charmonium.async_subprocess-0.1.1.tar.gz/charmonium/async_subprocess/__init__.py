from __future__ import annotations
import io
import asyncio
import textwrap
import datetime
import shlex
from typing import IO, Any, Optional, Sequence, Mapping, Union, Optional, Dict, cast
import subprocess
import os
from pathlib import Path


__version__ = "0.1.1"


StrBytes = Union[str, bytes]


class CalledProcessError(Exception):
    """Like `subprocess.CalledProcessError` but also writes stdout and stderr."""

    # unfortunately, Exception is not compatible with @dataclass
    def __init__(
        self,
        args2: Sequence[StrBytes],
        stdout: Optional[StrBytes],
        stderr: Optional[StrBytes],
        returncode: int,
    ) -> None:
        self.args2 = args2
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode

    def __str__(self) -> str:
        output = f"""
Command returned non-zero exit status {self.returncode}
command:
  {self.args2!s}"""
        if self.stdout:
            value = (
                self.stdout.decode() if isinstance(self.stdout, bytes) else self.stdout
            )
            output += "\nstdout:\n" + textwrap.indent(value, "  ")
        if self.stderr:
            value = (
                self.stderr.decode() if isinstance(self.stderr, bytes) else self.stderr
            )
            output += "\nstderr:\n" + textwrap.indent(value, "  ")
        return output


async def run(
    args: Sequence[StrBytes],
    cwd: Optional[Path] = None,
    env: Optional[Union[Mapping[StrBytes, StrBytes]]] = None,
    env_override: Optional[Mapping[StrBytes, StrBytes]] = None,
    capture_output: bool = False,
    check: bool = False,
    text: Optional[bool] = None,
) -> subprocess.CompletedProcess:
    """An async clone of `subprocess.run`.

    Suppose you have Python script that orchestrates shell commands,
    but it's too slow, and you've identified commands which can run in
    parallel. You could use `threading`, but that has GIL problems, or
    `multiprocess`, which has a high startup-cost per worker. You are
    already spinning off subprocesses, which the OS will run
    concurrently, so why not use async/await programming to express
    concurrency in a single thread?

    Note this function does not permit you to communicate
    asynchronously, just to run commands asynchronously.

    This function supports a subset of the signature of
    `subprocess.run`, that I will expand based on need. If you need
    some functionality, submit an issue or PR.

    """

    env = cast(Dict[StrBytes, StrBytes], dict(env if env is not None else os.environ))  # type: ignore
    if env_override:
        env.update(env_override)

    if capture_output:
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE

    proc = await asyncio.create_subprocess_exec(
        *args,
        stdin=subprocess.DEVNULL,
        stdout=stdout,
        stderr=stderr,
        cwd=cwd,
        env=cast(Mapping[str, str], env),
    )

    cap_stdout: Optional[Union[str, bytes]]
    cap_stderr: Optional[Union[str, bytes]]
    if capture_output:
        cap_stdout, cap_stderr = await proc.communicate()
        if text:
            cap_stdout = cap_stdout.decode()
            cap_stderr = cap_stderr.decode()
    else:
        cap_stdout, cap_stderr = None, None
        await proc.wait()

    rc = proc.returncode
    assert rc is not None
    if check and rc != 0:
        raise CalledProcessError(args, cap_stdout, cap_stderr, rc)

    return subprocess.CompletedProcess(args, rc, cap_stdout, cap_stderr)

__all__ = ["run", "CalledProcessError"]
