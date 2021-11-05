import numpy as np
import re

def get_Several_MinMax_Array(np_arr, several):
    """
    获取numpy数值中最大或最小的几个数
    :param np_arr:  numpy数组
    :param several: 最大或最小的个数（负数代表求最大，正数代表求最小）
    :return:
        several_min_or_max: 结果数组
    """
    np_arr = np.array(np_arr)
    if several > 0:
        index_pos = np.argpartition(np_arr, several)[:several]
    else:
        index_pos = np.argpartition(np_arr, several)[several:]
    several_min_or_max = np_arr[index_pos]
    return index_pos, several_min_or_max


def find_longest_start_end(arr):
    substr = max(re.findall('1+', str(arr)))
    obj = re.search(substr, str(arr))
    return obj.start(), obj.end()


def get_longest_part(signal):
    if len(signal) == 0:
        return 0, 0

    signal = (signal != 0).astype('int8')
    str_signal = str(signal.tolist()).replace(', ', '')[1:-1]
    start, end = find_longest_start_end(str_signal)

    return start, end