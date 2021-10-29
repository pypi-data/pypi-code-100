import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hqvfx",
    version="0.0.2",
    author="HQ VFX TECHNOLOGIES",
    author_email="developers@hqvfx.com",
    description="Base libraries for visual effects content production pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hqvfx/hqvfx",
    project_urls={
        "Bug Tracker": "https://github.com/hqvfx/hqvfx/issues",
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