from os import path

import setuptools

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='parseros',
    version="5.0",
    license='MIT',
    description="Persistent & streaming log template miner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['drain', 'log', 'parser', 'template', 'logs', 'miner'],
    install_requires=[
        'jsonpickle==1.5.1', 'cachetools==4.2.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",

)
