import time


class FPS:
    def __init__(
        self, fps: any, smooth_fix: bool = False, no_limit: bool = False
    ) -> None:
        super(FPS, self).__init__()
        self.fps = float(fps)
        self.frame_rate = 1 / fps
        self.frame_rate_big = 1000 / fps
        self.smooth_fix = smooth_fix
        self.no_limit = no_limit
        self.last_tick = time.time()
        self.delta = round(1000 / fps)
        self.ideal_delta = round(1000 / fps)
        self.round_count = 2
        self.round_num = 10 ** self.round_count

    def try_tick(self) -> bool:
        now = time.time()
        if self.no_limit or now - self.last_tick >= self.frame_rate:
            self.delta = round((now - self.last_tick) * 1000) if not self.smooth_fix else self.frame_rate_big
            self.last_tick = now
            return True
        return False

    def get_fps(self) -> float:
        try:
            return 1000 / self.delta
        except ZeroDivisionError:
            return self.fps

    def get_int_fps(self) -> int:
        return round(self.get_fps())

    def set_round_num(self, round_num: int = 2) -> None:
        self.round_count = round_num
        self.round_num = 10 ** round_num

    def round_fps(self) -> str:
        fps_ = self.get_fps()
        return str(round(fps_ * self.round_num) / self.round_num)[:len((str(fps_))) + self.round_count + 1]
