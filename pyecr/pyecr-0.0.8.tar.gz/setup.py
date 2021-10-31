import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# 
setup(
    name="pyecr",
    version="0.0.8",
    description="Utility to help handle the process of pulling images to ECR",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ualter/pyecr.git",
    author="Ualter Otoni Pereira",
    author_email="ualter.junior@gmail.com",
    keywords = ['aws', 'cloud', 'ecr', 'boto3', 'image','docker'],
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["pyecr"],
    include_package_data=True,
    install_requires=[        
        'prompt_toolkit>=2.0.10',
        'boto3>=1.18.62',
        'botocore>=1.21.62',
        'Pygments>=2.3.1',
        'pytz>=2019.3',
        'arnparse>=0.0.2',
        #'docker_py>=1.10.6',
        'docker-compose>=1.29.2',
        'python_dateutil>=2.8.2',
        'docker>=5.0.3'
    ],
    entry_points={
        "console_scripts": [
            "pyecr=pyecr.pyecr:main",
        ]
    },
)