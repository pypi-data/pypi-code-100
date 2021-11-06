import cProfile
import logging
import time
import functools


logger = logging.getLogger(__name__)


def time_it(f):
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f.__name__, 'took', end - start, 's')
        return result
    return f_timer


class time_with():
    def __init__(self, name=''):
        self.name = name
        self.start = time.time()

    @property
    def elapsed(self):
        return time.time() - self.start

    def checkpoint(self, name=''):
        print('{timer} {checkpoint} took {elapsed} s'.format(
            timer=self.name,
            checkpoint=name,
            elapsed=self.elapsed,
        ).strip())

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.checkpoint('finished')
        pass


def c_profile(filename="", keys=(), xls_filename="", xls_sheet="Sheet1"):
    def inner(func):
        @functools.wraps(func)
        def profiled_func(*args, **kwargs):
            profile = cProfile.Profile()
            try:
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                return result
            finally:
                if not filename:
                    profile.print_stats()
                else:
                    profile.dump_stats(filename)
        return profiled_func
    return inner


try:
    from line_profiler import LineProfiler

    def line_profile(follow=[], filename="", keys=(), xls_filename="", xls_sheet="Sheet1"):
        def inner(func):
            @functools.wraps(func)
            def profiled_func(*args, **kwargs):
                profile = LineProfiler()
                print("Starting Line Profiler...")
                try:
                    profile.add_function(func)
                    for f in follow:
                        profile.add_function(f)
                        profile.enable_by_count()
                    return func(*args, **kwargs)
                finally:
                    if not filename:
                        profile.print_stats()
                    else:
                        profile.dump_stats(filename)
            return profiled_func
        return inner

except ImportError:
    def line_profile(follow=[], filename="lineprofile.pstat", keys=(), xls_filename="", xls_sheet="Sheet1"):
        "Helpful if you accidentally leave in production!"
        def inner(func):
            def nothing(*args, **kwargs):
                return func(*args, **kwargs)
            return nothing
        return inner


def _get_number():
    for x in range(5000000):
        yield x


@time_it
def _time_it_function():
    for x in _get_number():
        i = x ^ x ^ x
    return 'some result!'


def _time_with_function():
    for x in _get_number():
        i = x ^ x ^ x
    return 'some result!'


@c_profile(filename="profile2.pstat")
def _cprofile_function():
    for x in _get_number():
        i = x ^ x ^ x
    return 'some result!'


@line_profile(follow=[_get_number])
def _lineprofile_function():
    for x in _get_number():
        i = x ^ x ^ x
    return 'some result!'


if __name__ == "__main__":
    print("time_it()")
    result = _time_it_function()

    print("time_with")
    with time_with('fancy thing') as timer:
        _time_with_function()
        timer.checkpoint('done with something')
        _time_with_function()
        _time_with_function()
        timer.checkpoint('done with something else')

    print("c_profile")
    result = _cprofile_function()

    print("line_profile")
    result = _lineprofile_function()

