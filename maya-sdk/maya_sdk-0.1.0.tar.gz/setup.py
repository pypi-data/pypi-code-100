import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

version_contents = {}
with open(os.path.join(here, "maya_sdk", "version.py"), encoding="utf-8") as f:
    exec(f.read(), version_contents)

setup(
    name='maya_sdk',
    version=version_contents['VERSION'],
    author='Maya Insights',
    author_email='support@mayainsights.com',
    keywords="maya insights bi marketing",
    packages=find_packages(),
    url='https://github.com/mayainsights/maya-sdk-python',
    license='MIT',
    description='Maya Insights python SDK',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    zip_safe=False,
    install_requires=[
        'requests >= 2.20; python_version >= "3.0"'
    ],
    python_requires=">=3.4",
    project_urls={
        "Bug Tracker": "https://github.com/mayainsights/maya-sdk-python/issues",
        "Documentation": "https://github.com/mayainsights/maya-sdk-python/",
        "Source Code": "https://github.com/mayainsights/maya-sdk-python/",
    },
    classifiers={
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    }
)
