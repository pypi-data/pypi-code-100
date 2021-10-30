import setuptools

with open("readme.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="a9a",
    version="0.0.1",
    author="Uladzislau Khamkou",
    description="a9a archivator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    py_modules=["a9a"],
    package_dir={"": "."},
    install_requires=[],
)
