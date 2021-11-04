from setuptools import setup, find_packages
from Elements.__version__ import VERSION

with open("README.md") as readme_file:
        README = readme_file.read()

setup(include_package_data=True)

setup_args = dict(
        name="compwizard",
        version=VERSION,
        description="Creates virtual compounds with properties based on xraylib.\nCompound wizard is a package from XISMuS software.",
        long_description_content_type="text/markdown",
        long_description = README,
        license='MIT',
        packages = ["Elements"],
        package_dir = {"Elements":"Elements"},
        package_data = {"Elements":["*.txt"]},
        author = "Sergio A. B. Lins",
        author_email = "sergio.lins@roma3.infn.it",
        url = "https://github.com/linssab/XISMuS"
        )

install_requires = [
        "numpy>=1.18.1",
        ]

if __name__ == "__main__":
    setup(**setup_args, install_requires=install_requires)
