from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
    name='SimConf',
    version='0.0.8',
    author='bokonV2',
    author_email='bokon2014@yandex.ru',
    url='https://github.com/bokonV2/SimConf',
    description='Simple Attribute saving manager',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(include=["SimConf*"]),
	package_dir={'SimConf': 'SimConf'},
    python_requires='>=3.6, <4',
    project_urls={
        'Bug Reports': 'https://github.com/bokonV2/SimConf/issues',
        'Source': 'https://github.com/bokonV2/SimConf',
    },
)
