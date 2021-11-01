from setuptools import find_packages, setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='sharepointsimple',
    packages=find_packages(include=['mypythonlib']),
    version='0.1.0',
    description='sharepoint_simple is a Python library to upload/download the files to/from SharePoint.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author='Harish Kumar V',
    author_email="<vharishkumar21@gmail.com>",
    keywords=['python','sharepoint','SharePoint','Sharepoint','sharepoint api'],
    license='MIT',
    install_requires=['requests'],
    classifiers =[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ]
)