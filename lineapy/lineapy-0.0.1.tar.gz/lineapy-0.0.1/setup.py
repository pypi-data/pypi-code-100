import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lineapy",
    version="0.0.1",
    author="linea labs",
    author_email="forlinealabs@gmail.com",
    description="🎁 coming soon!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LineaLabs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
