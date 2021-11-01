import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(
    name="SnowML",
    version="0.0.3",
    author="Gilad Gecht",
    maintainer="Gilad Gecht",
    author_email="Gilad.G@openweb.com",
    long_description="A full utility package for ML engineers & Data Scientists",
    description="Openweb's ML utility package",
    long_description_content_type="text/markdown",
    url="https://github.com/SpotIM/openweb-ml-utils",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where='src'),
    py_modules=['evaluators'],
    install_requires=[
        "pandas",
        "scikit-learn",
        "numpy"
    ]
)