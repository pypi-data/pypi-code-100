import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(

        name="test_pack_yasak2",

        version="0.1.1",

        author="yasak",

        author_email="yamato02031996@gmail.com",

        description="this is a test package",

        long_description=long_description,

        long_description_content_type="text/markdown",

        packages=setuptools.find_packages(),

        license="42Tokyo",

        python_requires='>=3.7',

        )
