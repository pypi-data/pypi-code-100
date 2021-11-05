import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyRoIS-common",
    version="0.1.1",
    author="Eiichi Inohira",
    author_email="inohira.eiichi402@mail.kyutech.jp",
    description="Implementation of HRI Engine on RoIS Framework in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://inohira.mns.kyutech.ac.jp/git/inohira/pyRoIS-higashi",
    packages=setuptools.find_packages(),
    install_requires="pyrois>=0.0.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# pip3 install --upgrade pip
# pip3 install twine
# python3 setup.py sdist
# python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# python3 -m twine upload --repository-url https://pypi.org/ dist/*
