import os.path as osp

from handypy.parallel import *

test_script = osp.dirname(osp.abspath(__file__)) + "/echo.sh"


def _mul2(x):
    return x * 2


def test_parallel():
    mul2p = parallel(_mul2)
    inp = [(i,) for i in range(100)]
    res = mul2p(inp)
    for i, j in zip(inp, res):
        assert i[0] * 2 == j, i

    mul2p = parallel_tqdm(_mul2)
    res = mul2p(inp)
    for i, j in zip(inp, res):
        assert i[0] * 2 == j, i

    parallel_bash(open(test_script).readlines())
    parallel_bash_tqdm(open(test_script).readlines())
