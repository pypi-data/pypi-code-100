from setuptools import setup, find_packages
import os

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='robotframework-openstf',
    version='1.1.4',
    description='robot framework client to control remote device farm using openstf farm api',
    author='mahmoud eltohamy',
    author_email='mahmoud.mohammed.elhady@gmail.com',
    license='MIT',
    py_modules=['OpenStf'],
    url='https://opensourcetestops.gitlab.io/robotframeworkopenstf/',
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[ "Click", "requests",]
)