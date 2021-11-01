from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from tqdm.auto import tqdm
import multiprocessing as mp
import itertools
from collections import defaultdict


def unzip(it, default=([], [])):
    l = list(it)
    if len(l) == 0:
        return default

    return tuple([list(x) for x in zip(*l)])


def par_for(f, l, process=False, workers=None, progress=True, **kwargs):
    Pool = ProcessPoolExecutor if process else ThreadPoolExecutor
    with Pool(max_workers=mp.
              cpu_count() if workers is None else workers) as executor:
        if progress:
            return list(tqdm(executor.map(f, l, **kwargs), total=len(l), smoothing=0.05))
        else:
            return list(executor.map(f, l, **kwargs))


def par_filter(f, l, **kwargs):
    return [x for x, b in zip(l, par_for(f, l, **kwargs)) if b]


# https://mathieularose.com/how-not-to-flatten-a-list-of-lists-in-python/
def flatten(l):
    return list(itertools.chain.from_iterable(l))


def collect(l, kfn):
    d = defaultdict(list)
    for x in l:
        d[kfn(x)].append(x)
    return dict(d)


def batch(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
