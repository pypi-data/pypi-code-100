#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
@Author: HornLive
@Time: 11-26,2020
'''
import os
import shutil
import zipfile


def get_dir():
    pwd = os.path.dirname(__file__)
    parent = os.path.dirname(pwd)
    print(parent, pwd)
    return pwd, parent


# 遍历多级目录
def scan_dir(dir):
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


# 遍历当前目录,并递归
def scan_all(path):
    sub_paths = os.listdir(path)  # 列出指定路径下的所有目录和文件
    for sub in sub_paths:
        com_path = os.path.join(path, sub)
        print(com_path)
        if os.path.isdir(com_path):
            scan_all(com_path)  # 如果该路径是目录，则调用自身方法


def create_dir_and_clear(path: str):
    if not os.path.exists(dir):
        os.mkdir(dir)
    else:
        shutil.rmtree(dir)
        os.mkdir(dir)


def create_dir_not_clear(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


def remove_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
        print("remove %s success." % dir)


# [慢]写大文件1 10M/s
def write_10M():  # [with外for]
    for i in range(10000000):
        with open("tmp_data/write.txt", encoding='utf8', mode='a') as w:
            w.write("qqqqqqqqqqqqqqqqqqqqqqqqqqq\n")


def zip(local_path, target_zip_path):
    '''
    压缩文件
    :param local_path:本地路径(文件或文件夹)
    :param target_zip:目标.zip文件(需要解压到本地)
    :return:
    '''
    f = zipfile.ZipFile(target_zip_path, 'w', zipfile.ZIP_DEFLATED)
    f.write(local_path)
    f.close()


def un_zip(source_zip_path, target_dir):
    """unzip zip file"""
    os.makedirs(target_dir, exist_ok=True)

    zf = zipfile.ZipFile(source_zip_path)
    for file in zf.namelist():
        zf.extract(file, target_dir)
    zf.close()


# [快]写大文件方法2 <不占内存><固体硬盘>140M/s（mode=a）190M/s(mode=w)
def write_140M():  # [with内for]
    with open("data/write333.txt", encoding='utf8', mode='w') as w:
        for i in range(10000000):
            w.write("qqqqqqqqqqqqqqqqqqqqqqqqqqq\n")
            # w.flush()#会慢


# 不占内存130M/s<机械硬盘>
def write_130M():  # [无with]
    w = open("f:/write444.txt", encoding='utf8', mode='w')
    for i in range(10000000):
        w.write("qqqqqqqqqqqqqqqqqqqqqqqqqqq\n")
        if (i % 1000 == 0):
            print(i)
            w.flush()


# 读写大文件3 110M/s
def write_110M():  # [双with内for]
    with open("tmp_data/write222.txt", encoding='utf8', mode='a') as w:
        with open('tmp_data/write.txt', encoding='utf8') as f:
            for line in f:
                w.write(line)


# with语句打开和关闭文件，包括抛出一个内部块异常。
# for line in f文件对象f视为一个迭代器，会自动的采用缓冲IO和内存管理，所以你不必担心大文件
# "rb"时的效率是"r"的6倍，二进制读取依然是最快的模式
# 100w行全遍历2.9秒
def read_text():
    with open("data/input2_scalaseq.dat", mode='rb') as f:  # encoding='utf8'
        for line in f:
            print(line)


def test_file():
    shutil.move('aaa/bbb', 'aaa/ccc')
    shutil.make_archive('aaa/bbb', 'zip', 'kflearn')
    shutil.unpack_archive('aaa/bbb.zip', 'ccc', 'zip')


if __name__ == '__main__':
    # scan_all('/opt/files/mxmodels')
    # un_zip('data/test.zip', 'data')
    # pass
    # move('aaa','bbb')
    # shutil.move('bbb/aaa.txt', 'aaa')
    pass

    print(os.path.dirname(__file__))
    print(os.getcwd())
