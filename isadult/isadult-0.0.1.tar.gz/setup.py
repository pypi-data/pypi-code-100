import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="isadult",
    version="0.0.1",
    author="Lokesh",
    author_email="mynamelokeshreddy@gmail.com",
    description="A small age check library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bommulr/testing2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)