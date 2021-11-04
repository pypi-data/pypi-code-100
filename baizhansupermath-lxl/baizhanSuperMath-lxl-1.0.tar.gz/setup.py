from distutils.core import setup

setup(
    name="baizhanSuperMath-lxl",    # 对外模块的名字
    version="1.0",  # 版本号
    description="这是第一个对外发布的模块,里面只有数学方法,用于测试",   # 描述
    author="lxl",   # 作者
    author_email="1420524682@qq.com",
    py_modules=["baizhanSuperMath-lxl.demo1","baizhanSuperMath-lxl.demo2"]  # 要发布的模块
)