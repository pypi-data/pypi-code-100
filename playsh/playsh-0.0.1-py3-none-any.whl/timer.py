from timeit import default_timer as timer


class Timer:
    def __init__(self) -> None:
        self.prev_time: float = timer()
        self.elapsed_seconds: float = 0.0
        self.total_elapsed_seconds: float = 0.0

    def tick(self) -> None:
        current_time = timer()
        self.elapsed_seconds = current_time - self.prev_time
        self.total_elapsed_seconds = self.total_elapsed_seconds + self.elapsed_seconds
        self.prev_time = current_time

    def seconds_since_tick(self) -> float:
        return timer() - self.prev_time
