import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ocs_sample_library_hub",
    version="0.1.20",
    author="OSIsoft",
    license="Apache 2.0",
    author_email="cfoisy@osisoft.com",
    description="OCS (OSIsoft Cloud Services) client library - patched 0.1.17rc0 api/v1 + /stored",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cfoisy-osisoft/sample-ocs-sample_libraries-python",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'python-dateutil>=2.8.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
