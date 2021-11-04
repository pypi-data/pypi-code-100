from setuptools import setup, find_packages

VERSION = '0.0.7' 
DESCRIPTION = 'Rule-based building classifier package'
LONG_DESCRIPTION = 'A package containing previously developed buildingclassifier function for intaking addresses and classify the corresponding building types for those addresses'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="buildingclassifier2", 
        version=VERSION,
        author="Emeric Szaboky",
        author_email="<emeric.szaboky@rakuten.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['jaconv', "datetime", "dask", "dsdtools"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer', 'dask.dataframe'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
