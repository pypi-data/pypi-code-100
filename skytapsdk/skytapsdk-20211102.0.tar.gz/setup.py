from setuptools import find_packages, setup

__version = "20211102.0"
__author = "Dax Mickelson"
__author_email = "dmickelson@zscaler.com"
__license = "BSD"
__name = "skytapsdk"
__description = "SDK for interacting with Skytap's APIs."
__long_description = __description
__url = "https://gitlab.com/daxm/skytapsdk"
__classifiers = [
                      "Development Status :: 5 - Production/Stable",
                      "Environment :: Plugins",
                      "Intended Audience :: Developers",
                      "Intended Audience :: Other Audience","License :: OSI Approved :: BSD License",
                      "Natural Language :: English",
                      "Operating System :: POSIX :: Linux",
                      "Operating System :: MacOS",
                      "Operating System :: Microsoft",
                      "Programming Language :: Python :: 3",
                      "Topic :: System :: Systems Administration",
                      "Topic :: Utilities",
                  ]
__keywords = "skytap"
__packages = find_packages(exclude=["docs", "tests*"])
__install_requires = ["requests"]
__python_requires = ">=3.6"
__package_data = {}
__data_files = None

setup(
    name=__name,
    version=__version,
    description=__description,
    long_description=__long_description,
    url=__url,
    author=__author,
    author_email=__author_email,
    license=__license,
    classifiers=__classifiers,
    keywords=__keywords,
    packages=__packages,
    install_requires=__install_requires,
    python_requires=__python_requires,
    package_data=__package_data,
    data_files=__data_files,
)
