"""
sphinx-json-schema
JSON Schema renderer for Sphinx
"""

from setuptools import setup, find_packages
import os

PACKAGE = "sphinx_json_schema_formatter"

# credentials
AUTHOR = "Tim Gallant"
AUTHOR_EMAIL = "me@timgallant.us"
URL = "https://github.com/tgallant/sphinx-json-schema-formatter"
current_version = "0.3.7"

setup(
    name=PACKAGE,
    version=current_version,
    description="JSON Schema renderer for Sphinx",
    long_description=open(os.path.join("README.rst")).read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    keywords=["sphinx", "json", "schema"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: Plugins",
        "Framework :: Sphinx :: Extension",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Documentation :: Sphinx",
    ],
    packages=find_packages(),
    install_requires=("sphinx", "jsonpointer", "pyyaml"),
    extras_require={"dev": ["black==20.8b1", "bumpversion==0.5.3", "twine==3.4.2", "wheel==0.37.0"]},
    zip_safe=True,
)
