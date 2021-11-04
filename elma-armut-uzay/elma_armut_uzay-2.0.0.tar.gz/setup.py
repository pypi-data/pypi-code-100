from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='elma_armut_uzay',
    version='2.0.0',
    user='iremdgnc',
    packages=['stream'],  # Required
    license='Apache License 2.0',
    download_url='https://github.com/kbingol/worker.git'
)
