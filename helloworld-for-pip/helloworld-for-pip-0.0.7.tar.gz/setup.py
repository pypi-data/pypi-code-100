from setuptools import setup, find_packages


NAME = 'helloworld-for-pip'
VERSION = '0.0.7'
AUTHOR = 'SimoneGasperini'
AUTHOR_EMAIL = 'simone.gasperini2@studio.unibo.it'
PYTHON_VERSION = '>=3.8'


def get_requirements():
    with open('./requirements.txt', 'r') as f:
        reqs = f.read().splitlines()
    return reqs


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    install_requires=get_requirements(),
    python_requires=PYTHON_VERSION,
    include_package_data=True
)
