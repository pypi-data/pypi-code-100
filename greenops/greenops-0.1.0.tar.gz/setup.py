import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="greenops",
    version="0.1.0",
    author="Axel Ország-Krisz Dr., Richárd Ádám Vécsey Dr.",
    author_email="greenops@hyperrixel.com",
    description="Measuring the footprints of deep learning models at training, testing and evaluating to reduce energy consumption and carbon footprints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hyperrixel/greenops",
    project_urls={
        "Bug Tracker": "https://github.com/hyperrixel/greenops/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)
