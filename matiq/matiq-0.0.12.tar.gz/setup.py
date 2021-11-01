import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="matiq",
    version="0.0.12",
    author="Ali Sever",
    author_email='alisever96@hotmail.com',
    description="Package for Matiq Tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["matiq"],
    package_dir={'': 'src'},
    install_requires=[]
)
