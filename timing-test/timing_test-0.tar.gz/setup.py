# coding: utf-8

from setuptools import setup

setup(
    name='timing_test', # 项目的名称,pip3 install get-time
    version='0', # 项目版本
    author='sherrryy', # 项目作者
    author_email='yingshiyu519@163.com', # 作者email
    url='https://github.com/sherrrrryy/get_time_tryy', # 项目代码仓库
    description='获取任意时间/获取当前的时间戳/时间转时间戳/时间戳转时间', # 项目描述
    packages=['timing_test'], # 包名
    install_requires=[],
    entry_points={
        'console_scripts': [
            'get_time=get_time:get_time', # 使用者使用get_time时,就睡到get_time项目下的__init__.py下执行get_time函数
            'get_timestamp=get_time:get_timestamp',
            'timestamp_to_str=get_time:timestamp_to_str',
            'str_to_timestamp=get_time:str_to_timestamp',
        ]
    } # 重点
)