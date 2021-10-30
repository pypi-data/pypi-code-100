# This file is placed in the Public Domain.


import getpass
import os
import pwd
import sys
import time


from .dpt import Dispatcher
from .lop import Loop
from .obj import Object, cdir, get, update
from .obj import Cfg as ObjCfg
from .prs import parse
from .tbl import Table
from .thr import launch
from .utl import spl


starttime = time.time()


def getmain(name):
    return getattr(sys.modules["__main__"], name, None)


class Cfg(Object):

    console = False
    daemon = False
    debug = False
    index = None
    mods = ""
    name = ""
    systemd = False
    verbose = False
    version = None

class Runtime(Dispatcher, Loop):

    classes = Object()
    cmds = Object()
    opts = Object()
    prs = Object()

    def __init__(self):
        Dispatcher.__init__(self)
        Loop.__init__(self)
        self.register("cmd", Runtime.handle)

    def add(self, cmd):
        Table.add(cmd)

    @staticmethod
    def cmd(clt, txt):
        if not txt:
            return None
        e = clt.event(txt)
        e.origin = "root@shell"
        Runtime.handle(clt, e)
        e.wait()
        return None

    def do(self, e):
        self.dispatch(e)

    def error(self, txt):
        pass

    @staticmethod
    def handle(clt, obj):
        obj.parse()
        f = None
        mn = get(Table.modnames, obj.prs.cmd, None)
        if mn:
            mod = sys.modules.get(mn, None)
            if mod:
                f = getattr(mod, obj.prs.cmd, None)
        if not f:
            f = get(Runtime.cmds, obj.prs.cmd, None)
        if f:
            f(obj)
            obj.show()
        obj.ready()

    def init(self, mns, threaded=False):
        for mn in spl(mns):
            mod = sys.modules.get(mn, None)
            i = getattr(mod, "init", None)
            if i:
                self.log("init %s" % mn)
                if threaded:
                    launch(i, self)
                else:
                    i(self)

    def log(self, txt):
        pass

    @staticmethod
    def opt(ops):
        if not Runtime.opts:
            return False
        for opt in ops:
            if opt in Runtime.opts:
                return True
        return False

    def parse_cli(self):
        parse(self.prs, " ".join(sys.argv[1:]))
        update(self.opts, self.prs.opts)
        if "mods" in self.prs.sets:
            Cfg.mods = self.prs.sets.mods
        Cfg.console = Runtime.opt("c")
        Cfg.daemon = Runtime.opt("d")
        Cfg.debug = Runtime.opt("z")
        Cfg.systemd = Runtime.opt("s")
        Cfg.verbose = Runtime.opt("v")

    @staticmethod
    def privileges(name=None):
        if os.getuid() != 0:
            return None
        try:
            pwn = pwd.getpwnam(name)
        except (TypeError, KeyError):
            name = getpass.getuser()
            try:
                pwn = pwd.getpwnam(name)
            except (TypeError, KeyError):
                return None
        if name is None:
            try:
                name = getpass.getuser()
            except (TypeError, KeyError):
                pass
        try:
            pwn = pwd.getpwnam(name)
        except (TypeError, KeyError):
            return False
        try:
            os.chown(ObjCfg.wd, pwn.pw_uid, pwn.pw_gid)
        except PermissionError:
            pass
        os.setgroups([])
        os.setgid(pwn.pw_gid)
        os.setuid(pwn.pw_uid)
        os.umask(0o22)
        return True

    @staticmethod
    def root():
        if os.geteuid() != 0:
            return False
        return True

    @staticmethod
    def skel():
        assert ObjCfg.wd
        cdir(ObjCfg.wd + os.sep)
        cdir(os.path.join(ObjCfg.wd, "store", ""))

    @staticmethod
    def wait():
        while 1:
            time.sleep(5.0)
