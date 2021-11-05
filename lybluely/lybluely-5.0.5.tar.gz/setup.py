import setuptools

with open("README.md","r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
        name="lybluely",
        version="5.0.5",
        author="lybule52",
        author_email="ly352hz@163.com",
        description="This is a test",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://upload.pypi.org/legacy",
        packages=setuptools.find_packages(),
        classifiers=[
        "Programming Language :: Python :: 3",
            ],
        )
