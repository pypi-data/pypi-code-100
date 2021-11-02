'''
Ku
==

Provides
  Each kind of function I collect.

===================================

'''
# Filename: ku.py
import pip
import sys
import os
import socket
import uuid

from datetime import datetime
import requests

import urllib
import time

from requests.models import Response
from functools import wraps


def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):

        print(
            f"\033[34m函数\033[0m\033[33m{func.__name__}\033[0m\033[34m已被调用\033[0m")


@logit
def print_hello(name: str):
    """
    Greets the user by name
        Parameters:
                name (str): The name of the user
        Returns:
                str: The greeting
        """
    print('hello , ' + name)


# def speak(words: str, speed: int):
#     '''
#     Speak words...
#         朗读文本。
#     '''
#     engine = pyttsx3.init()
#     rate = engine.getProperty('rate')

    # engine.setProperty('rate', rate + speed)
    # engine.say(words)
    # engine.runAndWait()

@logit
def time():
    '''
    Return current_date...
        返回当前时间。
    '''
    current_date = datetime.now()
    print('现在时间为:' + str(current_date)[0:-10] + '\n')
    return current_date

# speak('hello, are u ok.')


@logit
def judge(login, pas):  # 判断是否重复
    sin = 1  # 判断标志
    s = 0
    t = 0
    f = open("date.txt", "r+")
    # print(sin)
    for line in f:

        accout_id = line.find('用户名为:')
        password_id = line.find('密码为:')
        # final_id = line.find('吧')
        # print(accout_id,password_id)
        # if accout_id != -1:
        accout = line[5:password_id]
        password = line[password_id + 4:-1]
        # print(accout,login)
        # print(password,pas)
        if login == accout and pas == password:
            # print('密码正确')
            # return 1
            t = 1
            quit

    # print(t)
    if t == 1:
        print('密码正确')
        return 1
    else:
        print('密码错误')
        return 0


@logit
def rejudge(login):  # 判断是否重复
    sin = 1  # 判断标志
    s = 0
    t = 0
    f = open("date.txt", "r+")
    # print(sin)
    for line in f:
        accout_id = line.find('用户名为:')
        password_id = line.find('密码为:')
        # final_id = line.find('吧')
        # print(final_id)
        if accout_id != -1:
            # name = line[5:-1]
            name = line[5:password_id]
            s += 1
            # print(line)
            if(login == name):
                t = s
                sin = 0
                # print(sin)
        # print(sin)
    f.close()
    # print(s,t)
    if sin == 0:
        return t
    else:
        return 0


@logit
def regist(login):
    f = open("date.txt", "a+")
    name = f.write('\n用户名为:' + login)
    psd = f.write('密码为:' + input('请输入密码：') + '\n')
    f.close()
    print('恭喜你，用户保存成功。')


@logit
def get_mac_address():
    '''
    Return your mac address
    '''
    m = uuid.UUID(int=uuid.getnode()).hex[-12:]
    mac = ":".join([m[e:e + 2] for e in range(0, 11, 2)])
    # print(c)
    return mac


@logit
def get_host_info():
    # myname = socket.getfqdn(socket.gethostname())
    '''
    获取本机局域网ip

    '''
    myaddr = socket.gethostbyname(socket.gethostname())
    # print(myname)
    return myaddr


@logit
def download(url, file_path):
    '''
    指定url和文件路径，不中断下载。
    '''
    # 第一次请求是为了得到文件总大小
    r1 = requests.get(url, stream=True, verify=False)
    total_size = int(r1.headers['Content-Length'])

    # 这重要了，先看看本地文件下载了多少
    if os.path.exists(file_path):
        temp_size = os.path.getsize(file_path)  # 本地已经下载的文件大小
    else:
        temp_size = 0
    # 显示一下下载了多少
    if temp_size > total_size:
        print('当前文件比目标文件要大，下载失败！\n是否删除本地文件，重新下载？(1.是  2.否)\n')
        if input() == '1':
            os.remove(file_path)
            temp_size = 0
        else:
            return

    print(str(temp_size) + '/' + str(total_size))

    # 核心部分，这个是请求下载时，从本地文件已经下载过的后面下载
    headers = {'Range': 'bytes=%d-' % temp_size}
    # 重新请求网址，加入新的请求头的
    r = requests.get(url, stream=True, verify=False, headers=headers)

    # 下面写入文件也要注意，看到"ab"了吗？
    # "ab"表示追加形式写入文件
    with open(file_path, "ab") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()

                ###这是下载实现进度显示####
                done = int(50 * temp_size / total_size)
                sys.stdout.write("\r[%s%s] %d%%" % (
                    '█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                sys.stdout.flush()
    print()  # 避免上面\r 回车符


@logit
def api_get(url):
    '''
     get 方式获得url或api内容
        Return : res = s.get(url)
    '''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    s = requests.session()
    # please
    res = s.get(url, headers=headers)
    return res


@logit
def api_post(url, data):
    '''
     post 方式获得url或api内容
        Return : res = s.post(url,data)
    '''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    s = requests.session()
    # please
    res = s.post(url=url, data=data, headers=headers)
    return res


@logit
def process_display(temp_size, total_size):
    '''
    进度展示
    '''
    done = int(100 * temp_size / total_size)
    sys.stdout.write("\r[%s%s] %d %%" % (
        '█' * done, ' ' * (100 - done), 100 * temp_size / total_size))
    sys.stdout.flush()


@logit
def insert_point1():
    rev = requests.get("http://selfaaa.whut.edu.cn/", timeout=2)

    print(rev)
    # print(rev)
    jsontxt = rev.text
    # print(jsontxt)
    title = jsontxt.find('code-image" src="')
    text = jsontxt[title + len('code-image" src="')                   :(jsontxt.find('alt=""><') - 2)]
    # print(text)
    # print(title)
    text = 'http://selfaaa.whut.edu.cn/' + text
    print(text)
    return text


if __name__ == '__main__':
    # print(sys.path)
    # print(url_get('https://www.baidu.com/').text)
    # download(insert_point1(), '1233.jpg')
    # speak('焦继丰牛逼')
    print(pip.__version__)
