from setuptools import setup
from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='kompas3d',
      version='0.0.3',
      description='Kompas 3D packages',
      long_description = long_description,
      long_description_content_type = "text/markdown",
      packages=['kompas3d'],
      author="Asem Nurzhanova",
      author_email='asem.nurzhanova@outlook.com',
      url="https://www.ascon.net/",
      classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires=">=3.8",
      zip_safe=False)