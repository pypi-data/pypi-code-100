import urllib.request
import urllib.error
import pathlib
import warnings
import os
import time


def download(url, save_path, sleep=1):
    """
    urlからダウンロードする。save_pathが存在するなら何もしない。
    Args:
        url (str): url
        save_path (str): save path
        sleep (int): 待機時間(秒)
    Returns:
        int: 成功なら1,urlがnotfoundまたはファイルが既に存在するなら0
    """
    save_path = pathlib.Path(save_path)
    if save_path.exists():
        return 0
    time.sleep(sleep)
    os.makedirs(save_path.parent, exist_ok=True)
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as res:
            save_path.write_bytes(res.read())
        return 1
    except urllib.error.HTTPError as e:
        warnings.warn(f"{e.code}: {e.reason}")
        warnings.warn(f"url: {url}")
        return 0
