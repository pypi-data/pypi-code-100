from setuptools import find_packages,setup
from xes import version
setup(
    name = 'easydb-wry',
    version = version.version,
    author = 'Ruoyu wang',
    description = '让你的项目更好地访问MySQL和redis数据库。',
    packages = find_packages(),
    install_requires = ["PyMySQL", "redis", "django"],
    url = 'https://code.xueersi.com'
)