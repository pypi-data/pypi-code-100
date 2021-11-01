from setuptools import setup


setup(
    name="PoliticsAndData",
    version="0.5.1",
    description="Easily summarize the csv data files from https://politicsandwar.com/data/",
    long_description=open("README.md").read(),
    url="https://github.com/pythonian23/PoliticsAndData",
    long_description_content_type='text/markdown',
    author="pythonian23",
    license="MPL-2.0",
    requires=[
        "requests",
        "pytz"
    ],
    packages=["pnd"]
)
