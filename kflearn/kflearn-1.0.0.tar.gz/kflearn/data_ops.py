#!/usr/bin python
# -*- coding: utf-8 -*-
'''
@Author: HornLive
@Time: 10 15, 2021
'''
import logging
import os
import random
import requests
import json

logging.getLogger().setLevel(logging.INFO)


def parse_line(line: str, a=None, b=None) -> str:  # 为用户自定义
    return line


def data_split_parse(raw_dir,
                     train_path=None,
                     valid_path=None, valid_limit=100,
                     test_path=None, test_limit=100,
                     parse_line_func=parse_line, fun_args={},
                     pct=100):
    '''
    数据集切分为训练集、验证集、测试集
    :param raw_dir:未拆分训练集目录
    :param train_path:已拆分训练集
    :param valid_path:已拆分验证集
    :param valid_limit:验证集条数
    :param test_path:已拆分测试集
    :param test_limit:测试集条数
    :param parse_line_func：需自实现-行处理函数(默认不处理)
    :param fun_args:行处理函数额外入参(默认不填)
    :param pct:按 1/pct 进行随机抽取验证集和测试集
    :return:
    '''

    # 遍历原始训练集目录
    file_list = []
    for root, dirs, files in os.walk(raw_dir):
        for file in files:
            file_list.append(os.path.join(root, file))

    train_cnt = 0
    valid_cnt = 0
    test_cnt = 0
    valid_w = open(valid_path, encoding='utf8', mode='w')
    test_w = open(test_path, encoding='utf8', mode='w')
    with open(train_path, encoding='utf8', mode='w') as train_w:
        for file_path in file_list:
            with open(file_path, encoding='utf8') as f:
                for line in f:
                    new_line = parse_line_func(line.strip(), **fun_args)

                    rand = random.randint(0, pct)
                    if rand == 13 and valid_cnt < valid_limit:
                        valid_w.write(new_line + '\n')
                        valid_cnt += 1
                    elif rand == 31 and test_cnt < test_limit:
                        test_w.write(new_line + '\n')
                        test_cnt += 1
                    else:
                        train_w.write(new_line + '\n')
                        train_cnt += 1
                valid_w.flush()
                test_w.close()
    logging.info('Data split over:' + str({'train': train_cnt, 'valid': valid_cnt, 'test': test_cnt}))


def upload(local_file_path) -> str:
    # '''
    # 上传文件到云仓库
    # :param local_file_path: 本地文件路径
    # :param dst_name: 目标文件名
    # :param dst_version: 目标文件版本
    # :return: 返回该文件下载地址
    # '''
    url = "http://dev-predict.amh-group.com/predict-fs/file/upload"
    file_name = os.path.basename(local_file_path)
    logging.info(file_name)

    payload = {}
    files = [
        ('file', (file_name, open(local_file_path, 'rb'), 'application/octet-stream'))
    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    logging.info("####" + response.text)
    return json.loads(response.text)['data']['url']


def download(down_file_url, target_file_path):
    down_res = requests.get(down_file_url)
    with open(target_file_path, "wb") as code:
        code.write(down_res.content)

    logging.info('#### 下载文件：' + target_file_path)
