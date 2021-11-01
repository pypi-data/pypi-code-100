from pathlib import Path

import numpy as np
import pytest

import fast_overlap

ims = np.load(str(Path(__file__).parent / "test-ims.npy"))
expected = np.load(str(Path(__file__).parent / "expected-overlap.npy"))
shape = (int(np.max(ims[0]) + 1), int(np.max(ims[1]) + 1))


# test a few different types but not all
@pytest.mark.parametrize("type", [np.uint16, np.uint64, np.int32, np.int64])
def test_overlap(type):
    out = fast_overlap.overlap(ims[0].astype(type), ims[1].astype(type), shape)
    assert np.all(out == expected)


def test_parallel_overlap():
    out = fast_overlap.overlap_parallel(
        ims[0].astype(np.int32), ims[1].astype(np.int32), shape
    )
    assert np.all(out == expected)
