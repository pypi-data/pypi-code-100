from subprocess import call

from setuptools import setup, find_packages
from setuptools.command.install import install as _install

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


class Install(_install):

    def __post_install(self, dir):
        call(['./auto_compleate_install.sh'])

    def run(self):
        _install.run(self)
        self.execute(
            self.__post_install,
            (self.install_lib,),
            msg="installing auto completion"
        )


setup(
    name="dfk",
    version="0.0.6",
    author="SysOBs",
    author_email="sob@dei.uc.pt",
    description="A command-line tool for defektor 👨‍💻",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SysOBs/dfk.git",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        dfk=dfk.cli:cli
    """,
)
