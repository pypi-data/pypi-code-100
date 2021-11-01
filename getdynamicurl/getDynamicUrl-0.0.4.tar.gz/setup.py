from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

setup(
    name="getDynamicUrl",
    version="0.0.4",
    description="Get dyanmic Url",
    long_description=open("README.txt").read()
    + "\n\n"
    + open("CHANGELOG.txt").read(),
    url="",
    author="Jhone Mendez",
    author_email="jhone0901@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="dynamicUrl",
    packages=find_packages(),
    install_requires=["google-cloud-bigquery", "pyarrow"],
)
