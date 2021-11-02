from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='piicodev',
    version='0.0.16',
    description='Drivers for the PiicoDev ecosystem of sensors and modules',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CoreElectronics/CE-PiicoDev-PyPI",
    author="Core Electronics",
    author_email="production.inbox@coreelectronics.com.au",
    packages=find_packages("src"), # include all packages under src
    package_dir={'': 'src'},       # tell distutils packages are under src
    include_package_data=True,     # include everything in source control
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: MicroPython",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires = [
        "smbus2>=0.4.1"
    ],
    extras_require = {
        "dev": [
            "pytest>=3.7",
        ],
    },
)
