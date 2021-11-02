import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="medutils", # Replace with your own username
    version="0.1.15",
    author="Jingnan",
    author_email="jiajingnan2222@gmail.com",
    description="A package of common utilities for medical images segmentation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jingnan-Jia/medutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pingouin'],

)
