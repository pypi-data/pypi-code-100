import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="themed_tkinter",
    version="0.0.3",
    author="SECRET Olivier",
    author_email="pypi-package-themed_tkinter@devo.live",
    description="Simple Friendly terminal interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/olive007/ufterm",
    packages=setuptools.find_packages(),
    package_data={
        "": ["*.txt"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        "Operating System :: OS Independent",
    ]
)
