from multiprocessing import Value, Queue

from typing import Union, Callable, Sequence

from .worker import Worker
from .producer import Producer
from .consumer import Consumer



class Warehut:
    """Manager for starting and stopping producers and consumers"""

    workers: list[Worker]
    producer: list[Worker]
    consumers: list[Worker]

    def __init__(self, worker_types: Sequence[type[Worker]]):
        # Initialize consumers and producers from worker classes
        self.consumers = [w() for w in worker_types if issubclass(w, Consumer)]
        self.producers  = [w(self.consumers) for w in worker_types if issubclass(w, Producer)]

        self.workers = self.producers + self.consumers


    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, trace):
        self.stop()


    def start(self):
        """Start all worker processes"""
        for worker in self.workers:
            worker.start(handle_error=self.handle_error)

    def stop(self):
        """Stop all worker processes"""
        for worker in self.workers:
            worker.stop()

    def handle_error(self, worker_class: type[Worker], exception: Exception):
        """Handle exception raised within a worker process.
        Launch a window, write to a log file, etc.
        
        OBS! Although `self` of the `Warehut` object is available,
        not all functionality is, as it is run in a separate process.
        `self.stop()` for shutting down all workers, however, does work.
        So you can end all workers should an individual worker crash.
        """
        self.stop()