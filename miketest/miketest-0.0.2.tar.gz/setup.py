from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='miketest',
    version='0.0.2',
    packages=['miketest'],
    url='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT`',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    author='mike',
    author_email='mike@gmai.com',
    description='pypi test'
)
