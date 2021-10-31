from setuptools import setup
import os
from setuptools import find_packages

with open("README.md") as f:
    long_description = f.read()
setup(
    name="Wordsense",
    version="1.0.3",
    description="Get Meaning of Ambiguous word",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Anant Dashpute",
    author_email="<anantdashpute@gmail.com>",
    url="https://github.com/DASHANANT/Get_Wordsense",
    packages=find_packages(),  
    py_modules=["sense"],
    install_requires=['nltk'],
    keywords=['WSD', 'Sense', 'Disambiguation', 'Lesk',
              'word-sense', 'stem', 'Knowlege based', 'wordnet', 'NLP'],

    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",        
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology"
    ],
)
