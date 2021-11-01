import os
import sys
import time

PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)), "src")
sys.path.append(PATH)
print(PATH)

from winhye_common.winhye_logger import logging as logging


def log_test():
    logger = logging.getLogger()
    for i in range(10000):
        logger.info("1111111111111111")
        time.sleep(1)


def log_test2():
    logger = logging.getLogger()
    logger.report("123456")


if __name__ == '__main__':
    log_test2()
