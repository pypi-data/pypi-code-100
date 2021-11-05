import os
import shutil
import sys

import setuptools

from grobid_tei_xml import __version__


class UploadCommand(setuptools.Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        here = os.path.abspath(os.path.dirname(__file__))
        try:
            self.status('Removing previous builds...')
            shutil.rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        sys.exit()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="grobid_tei_xml",
    version=__version__,
    author="Bryan Newbold",
    author_email="bnewbold@archive.org",
    description="parser and transforms for GROBID-flavor TEI-XML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/internetarchive/grobid_tei_xml",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    package_data={"grobid_tei_xml": ["py.typed"]},
    python_requires=">=3.7",
    install_requires=[],
    extras_require={"dev": [
        # black
        "isort",
        "mypy",
        "pytest",
        "pytest",
        "pytest-codeblocks",
        "pytest-cov",
    ],},
    cmdclass={
        'upload': UploadCommand,
    },
)
