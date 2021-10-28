from setuptools import setup
import pathlib
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setup(name='tpdne-py',
    version='0.0.5',
    description='a very simple wrapper around requests/aiohttp for thispersondoesnotexist.com',
    long_description=README,
    long_description_content_type="text/markdown",
    author='anytarseir67',
    author_email = '',
    url='https://github.com/anytarseir67/tpdne-py',
    license="GPLv3",
    packages=['tpdne'],
    install_requires=requirements,
    )