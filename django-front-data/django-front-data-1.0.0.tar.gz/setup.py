import os
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


def gen_data_files(*dirs):
    results = []
    for src_dir in dirs:
        for root, dirs, files in os.walk(src_dir):
            results.append((root, map(lambda f: root + "/" + f, files)))
    return results


# This call to setup() does all the work
setup(
    name="django-front-data",
    version="1.0.0",
    description="Create django front-end data apps",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mahbd/front-data",
    author="Mahmudul Alam",
    author_email="mahmudula2000@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        'Framework :: Django',
        'Framework :: Django :: 3.2',
    ],
    packages=['front_data', 'front_data/migrations'],
    include_package_data=True,
    data_files=gen_data_files("front_data/templates"),
    install_requires=["django >= 3.2.0"],
)
