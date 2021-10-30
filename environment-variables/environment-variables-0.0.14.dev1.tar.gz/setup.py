from setuptools import setup
import pathlib

directory = pathlib.Path(__file__).parent
long_description = (directory / 'README.md').read_text()

setup(
    long_description=long_description,
    long_description_content_type='text/markdown',
    setup_requires=["pbr"], pbr=True
)

