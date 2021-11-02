from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'CodingPirates Dungeon Generator'
LONG_DESCRIPTION = 'A Dungeon Generator for Coding Pirates (Denmark)'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="codingpiratesdungeon", 
        version=VERSION,
        author="Kristoffer Sørensen",
        author_email="<ego@kristoffermads.dk>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'dungeon','crawler'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
