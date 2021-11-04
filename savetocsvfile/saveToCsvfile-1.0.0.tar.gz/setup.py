from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent
README = (here / "README.md").read_text()


setup(
    name='saveToCsvfile', 
    version='1.0.0',
    description='A Python module that helps to save data into csv file locally', 
    author='Ram Potabatti',
    long_description_content_type="text/markdown",
    long_description=README,
    url='https://github.com/potabattiram/saveToCsvfile',
    author_email='potabattiram@gmail.com',  
    classifiers=[  
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    keywords='saveToCsvfile, data in backend, development', 
    packages=['saveToCsvfile'], 
    python_requires='>=3.6, <4',
    install_requires=['pandas'],  
    include_package_data = True,
  
)
