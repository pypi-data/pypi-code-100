from re import compile, match
from os import scandir
import os, stat
from datetime import datetime
from operator import attrgetter
from pathlib import Path
from functools import partial


def files(path):
    with scandir(path) as ls:
        for entry in sorted(ls, key=attrgetter('path')):
            if entry.is_dir(follow_symlinks=False):
                yield from files(entry.path)
            elif entry.is_file():
                yield Path(entry)


def find(path, name):
    match = compile(name).search
    for path in files(path):
        if match(str(path)):
            yield path


def grep(path, rex):
    rmatch = partial(match, compile(rex))
    with open(path) as inp:
        for found in filter(None, map(rmatch, inp)):
            yield found.groups()


class FileStat:
    def __init__(self, path):
        self.path = path if isinstance(path, Path) else Path(path)
        self.stat = os.stat(str(self.path))

    @property
    def mtime(self):
        mtime = self.stat[stat.ST_MTIME]
        return datetime.fromtimestamp(mtime)

    @property
    def age(self):
        delta = datetime.now() - self.mtime
        return delta.days
