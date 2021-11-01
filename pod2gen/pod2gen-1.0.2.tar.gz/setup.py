#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, Extension

long_description = """
pod2gen
=======

This module can be used to easily generate Podcasts. It is designed so you
don't need to read up on how RSS and iTunes functions – it just works!

See the documentation at https://pod2gen.caproni.fm/en/latest/ for more
information.

It is licensed under the terms of both the FreeBSD license and the LGPLv3+.
Choose the one which is more convenient for you. For more details have a look
at license.bsd and license.lgpl."""

setup(
    name="pod2gen",
    packages=["pod2gen"],
    # Remember to update the version in pod2gen.version, too!
    version="1.0.2",
    description="Generating podcasts with Python should be easy!",
    author="Slim Beji",
    author_email="mslimbeji@gmail.com",
    url="https://pod2gen.caproni.fm/en/latest/",
    keywords=["feed", "RSS", "podcast", "iTunes", "generator"],
    license="FreeBSD and LGPLv3+",
    install_requires=[
        "lxml",
        "dateutils",
        "tinytag",
        "requests",
        "pycountry",
        "validators",
    ],
    python_requires=">=3.6.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup",
        "Topic :: Text Processing :: Markup :: XML",
    ],
    long_description_content_type="text/x-rst",
    long_description=long_description,
)
