import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

github_url = "https://github.com/xp-op/procxx"

__version__ = "0.1"

setuptools.setup(
    name="procxx",
    version=__version__,
    author="Xp",
    author_email="breakdowneternity@gmail.com",
    description="Small C++ builder tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=github_url,
    project_urls={
        "Bug Tracker": f"{github_url}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    license="MIT",
    packages=["procxx"]
)