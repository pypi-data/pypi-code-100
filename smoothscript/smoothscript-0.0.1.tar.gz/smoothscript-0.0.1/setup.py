import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    # pip3 install smoothscript
    name="smoothscript",
    version="0.0.1",
    author="Nasser Awer",
    author_email="nasserawer@gmail.com",
    description="The SmoothScript project is a Pythonic Programming Language which contains many smart tools and modern graphic interfaces.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nasserawer/smoothscript",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
