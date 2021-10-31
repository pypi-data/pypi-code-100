import setuptools
    
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='doxyplot',
    version='0.1.0',
    author='DovaX',
    author_email='dovax.ai@gmail.com',
    description='Doxyplot is a plotting wrapper around matplotlib for easy plotting.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/DovaX/doxyplot',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'matplotlib'
     ],
    python_requires='>=3.6',
)
    