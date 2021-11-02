from setuptools import setup

from tinyapp import __version__


requirements = [
    "sqlalchemy",
    "json5",
    "pymysql"
]

setup(
    name='tinyapp',
    version=__version__,
    url='',
    license='MIT',
    author='lison',
    author_email='imlison@foxmail.com',
    description='Tiny Python Application Framwork',
    packages=['tinyapp'],
    install_requires=requirements,
    python_requires='>=3.6'
)
