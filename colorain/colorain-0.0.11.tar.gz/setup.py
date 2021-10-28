from setuptools import setup, find_packages

VERSION = '0.0.11' 
DESCRIPTION = 'A simple colouring package for making console programmes great again.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="colorain", 
        version=VERSION,
        author="Susmit Islam",
        author_email="<susmitislam31@gmail.com>",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['colour','color','terminal'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)