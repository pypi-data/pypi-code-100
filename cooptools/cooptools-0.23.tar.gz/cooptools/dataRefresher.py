import threading
from typing import Callable, Any, List
import time
import logging

logger = logging.getLogger("cooptools.datarefresher")


class DataRefresher:
    def __init__(self,
                 name: str,
                 refresh_callback: Callable[[], Any],
                 refresh_interval_ms: int,
                 timeout_on_fail_ms: int = None,
                 as_async: bool = False):
        self._name = name
        self._last_refresh = None
        self._refresh_callback = refresh_callback
        self._cached_return = None
        self._start_timeout = None
        self._timeout_on_fail_ms = timeout_on_fail_ms if timeout_on_fail_ms else refresh_interval_ms
        self.refresh_interval_ms = refresh_interval_ms
        self._async = as_async

        # Set initial cache
        self._try_refresh_cache()

        if self._async: self._init_refresh_thread()

    def _init_refresh_thread(self):
        refresh_thread = threading.Thread(target=self._async_thread_loop, daemon=True)
        refresh_thread.start()

    @property
    def in_timeout(self):
        # check if can clear the timeout
        if self._start_timeout and time.perf_counter() - self._start_timeout > self._timeout_on_fail_ms:
            self._start_timeout = None

        return self._start_timeout is not None

    @property
    def latest(self):
        if self._async:
            return self._cached_return
        else:
            return self._check_refresh_latest()

    def refresh(self):
        self._try_refresh_cache()
        return self._cached_return

    def _set_cache(self):
        """ Set cache with value from the refresh callback. Acquires a thread lock before setting cache """
        tic = time.perf_counter()
        return_of_callback = self._refresh_callback()
        with threading.Lock():
            self._cached_return = return_of_callback
            toc = time.perf_counter()
            logger.info(f"cache refreshed for \"{self._name}\" in {round(toc-tic, 3)} sec")

    def _try_refresh_cache(self):
        """ Try the refresh callback. if fail, start the timeout timer """
        try:
            self._set_cache()
            self._last_refresh = time.perf_counter()
        except Exception as e:
            logger.error(e)
            self._start_timeout = time.perf_counter()

    def _check_refresh_latest(self):
        """ Checks the state of the instance and whether or not to refresh"""
        # dont do any refresh during a timeout
        if self.in_timeout:
            pass
        # check if time to refresh cache
        elif self._last_refresh is None or \
                time.perf_counter() - self._last_refresh > self.refresh_interval_ms / 1000:
            self._try_refresh_cache()

        return self._cached_return

    def _async_thread_loop(self):
        while True:
            self._check_refresh_latest()
            time.sleep(0.5)

    @property
    def last_refresh(self):
        return self._last_refresh

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    def takes_some_time():
        time.sleep(2)
        return {"a": time.perf_counter()}

    callback = takes_some_time

    refresh_interval_sec = 5
    df = DataRefresher('key', callback, 5 * 1000, as_async=True)

    while True:
        print(df.latest)
        time.sleep(.5)

