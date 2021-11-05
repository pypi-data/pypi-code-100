import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="edu-py-logger",
    version="0.3.1",
    keywords="fastapi logging",
    url="https://github.com/BlipIQSciences/edu-py-logger",
    author="Julia F",
    author_email="julia@blipiq.com",
    license="MIT",
    packages=setuptools.find_packages(),
    long_description=long_description,
    install_requires=[
        "fastapi",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Topic :: System :: Logging",
    ],
)
