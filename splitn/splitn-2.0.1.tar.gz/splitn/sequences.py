import sys
from typing import Union
from rstr import xeger
from re import compile, Pattern
from loguru import logger

@logger.catch
def random_sequence(regex: Union[str, Pattern]) -> str:
    return xeger(compile(regex))

@logger.catch
def main():
    try:
        print(random_sequence(str(sys.argv[1])))
    except:
        return 1

if __name__ == '__main__':
    sys.exit(main())
