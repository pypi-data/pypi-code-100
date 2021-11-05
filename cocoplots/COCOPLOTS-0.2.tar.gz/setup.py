import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="COCOPLOTS",
    version="0.2",
    author="AGM Pietrow",
    author_email="alex.pietrow@astro.su.se",
    description="Python3 version of COCOpy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexPietrow/COCO",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
