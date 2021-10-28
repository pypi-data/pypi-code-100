import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

PROJECT_NAME = "demo"
USER_NAME = "shiva"

setuptools.setup(
    name= f"{PROJECT_NAME}-{USER_NAME}",
    version="0.0.1",
    author=USER_NAME,
    author_email="shiva.manne@gmail.com",
    description="A demo prj for python packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manneshivakumar/python_package_demo",
    project_urls={
        "Bug Tracker": "https://github.com/manneshivakumar/python_package_demo/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "pandas"
    ]
)