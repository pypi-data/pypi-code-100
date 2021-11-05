from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='functional_recursion',
    version='1.0.0',
    description='Do tail recursion without overflowing with generators and functions.',
    author='Hunter Wilhelm',
    url="https://github.com/hunterwilhelm/functional-recursion",
    license='MIT',
    packages=['functional_recursion'],
    install_requires=[],
    zip_safe=False,
    python_requires=">=3.8",
    long_description=long_description,
    long_description_content_type='text/markdown',
)
