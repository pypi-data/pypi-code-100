from multiprocessing import cpu_count
from dataclasses import dataclass
from typing import Union, List, Tuple, Any, Iterator

from .pools import WorkersPool, TasksPool

WorkResults = List[Tuple[str, Tuple, Any]]
DispatchedResults = List[Tuple[str, WorkResults]]

@dataclass
class WorkManager:
    """Manage work dispatch using WorkersPool and TasksPool to make multiprocessing/multithreading traitement of given function and args.

    Create a Process pool of workers.
    Dispatch work in chunk to processes
    Processes generate multiple threads based on the workload
    The work is done by the threads generated in a chunked scheme over all processes

    Attributes:
        work_name (str, optional): work name. Defaults to 'task'.
        max_tasks (int, optional): maximun tasks pool size, should never be greather than 399. Defaults to 64.
        max_workers (int, optional): number of cpu to use. Defaults to multiprocessing.cpu_count().
        show_progress (bool, optional): show tqdm progress bar if True. Defaults to False.
        show_debug (bool, optional): show debug msg on start and end or each method if True. Defaults to False.
    """
    work_name: str = "task"
    max_tasks: int = 64
    max_workers: int = cpu_count()
    show_progress: bool = False
    show_debug: bool = False

    def chunks(self, lst: list, n: int) -> Iterator[list]:
        """Yield successive n-sized chunks from lst.

        Args:
            lst (list): list of items to yield chunks from
            n (int): chunk length size

        Yields:
            list: n-sized chunk from lst
        """
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def work(self, work_name: str, work_to_do, work_data: Union[List, int]) -> WorkResults:
        """Dispatch and apply work_to_do accross multiple threads using TasksPool.

        Args:
            work_name (str): work name
            work_to_do (function): function to apply
            work_data (list): list of function args

        Returns:
            list[tuple[str, tuple, Any]]: list of tuples containing task name, function args as tuple, function results
        """
        work_data = [() for _ in range(work_data)] if isinstance(work_data, int) else work_data
        if(isinstance(work_data, list) and len(work_data)):
            if(self.show_debug):
                print(f"[START {__class__.__name__}.work # {self.work_name} | {work_name} - (Tasks: {len(work_data)})]\n")
            work_results = TasksPool(nb_tasks=len(work_data), show_progress=self.show_progress).do(work_name, work_to_do, work_data)
            if(self.show_debug):
                print(f"\n[END {__class__.__name__}.work # {self.work_name} | {work_name} - (Tasks: {len(work_data)})]\n")
            return [
                (f"Task #{i}", work_args, work_results[i])
                for i, work_args in enumerate(work_data)
            ]

    def dispatch(self, work_to_do, work_data: Union[List, int], workload=4) -> DispatchedResults:
        """Dispatch and apply work_to_do accross multiple processes (using WorkersPool on worker) which then dispatch work_to_do accross multiple threads.

        Args:
            work_to_do (function): function to dispatch over workers
            work_data (int or list of tuples): list of function args
            workload (int, optional): chunk length size. Defaults to 4.

        Returns:
            list[tuple[str, list[tuple[str, tuple, Any]]]]: list of tuples containing worker name and chunked work results
        """
        # Handle the case when work_to_do don't need work_data
        work_data = [() for _ in range(work_data)] if isinstance(work_data, int) else work_data
        if(isinstance(work_data, list) and len(work_data)):
            # Adapt given workload size and work_data with max_tasks possible (create tasks only when)
            workload_capacity = min(workload, len(work_data), self.max_tasks)
            chunked_work = [
                (f"Worker #{i} [{(i*workload_capacity)} -> {(i*workload_capacity + len(chunk) - 1)}]", work_to_do, chunk)
                for i, chunk in enumerate(list(self.chunks(work_data, workload_capacity)))
            ]
            if(self.show_debug):
                print(f"[START {__class__.__name__}.dispatch # {self.work_name} - (Tasks: {len(work_data)}, Workload: {workload_capacity})]\n")
            worker_results = WorkersPool(nb_workers=self.max_workers, show_progress=self.show_progress).do(self.work_name, self.work, chunked_work)
            if(self.show_debug):
                print(f"\n[END {__class__.__name__}.dispatch # {self.work_name} - (Workers: {len(chunked_work)}, Workload: {workload_capacity}, Tasks: {len(work_data)})]\n")
            return [
                (f"Worker #{i}", worker_result)
                for i, worker_result in enumerate(worker_results)
            ]


