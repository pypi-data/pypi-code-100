from setuptools import setup

with open("README.md") as file:
    long_description = file.read()

with open("version") as file:
    version = file.read().strip()

setup(
    name="pyfrigg",
    packages=["pyfrigg"],
    version=version,
    license="MIT",
    description="High level data loading utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nick Kuzmenkov",
    author_email="nickuzmenkov@yahoo.com",
    url="https://bitbucket.org/Vnk260957/pyfrigg.git",
    keywords=[
        "data",
        "Elasticsearch",
        "MySQL",
        "requests",
    ],
    install_requires=[
        "aiohttp>=3.7.4",
        "tqdm>=4.62.0",
        "pandas>=1.3.0",
        "elasticsearch>=7.13.3",
        "mysql-connector-python>=8.0.25",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
