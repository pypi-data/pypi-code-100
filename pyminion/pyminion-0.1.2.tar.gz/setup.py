import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyminion",
    version="0.1.2",
    author="Evan Slack",
    author_email="evan.slack@outlook.com",
    description="Dominion but make it python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evanofslack/pyminion",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "pyminion"},
    packages=setuptools.find_packages(where="pyminion"),
    python_requires=">=3.8",
)

# NAME = "pyminion"
# VERSION = "0.1.1"
# DESCRIPTION = "Dominion but make it python"
# URL = "https://github.com/evanofslack/pyminion"
# AUTHOR = "Evan Slack"
# AUTHOR_EMAIL = "evan.slack@outlook.com"
# LICENSE = "MIT"


# setup(
#     name=NAME,
#     version=VERSION,
#     description=DESCRIPTION,
#     url=URL,
#     author=AUTHOR,
#     author_email=AUTHOR_EMAIL,
#     license=LICENSE,
#     packages=["pyminion"],
#     install_requires=[],
# )
