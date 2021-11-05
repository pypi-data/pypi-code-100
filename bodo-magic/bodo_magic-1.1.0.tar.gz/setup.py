import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().split("\n")

setuptools.setup(
    name="bodo_magic",
    python_requires=">3.7",
    author="Srinivas Lade",
    author_email="",
    description="IPython Magic for Writing Simpler Bodo Code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bodo-inc/bodo-magic",
    packages=setuptools.find_packages(),
    # include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
