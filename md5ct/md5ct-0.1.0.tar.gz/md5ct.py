import os
import sys
import logging
from pathlib import Path
import time
from pypinyin import pinyin, lazy_pinyin, Style
import argparse


class MyAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, ' '.join(values))


__VERSION__ = '0.1.0'

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

TIME = lambda: int(time.time() * 1000)

file_extensions = '.DS_Store', '.ini'


def get_parser():
    parser = argparse.ArgumentParser(
        description='批量修改文件md5',
    )

    parser.add_argument(
        'path',
        metavar='PATH',
        help='文件或者文件夹路径',
        nargs='+',
        action=MyAction
    )

    parser.add_argument(
        '-tp', '--topinyin', action='store_true',
        help='是否将文件名转为拼音'
    )
    parser.add_argument('-v', '--version',
                        action='version', version=__VERSION__, help='显示当前版本号')

    return parser


def checkIsNotIncludeFile(file):
    for extension in file_extensions:
        if extension in file:
            return False
    else:
        return True


def fileAppend(filename):
    temp = open(filename, 'a')

    temp.write(" ")

    temp.close()
    print(filename + " ---> 处理完成")


def changeMd5(path, topinyin):
    if Path(path).exists():

        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):

                for file in files:
                    filename = os.path.join(root, file)
                    fileAppend(filename)
                    if checkIsNotIncludeFile(file) and topinyin:
                        os.renames(filename, "".join(lazy_pinyin(filename)))
                else:
                    for directory in dirs:
                        changeMd5(root + "/" + directory,topinyin)
        else:
            fileAppend(path)

    else:
        if path is not None:
            logging.error('路径不存在:' + path)
        else:
            logging.error('请出入路径:')


def cli():
    args = vars(get_parser().parse_args())
    path = args.get('path', None)
    topinyin = args.get('topinyin', False)
    begin = TIME()
    changeMd5(path, topinyin)
    print("用时：" + str(TIME() - begin) + '毫秒')


if __name__ == '__main__':
    cli()
