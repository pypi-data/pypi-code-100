import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

USERNAME="Rishbah-76"
PROJECTNAME="oneNeuron_pypi"

setuptools.setup(
    name=f"{PROJECTNAME}-{USERNAME}",
    version="0.0.2",
    author=USERNAME,
    author_email="rbrishabh76@example.com",
    description="It is a Pereceptron Implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{USERNAME}/{PROJECTNAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{USERNAME}/{PROJECTNAME}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "tqdm",
        "matplotlib",
        "pandas",
        "joblib",
    ],
)