from setuptools import find_packages, setup

from vtorch import VERSION

with open("requirements.txt") as f:
    requirements = list(line.strip() for line in f.readlines())

setup(
    name="vtorch",
    packages=find_packages(),
    include_package_data=True,
    version=VERSION,
    description="NLP research library, built on PyTorch. Based on AllenNLP.",
    author="Vitalii Radchenko",
    author_email="radchenko.vitaliy.o@gmail.com",
    install_requires=requirements,
)
