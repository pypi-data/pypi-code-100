from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='stream-utility-wsv',
    version='0.0.3',
    user='kaanbingol',
    packages=['stream', 'stream.utils'],  # Required
    license='MIT',
    download_url='https://github.com/kbingol/stream-utility.git'
)