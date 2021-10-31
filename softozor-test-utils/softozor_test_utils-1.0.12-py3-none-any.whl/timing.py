import time


def wait_until(predicate, timeout_in_sec=5, period_in_sec=0.1):
    timeout = time.time() + timeout_in_sec
    while True:
        if predicate():
            return
        if time.time() > timeout:
            raise TimeoutError(
                f'wait_until expired after <{timeout_in_sec}> seconds')
        time.sleep(period_in_sec)


def fail_after_timeout(predicate, timeout_in_sec=5, period_in_sec=0.1):
    try:
        wait_until(predicate, timeout_in_sec, period_in_sec)
        return True
    except TimeoutError:
        return False
