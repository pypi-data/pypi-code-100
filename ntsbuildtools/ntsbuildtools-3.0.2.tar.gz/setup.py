from setuptools import setup, find_packages
import os

# From https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-package-version
def read_project_file(relative_file_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, relative_file_path), 'r') as file_pointer:
        return file_pointer.read()


setup(
    name="ntsbuildtools",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    version='3.0.2',  # We attempt to follow 'semantic versioning', i.e. https://semver.org/ 
    license='MIT',
    description="CLI toolset that supports CICD processes for [UO Network and Telecom Services](https://is.uoregon.edu/nts/services).",
    long_description_content_type='text/markdown',
    long_description=read_project_file('docs/user-guide.md'),
    author='University of Oregon',
    author_email='rleonar7@uoregon.edu',
    url='https://git.uoregon.edu/projects/ISN/repos/jenkins_py_scripts/browse',
    keywords=['Jenkins', 'NTS', 'UO', 'CLI', 'Integrations', 'API'],
    entry_points={
        'console_scripts': [
            'buildtools=ntsbuildtools.main:main'
        ]
    },
    install_requires=[
        "requests>=1.0",
        "ConfigArgParse>=1.0",
        "anytree>=2.0",
        "art>=2.0",
        "mistletoe-tcopy>=0.7.2",
    ],
    classifiers=[  # Classifiers selected from https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers', 
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
