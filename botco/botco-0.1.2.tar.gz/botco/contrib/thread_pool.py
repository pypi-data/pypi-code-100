import concurrent.futures


class ThreadPoolExecutor:
    def __init__(self, max_workers: int = None):
        if not max_workers:
            max_workers = 5
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

    def add_task(self, callback, *args, **kwargs):
        task = self.executor.submit(callback, *args, **kwargs)
        return task

    def close(self):
        self.executor.shutdown(cancel_futures=True)
