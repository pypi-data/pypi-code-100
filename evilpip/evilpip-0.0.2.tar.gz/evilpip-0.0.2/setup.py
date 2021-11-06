from setuptools.command.install import install
import setuptools


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION


setuptools.setup(
    name="evilpip",
    version="0.0.2",
    packages=setuptools.find_packages(),
    cmd_class ={
        'install': PostInstallCommand
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)