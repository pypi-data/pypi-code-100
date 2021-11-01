# coding=utf-8
from setuptools import setup

setup(
    author="renyumeng",  # 作者的名字  也就是你自己的名字
    author_email="235328756@qq.com",  # 作者的邮箱
    description="This is a pacage, writen by renyumeng",  # 一句话概括一下
    url="https://github.com/renyumeng1",  # 你可以把你的home page或者github主页的地址写上
    name="amamiyass",  # 给你的包取一个名字
    license='MIT',
    version="1.0",  # 你的包的版本号
    packages=['amamiyass'],# 这里写的是需要从哪个文件夹下导入python包，目录结构如上面所示，名字必须对上，如果找不到会报错
    install_requires=[],
    exclude_package_date={'': ['.gitignore'], '': ['dist'], '': 'build', '': 'utility.egg.info'},
    # 这是需要排除的文件，也就是只把有用的python文件导入到环境变量中

)
