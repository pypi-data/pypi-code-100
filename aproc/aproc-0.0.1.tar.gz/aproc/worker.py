import multiprocessing
from inspect import getsource


def worker_function_one_way(queue):
    while True:
        status, functext, func_args = queue.get(block=True, timeout=None)
        if status:
            scope = {}
            exec(functext, scope)
            scope["func"](func_args)
        else:
            break


def worker_function_multi_way(queue_in, queue_out):
    while True:
        status, functext, func_args = queue_in.get(block=True, timeout=None)
        if status:
            scope = {}
            exec(functext, scope)
            queue_out.put(scope["func"](func_args))
        else:
            break


class Pool:
    def __init__(self, processes, initializer, bidirectional=False):
        self._queue_in = multiprocessing.Queue()
        self._processes = processes
        self._initializer = initializer
        if bidirectional:
            self._queue_out = multiprocessing.Queue()
            self._pool = multiprocessing.Pool(
                processes=self._processes,
                initializer=worker_function_multi_way,
                initargs=(
                    self._queue_in,
                    self._queue_out,
                ),
            )
        else:
            self._queue_out = None
            self._pool = multiprocessing.Pool(
                processes=self._processes,
                initializer=worker_function_one_way,
                initargs=(self._queue_in,),
            )

    @property
    def function(self):
        return self._initializer

    @function.setter
    def function(self, initializer):
        self._initializer = initializer

    def get(self, block=True, timeout=None):
        if self._queue_out is not None:
            return self._queue_out.get(block=block, timeout=timeout)
        else:
            raise ValueError(
                "Enable bidirectional communication using Worker(bidirectional=True)."
            )

    def put(self, obj, block=True, timeout=None):
        self._queue_in.put(
            obj=[True, self._make_functext(self._initializer), obj],
            block=block,
            timeout=timeout,
        )

    @staticmethod
    def _make_functext(func):
        ft = getsource(func)
        ft = ft.replace(func.__name__, "func")
        return ft

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for i in range(self._processes):
            self._queue_in.put([False, None, None])
        self._pool.close()
        self._pool.join()
        self._pool.terminate()
