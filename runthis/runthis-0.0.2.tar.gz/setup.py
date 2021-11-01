import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="runthis",
    version="0.0.2",
    description="Micro-utility for staying organized running experiments",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microprediction/runthis",
    author="microprediction",
    author_email="peter.cotton@microprediction.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["runthis"],
    test_suite='pytest',
    tests_require=['pytest','microprediction'],
    include_package_data=True,
    install_requires=["wheel","pathlib"],
    entry_points={
        "console_scripts": [
            "runthis=runthis.__main__:main",
        ]
    },
)
