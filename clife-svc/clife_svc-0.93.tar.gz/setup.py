from setuptools import setup

setup(
    name='clife_svc',   # 需要打包的名字,即本模块要发布的名字
    version='0.93',     # 版本
    description='A module for service',   # 简要描述
    packages=['clife_svc', 'clife_svc.errors', 'clife_svc.libs'],
    install_requires=[
        'loguru',
        'aiohttp',
        'uvicorn',
        'requests',
        'cos_python_sdk_v5',
        'aiofiles',
        'fastapi'
    ],
    author='andy.hu',         # 作者名
    author_email='hlp0@163.com',       # 作者邮件
    url='',       # 项目地址,一般是代码托管的网站
    # requires=['requests','urllib3'], # 依赖包,如果没有,可以不要
    license='MIT'
)