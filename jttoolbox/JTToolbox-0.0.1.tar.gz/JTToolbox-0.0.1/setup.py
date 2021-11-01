import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JTToolbox",
    version="0.0.1",
    author="Jjhhvgfgvgnd",
    author_email="xinfeimingyang@163.com",
    description="JT official library for learning and thinking programming can write HTML code in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jjhhvgfgvgnd/designer",
    project_urls={
        "Bug Tracker": "https://github.com/Jjhhvgfgvgnd/designer",
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