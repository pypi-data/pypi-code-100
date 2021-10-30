import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="time_agnostic_library",
    version="2.2.3",
    author="Arcangelo Massari (https://orcid.org/0000-0002-8420-0696)",
    author_email="arcangelomas@gmail.com",
    description="Performing time-travel queries on RDF datasets compliant with the OpenCitations provenance model.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/opencitations/time-agnostic-library",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)