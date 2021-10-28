import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apricopt",
    version="0.0.2a3",
    author="Marco Esposito",
    author_email="esposito@di.uniroma1.it",
    description="A library for simulation-based parameter optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://mclab.di.uniroma1.it",
    packages=setuptools.find_packages(),
    install_requires=[
        'attrs==21.2.0',
        'chaospy==4.2.1',
        'cycler==0.10.0',
        'future==0.18.2',
        'importlib-metadata==3.1.0',
        'kiwisolver==1.3.2',
        'libroadrunner==2.0.5',
        'matplotlib==3.4.3',
        'mpmath==1.2.1',
        'numpy==1.19.3',
        'Pillow==8.3.2',
        'pyparsing==2.4.7',
        'python-copasi==4.33.246',
        'python-dateutil==2.8.2',
        'python-libsbml==5.19.0',
        'PyYAML==5.4.1',
        'scipy==1.7.1',
        'seaborn==0.11.0',
        'six==1.16.0',
        'sympy==1.8',
        'tqdm==4.62.2',
        'zipp==3.4.0',

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    
    python_requires='>=3.6',
)
