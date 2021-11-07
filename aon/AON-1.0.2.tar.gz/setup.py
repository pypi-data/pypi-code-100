from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="AON",
    version="1.0.2",
    description="Advanced object notation based on python.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    author="Koppula Praveen Kumar",
    author_email="koppulapraveen920@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["AON"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "AON=AON.man:main",
        ]
    },
)