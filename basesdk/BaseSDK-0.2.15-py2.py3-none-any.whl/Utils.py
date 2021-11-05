import functools
import threading

import requests
from multiprocessing import Pool
import os

class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
            return cls._instance


def makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def download_binary(data):
    _path, _url = data
    response = requests.get(_url)
    with open(_path, 'wb') as handle:
        handle.write(response.content)


# def parallel_download(root_path, urls):
#     global __download_binary
#     # @functools.wraps(parallel_download)
#
#
#     try:
#
#         pool.map(__download_binary, urls)
#     except Exception as e:
#         raise e


def parallel_download_labels(save_path, header, payload, label_urls):
    mk_save_path(save_path)

    # @functools.wraps(parallel_download_labels)
    def __download_json(file):
        _name, _url = file
        response = requests.get(_url, params=payload, headers=header).json()
        with open(os.path.join(save_path, _name), 'w') as handle:
            handle.write(response)

    try:
        _pool = Pool()
        _pool.map(__download_json, label_urls)
    except Exception as e:
        raise e


def mk_save_path(_save_path):
    if not os.path.exists(_save_path):
        os.makedirs(_save_path)
    global save_path
    save_path = _save_path



