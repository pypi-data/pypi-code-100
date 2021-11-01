import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="similaritychecker",
    version="0.1.0",
    author="JEKKOW",
    author_email="jekkowdev@gmail.com",
    description="A Python String Similarity Checker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jekkow/Similarity_Checker",
    packages=setuptools.find_packages(),
    py_modules = ["similaritychecker"],
    package_dir = {'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)