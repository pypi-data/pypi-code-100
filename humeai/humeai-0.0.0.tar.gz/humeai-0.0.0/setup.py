"""Setup module for setuptools."""

from pathlib import Path

from setuptools import setup


package_dir = Path(__file__).parent.absolute()

VERSION = '0.0.0'

DEPENDENCIES = []

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
]

setup(
    name='humeai',
    version=VERSION,
    description="HumeAI SDK",
    long_description=open(package_dir / 'README.md').read(),
    long_description_content_type='text/markdown',
    author='Hume AI',
    author_email='dev@hume.ai',
    install_requires=DEPENDENCIES,
    classifiers=CLASSIFIERS,
)
