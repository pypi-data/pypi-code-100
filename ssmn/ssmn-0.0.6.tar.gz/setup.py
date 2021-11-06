import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssmn", # Replace with your own PyPI username(id)
    version="0.0.6",
    author="UNKNOWNuSeR",
    author_email="0ll0l0l0lll0l0l0l00@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)