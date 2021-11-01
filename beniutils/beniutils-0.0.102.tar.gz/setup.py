version = "0.0.102"
install_requires = [
    "aiohttp",
    "aiofiles",
    "python-dateutil",
    "twine",
    "pyinstaller",
    "openpyxl",
    "pytest",
    "pytest-asyncio",
    "pyecharts",
    # -------- 非依赖库，但常用的库
    "ipython",
    "autopep8",
    # -------- 准备放弃使用
    "selenium-wire", # selenium扩展版本
    "xlrd3",
    "defusedxml", # xlrd3用到    
]

from setuptools import setup, find_packages

setup(
    name = "beniutils",
    version = version,
    keywords="beni",
    description = "utils library for Beni",
    license = "MIT License",
    url = "https://pypi.org/project/beniutils/",
    author = "Beni",
    author_email = "benimang@126.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = install_requires,
    entry_points={
        "console_scripts": ["beniutils=beniutils.cmd:main"],
    },
)