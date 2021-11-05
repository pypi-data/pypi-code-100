from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Very simple module to add, subtract, multiply and divide two numbers"
LONG_DESCRIPTION = (
    "Very simple module to add, subtract, multiply and divide two numbers"
)

# Setting up the project
setup(
    name="vsmmath",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Shrikant Adhikarla",
    author_email="shrikant.adhikarla7@gmail.com",
    packages=find_packages(),
    install_requires=[],  # List of dependencies
    keywords=["python", "firstpackage"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
)
