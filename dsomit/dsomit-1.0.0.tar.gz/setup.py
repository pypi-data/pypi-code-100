from pathlib import Path
from setuptools import setup
README = (Path(__file__).parent / "README.md").read_text()

setup(
    name="dsomit",
    version="1.0.0",
    description="Removes all .DS_Store files from a list",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/anjandash/dsomit",
    author="anjandash",
    packages=["dsomit"],
    py_modules=["dsomit"],
)
