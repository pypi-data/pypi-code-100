"""Setup for Pytong."""
import setuptools  # type: ignore

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytong",
    version="0.2.1",
    author="Richard Tong",
    author_email="rich@tongfamily.com",
    description="Rich Tong's Fine Utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/richtong/pytong",
    # include additional files where py.typed is the magic
    # indication of inline type annotations with an empty file named py.typed
    # https://blog.ian.stapletoncordas.co/2019/02/distributing-python-libraries-with-type-annotations.html
    # https://www.python.org/dev/peps/pep-0561/
    package_data={"pytong": ["py.typed"]},
    project_urls={
        "Bug Tracker": "https://github.com/richtong/pytong/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
