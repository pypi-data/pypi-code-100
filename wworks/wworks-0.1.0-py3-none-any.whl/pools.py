from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count
from dataclasses import dataclass
from typing import Iterable

from tqdm.auto import trange


@dataclass
class TasksPool:
    """Dispatch function using ThreadPoolExecutor (multithreading).

    Wrapper arround concurrent.futures.ThreadPoolExecutor used to dispatch work_to_do over its work_data.

    Attributes:
        progress_cols (str, optional): progress bar columns. Defaults to 100.
        progress_color (str, optional): progress bar color if show_progress is enabled. Defaults to '#4052B5'.
        nb_tasks (int, optional): maximun tasks pool size, should never be greather than 399. Defaults to 64.
        show_progress (bool, optional): show tqdm progress bar if True. Defaults to False.
    """
    progress_cols: int = 100
    progress_color: str = "#4052B5" # light blue
    nb_tasks: int = 64
    show_progress: bool = False

    def do(self, work_name: str, work_to_do, work_data: list) -> list:
        """Apply work_to_do accross multiple threads using ThreadPoolExecutor.

        Args:
            work_name (str): work name
            work_to_do (function): function to apply
            work_data (list): list of function args

        Returns:
            list: list of function returns
        """
        work_data = [() for _ in range(work_data)] if isinstance(work_data, int) else work_data
        if(isinstance(work_data, list) and len(work_data)):
            thread_work_results = {}
            with ThreadPoolExecutor(max_workers=self.nb_tasks) as pool_exec:
                with trange(len(work_data), desc=work_name, ncols=self.progress_cols, colour=self.progress_color, disable=not self.show_progress) as progress_bar:
                    # Map futures with ids to return results in submited order
                    thread_work_results = dict(
                        (id(future), future)
                        for future in [
                            pool_exec.submit(work_to_do, *args)
                            if isinstance(args, Iterable) else
                            pool_exec.submit(work_to_do, args)
                            for args in work_data
                        ]
                    )

                    for future in as_completed(list(thread_work_results.values())):
                        if(self.show_progress):
                            progress_bar.clear()
                            progress_bar.update()
                        try:
                            thread_work_results[id(future)] = future.result()
                        except Exception as err:
                            print(err)
                        if(self.show_progress):
                            progress_bar.refresh()
                pool_exec.shutdown(wait=True)
            return list(thread_work_results.values())


@dataclass
class WorkersPool:
    """Dispatch function using ProcessPoolExecutor (multiprocessing).

    Wrapper arround concurrent.futures.ProcessPoolExecutor used to dispatch work_to_do over its work_data.

    Attributes:
        progress_cols (str, optional): progress bar columns. Defaults to 100.
        progress_color (str, optional): progress bar color if show_progress is enabled. Defaults to '#00f6ff'.
        nb_workers (int, optional): number of cpu to use. Defaults to multiprocessing.cpu_count().
        show_progress (bool, optional): show tqdm progress bar if True. Defaults to False.
    """
    progress_cols: int = 100
    progress_color: str = "#00f6ff" # light cyan
    nb_workers: int = cpu_count()
    show_progress: bool = False

    def do(self, work_name: str, work_to_do, work_data: list) -> list:
        """Apply work_to_do accross multiple processes using ProcessPoolExecutor.

        Args:
            work_name (str): work name
            work_to_do (function): function to apply
            work_data (list): list of function args

        Returns:
            list: list of function returns
        """
        work_data = [() for _ in range(work_data)] if isinstance(work_data, int) else work_data
        if(isinstance(work_data, list) and len(work_data)):
            process_work_results = {}
            with ProcessPoolExecutor(max_workers=self.nb_workers) as pool_exec:
                with trange(len(work_data), desc=work_name, ncols=self.progress_cols, colour=self.progress_color, disable=not self.show_progress) as progress_bar:
                    # Map futures with ids to return results in submited order
                    process_work_results = dict(
                        (id(future), future)
                        for future in [
                            pool_exec.submit(work_to_do, *args)
                            if isinstance(args, Iterable) else
                            pool_exec.submit(work_to_do, args)
                            for args in work_data
                        ]
                    )
                    
                    for future in as_completed(list(process_work_results.values())):
                        if(self.show_progress):
                            progress_bar.clear()
                            progress_bar.update()
                        try:
                            process_work_results[id(future)] = future.result()
                        except Exception as err:
                            print(err)
                        if(self.show_progress):
                            progress_bar.refresh()
                pool_exec.shutdown(wait=True)
            return list(process_work_results.values())
