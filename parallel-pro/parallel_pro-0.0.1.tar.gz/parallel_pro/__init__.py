from joblib import Parallel, delayed
from joblib import parallel_backend
from multiprocessing import cpu_count
from typing import List, Any


def __get_bins(no_bins: int, data: List) -> List:
    """ this method create same length bins with given data """
    d_len = len(data)
    interval = d_len // no_bins
    data_bins = []
    start_index = 0
    end_index = interval
    for i in range(d_len):
        inter = data[start_index:end_index]
        if len(inter) == 0:
            break
        data_bins.append(inter)
        start_index = end_index
        end_index = end_index + interval
    return data_bins


def run_parallel(list_of_data: List, process_fun: Any, workers=cpu_count(),
                 verbose=True, *args) -> List:
    """
    Parallel Processing for for loops using joblib parallel_backend
    :param list_of_data:
    :param process_fun:
    :param workers:
    :param verbose:
    :param args:
    :return:
    """
    jobs = workers
    if len(list_of_data) <= workers:
        jobs = len(list_of_data)

    if verbose:
        print(f"Parallel Processing Started with {jobs} workers...")

    data_bins = __get_bins(no_bins=jobs, data=list_of_data)
    with parallel_backend('threading', n_jobs=jobs):
        results = Parallel(verbose=verbose)(
            delayed(process_fun)(data_bin, *args) for
            data_bin in data_bins)
    if verbose:
        print(f"Parallel Processing Completed with {jobs} workers...")
    return results
