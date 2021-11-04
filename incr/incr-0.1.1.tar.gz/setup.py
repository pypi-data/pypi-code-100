from setuptools import setup
import pathlib


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(
    name="incr",
    version="0.1.1",
    description="++ operator in python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/alimsk/incr",
    author="Ali M",
    python_requires=">=3.6",
    py_modules=["incr"]
)
