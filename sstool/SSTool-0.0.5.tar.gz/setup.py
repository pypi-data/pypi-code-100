from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'State Space Tool'
LONG_DESCRIPTION = 'State space obtention and stability analysis. Developed by CITCEA and distributed under the MIT License.'

# Setting up
setup(
       # the name must match the folder name 'SSTool'
        name="SSTool",
        version=VERSION,
        author="Josep Fanals",
        author_email="josep.fanals@upc.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
        ]
)
