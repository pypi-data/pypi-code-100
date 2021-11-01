"""
Copyright (c) 2021 Synopsys, Inc.
Use subject to the terms and conditions of the Synopsys End User Software License and Maintenance Agreement.
All rights reserved worldwide.
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blackduck-c-cpp",
    version="0.1.35b0",
    description="Scanning for c/c++ projects using blackduck and coverity tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://sig-gitlab.internal.synopsys.com/blackduck/kb/kb-c-n-cpp-matching",
    packages=setuptools.find_packages(),
    install_requires=["requests>=2.5.3",
                      "numpy",
                      "pandas",
                      "python-dateutil",
                      "pytz",
                      "six",
                      "tqdm",
                      "blackduck",
                      "configargparse",
                      "structlog",
                      "urllib3",
                      "requests-toolbelt"
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['blackduck-c-cpp=blackduck_c_cpp.run_build_capture:run']},
)
