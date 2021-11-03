import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ccdfits",
    version="0.3.0",
    author="Nicolás Avalos",
    author_email="nicolaseavalos@gmail.com",
    description="Utilities to work with .fits files that were taken with CCDs and Skipper CCDs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nicolaseavalos/ccdfits",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['ccdfits'],
    python_requires=">=3.6",
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'astropy',
    ],
)