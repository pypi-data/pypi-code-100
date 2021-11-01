# This file is placed in the Public Domain.

import random
import unittest

from gcd.bus import Bus
from gcd.obj import Object
from gcd.ofn import save
from gcd.run import Runtime, getmain
from gcd.run import Cfg as RunCfg
from gcd.tbl import Table
from gcd.thr import launch

events = []

param = Object()
param.add = ["test@shell", "bart", ""]
param.cfg = ["server=localhost", ""]
param.dne = ["test4", ""]
param.rm = ["reddit", ""]
param.dpl = ["reddit title,summary,link", ""]
param.log = ["test1", ""]
param.flt = ["0", ""]
param.fnd = [
    "cfg",
    "log",
    "rss",
    "log txt==test",
    "cfg server==localhost",
    "rss rss==reddit",
]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["test4", ""]


class Test_Threaded(unittest.TestCase):
    def test_thrs(self):
        thrs = []
        if RunCfg.index:
            nr = Runtime.cfg.index
        else:
            nr = 1
        for x in range(nr):
            thr = launch(exec, name="task%s" % x)
            thrs.append(thr)
        for thr in thrs:
            thr.join()
        consume()


def consume():
    fixed = []
    res = []
    for e in events:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            events.remove(f)
        except ValueError:
            continue
    return res


def exec():
    k = getmain("k")
    c = Bus.first()
    l = list(Table.modnames)
    random.shuffle(l)
    for cmd in l:
        for ex in getattr(param, cmd, [""]):
            e = c.event(cmd + " " + ex)
            k.dispatch(e)
            events.append(e)
