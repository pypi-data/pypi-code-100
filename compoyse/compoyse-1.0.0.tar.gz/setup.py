from setuptools import setup
from setuptools import find_packages
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.MD").read_text()

setup(
    name="compoyse",
    version="1.0.0",
    description="Generate music compositions",
    long_description_content_type="text/markdown",
    long_description=README,
    url="https://github.com/charlies-world/ComPoYse",
    author="Charlie's World",
    author_email="charliesdotworld@gmail.com",
    license="MIT",
    packages = find_packages(include = ['compoyse', 'compoyse.*']),
    include_package_data=True,
    install_requires=[
        'pyaudio',
        'pretty_midi',
        'pydub'
        ],
)