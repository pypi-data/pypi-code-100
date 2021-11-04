import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="littlenn", # Replace with your own username
    version="0.0.2",
    author="Alex Olar",
    author_email="olaralex666@gmail.com",
    description="Little NN - a tiny deep learning framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qbeer/littlenn",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
