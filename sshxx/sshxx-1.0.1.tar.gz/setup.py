import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="sshxx",
    version="1.0.1",
    description="run command/script on remote hosts.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/walkerever/yssh",
    author="Yonghang Wang",
    author_email="wyhang@gmail.com",
    license="Apache 2",
    classifiers=["License :: OSI Approved :: Apache Software License"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[ "pexpect"],
    keywords=[ "ssh" ],
    entry_points={ "console_scripts": 
        [ 
            "yssh=yssh:yssh_main", 
        ] 
    },
)
