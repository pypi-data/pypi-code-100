import numpy as np
from foldedleastsquares import DefaultTransitTemplateGenerator


class LcbuilderHelper:
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def calculate_period_grid(time, min_period, max_period, oversampling, star_info, transits_min_count):
        dif = time[1:] - time[:-1]
        jumps = np.where(dif > 1)[0]
        jumps = np.append(jumps, len(time))
        previous_jump_index = 0
        time_span_all_sectors = 0
        for jumpIndex in jumps:
            time_chunk = time[previous_jump_index + 1:jumpIndex]  # ignoring first measurement as could be the last from the previous chunk
            time_span_all_sectors = time_span_all_sectors + (time_chunk[-1] - time_chunk[0])
            previous_jump_index = jumpIndex
        return DefaultTransitTemplateGenerator() \
            .period_grid(star_info.radius, star_info.mass, time[-1] - time[0], min_period,
                         max_period, oversampling, transits_min_count, time_span_all_sectors)
