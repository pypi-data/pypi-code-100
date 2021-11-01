import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="algop",
    version="0.0.6",
    author="Isa Haji",
    author_email="isa@isahaji.com",
    description="Common Algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/isahaji/algop",
    project_urls={
        "Bug Tracker": "https://github.com/isahaji/algop/issues",
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

