"""
Parallel
========

Convert a function into parallel run.

"""
import multiprocessing
import os


def parallel(func, np=8):
    """Convert a function to parallel version

    Example:

    .. highlight:: python
    .. code-block:: python

        def mul2(x):
          return x*2

        parallel_mul2 = parallel(mul2)
        parallel_mul2([(i,) for i in range(10)])

    :param func: function
    :param np: number of parallel jobs
    :return: a function takes a list of **lists**.
    """

    def wrapper(iter_list):
        with multiprocessing.Pool(np) as pool:
            return pool.starmap(func, iter_list)

    return wrapper


def parallel_tqdm(func, np=8):
    """Convert a function to parallel version with tqdm progress bar.

    Example:

    .. highlight:: python
    .. code-block:: python

        def mul2(x):
          return x*2

        parallel_mul2 = parallel_tqdm(mul2)
        parallel_mul2([(i,) for i in range(10)])

    :param func: function
    :param np: number of parallel jobs
    :return: a function takes a list of lists.
    """
    from tqdm import tqdm
    from sys import version_info
    if version_info[0] == 3 and version_info[1] > 7:
        from ._utils import _istarmap_38 as _istarmap
    else:
        from ._utils import _istarmap_37 as _istarmap
    multiprocessing.pool.Pool.istarmap = _istarmap

    def wrapper(iter_list):
        with multiprocessing.Pool(np) as pool:
            res = [i for i in tqdm(pool.istarmap(func, iter_list),
                                   total=len(iter_list))]
        return res

    return wrapper


def parallel_bash(scripts, np=8):
    """
    Run bash script line by line in parallel
    Example:

    .. highlight:: python
    .. code-block:: python

        parallel_bash(open("script.sh").readlines())

    :param scripts: list of scripts to run
    :param np: number of parallel jobs
    """
    cmd = [(i.strip(),) for i in scripts]
    call = parallel(os.system, np)
    call(cmd)


def parallel_bash_tqdm(scripts, np=8):
    """
    Run bash script line by line in parallel with tqdm progress bar
    Example:

    .. highlight:: python
    .. code-block:: python

        parallel_bash_tqdm(open("script.sh").readlines())

    :param scripts: list of scritps to run
    :param np: number of parallel jobs
    """
    cmd = [(i,) for i in scripts]
    call = parallel_tqdm(os.system, np)
    call(cmd)
