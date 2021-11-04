import sys
import os
import time


old_print = print
current_milli_time = lambda: int(round(time.time() * 1000))


def debug_print(*p):
    current_frame = sys._getframe(1)

    milli_tim_str = "%03d " % (current_milli_time() % 1000)
    code_info = " %s(%s:%s)" % (current_frame.f_code.co_name, os.path.basename(current_frame.f_code.co_filename), current_frame.f_lineno)
    old_print(time.strftime("%Y-%m-%d %H:%M:%S.")  + milli_tim_str + code_info, *p)



