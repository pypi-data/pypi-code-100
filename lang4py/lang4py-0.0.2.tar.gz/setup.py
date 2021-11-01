# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from setuptools import setup, find_packages

_author = "angel"
_author_email = "376355670@qq.com"
_description = ""
_py_version = ">=3.7"

_version = "0.0.2"
requires = []


def get_long_description(filename: str):
    long_description = ""
    with open(filename, mode="r", encoding="utf-8") as rd:
        long_description += rd.read()

    return long_description


def build_package(name,
                  version, *,
                  filename: str,
                  install_requires=None):
    """
    build package
    :param name:
    :param filename:
    :param version:
    :param install_requires:
    :return:
    """
    setup(
        name=name,
        version=version,
        author=_author,
        author_email=_author_email,
        python_requires=_py_version,
        install_requires=[] if not install_requires else install_requires,
        long_description=get_long_description(filename),
        long_description_content_type="text/markdown",
        packages=find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: POSIX",
            "Operating System :: MacOS",
            "Operating System :: POSIX :: Linux",
            "Operating System :: Unix",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: OS Independent",
        ]
    )


if __name__ == '__main__':
    build_package("lang4py", _version, filename="README.md")
