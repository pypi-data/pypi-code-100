from pathlib import Path
from os import makedirs

from pybrary.files import (
    files,
    find,
    grep,
    FileStat,
)


dest = '/tmp/test'

def init():
    dest_a = f'{dest}/aaa'
    dest_b = f'{dest}/bbb'
    for dst in (dest_a, dest_b):
        makedirs(dst, exist_ok=True)
        for t in 'abc':
            with open(f'{dst}/test_{t}', 'w') as out:
                out.write('abc')
        for tt in 'toto titi tata'.split():
            with open(f'{dst}/{tt}', 'w') as out:
                out.write(tt)


def test_n_files():
    init()

    expected = [
        f'{dest}/aaa/tata',
        f'{dest}/aaa/test_a',
        f'{dest}/aaa/test_b',
        f'{dest}/aaa/test_c',
        f'{dest}/aaa/titi',
        f'{dest}/aaa/toto',
        f'{dest}/bbb/tata',
        f'{dest}/bbb/test_a',
        f'{dest}/bbb/test_b',
        f'{dest}/bbb/test_c',
        f'{dest}/bbb/titi',
        f'{dest}/bbb/toto',
    ]

    found = []
    for f in files(dest):
        assert isinstance(f, Path), f'{type(f)} : {f}'
        assert f.is_file()
        found.append(str(f))

    assert found == expected


def test_n_find():
    init()

    expected = [
        f'{dest}/aaa/tata',
        f'{dest}/aaa/titi',
        f'{dest}/aaa/toto',
        f'{dest}/bbb/tata',
        f'{dest}/bbb/titi',
        f'{dest}/bbb/toto',
    ]

    found = []
    for f in find(dest, r't.t.'):
        found.append(str(f))

    assert found == expected


def test_n_grep():
    init()

    for f in files(dest):
        for g in grep(f, '(a.c)'):
            assert g[0] == 'abc'

    for f in files(dest):
        for g in grep(f, 't(.)t(.)'):
            assert g[0] == g[1]
            assert f't{g[0]}t{g[1]}' in str(f)


def test_n_age():
    path = '/tmp/tmp'
    with open(path, 'w'): pass
    age = FileStat(path).age
    assert age==0


if __name__=='__main__': test_n_age()
