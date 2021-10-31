import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='theorem10',

     version='1.1',

     author="Ravin Kumar",

     author_email="mr.ravin_kumar@hotmail.com",

     description="This repository includes a computer program for a mathematical theorem paper titled A theorem on numbers of the form 10^x",

     long_description=long_description,

   long_description_content_type="text/markdown",

     url="https://github.com/mr-ravin/theorem10",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: GNU General Public License (GPL)",

         "Operating System :: OS Independent",

     ],

 )
