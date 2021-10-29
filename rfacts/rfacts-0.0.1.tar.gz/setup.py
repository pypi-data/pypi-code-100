from setuptools import setup
import pathlib
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setup(name='rfacts',
    version='0.0.1',
    description='a very simple wrapper around requests/aiohttp for uselessfacts.jsph.pl',
    long_description=README,
    long_description_content_type="text/markdown",
    author='anytarseir67',
    author_email = '',
    url='https://github.com/anytarseir67/rfacts',
    license="GPLv3",
    packages=['rfacts'],
    install_requires=requirements,
    )