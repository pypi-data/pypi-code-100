# -*- coding: utf-8 -*-
# vim: set ts=4
#
# Copyright 2021-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import contextlib
import logging
import os
from pathlib import Path
import signal
import subprocess
import time


LOG = logging.getLogger("tuxrun")


class Runtime:
    binary = ""
    container = False
    prefix = [""]

    def __init__(self):
        self.__bindings__ = []
        self.__image__ = None
        self.__name__ = None
        self.__pre_proc__ = None
        self.__proc__ = None
        self.__sub_procs__ = []
        self.__ret__ = None

    @classmethod
    def select(cls, name):
        if name == "docker":
            return DockerRuntime
        if name == "podman":
            return PodmanRuntime
        return NullRuntime

    def bind(self, src, dst=None, ro=False):
        if dst is None:
            dst = src
        self.__bindings__.append((src, dst, ro))

    def image(self, image):
        self.__image__ = image

    def name(self, name):
        self.__name__ = name

    def pre_run(self, tmpdir):
        pass

    def post_run(self):
        pass

    def cmd(self, args):
        raise NotImplementedError()  # pragma: no cover

    @contextlib.contextmanager
    def run(self, args):
        args = self.cmd(args)
        LOG.debug("Calling %s", " ".join(args))
        try:
            self.__proc__ = subprocess.Popen(
                args,
                bufsize=1,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setpgrp,
            )
            yield
        except FileNotFoundError as exc:
            LOG.error("File not found '%s'", exc.filename)
            raise
        except Exception as exc:
            LOG.exception(exc)
            if self.__proc__ is not None:
                self.kill()
                _, errs = self.__proc__.communicate()
                for err in [e for e in errs.split("\n") if e]:
                    LOG.error("err: %s", err)
            raise
        finally:
            if self.__proc__ is not None:
                self.__ret__ = self.__proc__.wait()
            for proc in self.__sub_procs__:
                proc.wait()

    def lines(self):
        return self.__proc__.stderr

    def kill(self):
        if self.__proc__:
            self.__proc__.send_signal(signal.SIGTERM)

    def ret(self):
        return self.__ret__


class ContainerRuntime(Runtime):
    container = True

    def __init__(self):
        super().__init__()
        self.bind("/boot", ro=True)
        self.bind("/lib/modules", ro=True)
        # Bind /dev/kvm is available
        if Path("/dev/kvm").exists():
            self.bind("/dev/kvm")
        # Bind /var/tmp/.guestfs-$id if available
        guestfs = Path(f"/var/tmp/.guestfs-{os.getuid()}")
        if guestfs.exists():
            self.bind(guestfs, "/var/tmp/.guestfs-0")

    def cmd(self, args):
        prefix = self.prefix.copy()
        srcs = set()
        dsts = set()
        for binding in self.__bindings__:
            (src, dst, ro) = binding
            if src in srcs:
                LOG.error("Duplicated mount source %r" % src)
                raise Exception("Duplicated mount source %r" % src)
            if dst in dsts:
                LOG.error("Duplicated mount destination %r" % dst)
                raise Exception("Duplicated mount destination %r" % dst)
            srcs.add(src)
            dsts.add(dst)
            ro = "ro" if ro else "rw"
            prefix.extend(["-v", f"{src}:{dst}:{ro}"])
        prefix.extend(["--name", self.__name__])
        return prefix + [self.__image__] + args

    def kill(self):
        args = [self.binary, "stop", "--time", "60", self.__name__]
        with contextlib.suppress(FileNotFoundError):
            proc = subprocess.Popen(
                args,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                preexec_fn=os.setpgrp,
            )
            self.__sub_procs__.append(proc)


class DockerRuntime(ContainerRuntime):
    binary = "docker"
    prefix = ["docker", "run", "--rm", "--hostname", "tuxrun"]

    def pre_run(self, tmpdir):
        self.bind("/var/run/docker.sock")


class PodmanRuntime(ContainerRuntime):
    binary = "podman"
    prefix = ["podman", "run", "--rm", "--quiet", "--hostname", "tuxrun"]

    def pre_run(self, tmpdir):
        socket = tmpdir / "podman.sock"
        self.bind(socket, "/run/podman/podman.sock")
        args = [
            self.binary,
            "system",
            "service",
            "--time",
            "0",
            f"unix://{socket}",
        ]
        self.__pre_proc__ = subprocess.Popen(
            args,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            preexec_fn=os.setpgrp,
        )
        # wait for the socket
        for i in range(0, 60):
            if socket.exists():
                return
            time.sleep(1)
        raise Exception(f"Unable to create podman socket at {socket}")

    def post_run(self):
        if self.__pre_proc__ is None:
            return
        self.__pre_proc__.kill()
        self.__pre_proc__.wait()


class NullRuntime(Runtime):
    def cmd(self, args):
        return args
