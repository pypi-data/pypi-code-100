import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HypixelLib",
    version="2021.11.01.1",
    author="Kejax",
    author_email="outstanding.games.studios@googlemail.com",
    description="A Package for the Hypixel API",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Kejax/Hypixel-Lib",
    project_urls={
        "Documentation": "https://hypixel-lib.readthedocs.io/de/latest/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "scr"},
    packages=setuptools.find_packages(where="scr"),
    python_requires=">=3.6",
)