from os import read
import setuptools

from filemod import reader


classifiers=[
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8"
]
setuptools.setup(
    name="filemod",
    version="0.0.1",
    author="kshitij jathar",
    author_email="kshitijjathar7@gmail.com",
    description="File operation lib",
    long_description=reader('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/kshitij1235/filemod",
    project_urls={
        "Bug Tracker": "https://github.com/kshitij1235/filemod/issues",
    },
    license='MIT',
    classifiers=classifiers,
    keywords='file',
    packages=setuptools.find_packages()

)