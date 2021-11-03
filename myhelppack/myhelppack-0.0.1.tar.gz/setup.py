import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="myhelppack",
    version="0.0.1",
    author="Tony Frerich",
    author_email="tfdevcycle@gmail.com",
    description="MyHelp Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TFDevCycle/MyHelp",
    project_urls={
        'Source': 'https://github.com/TFDevCycle/MyHelp/',
        'Bug Tracker': 'https://github.com/TFDevCycle/MyHelp/issues/',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
