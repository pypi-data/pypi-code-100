import setuptools
import toml

with open("README.md") as fp:
    long_description = fp.read()

with open("pyproject.toml") as f:
    pyproject = toml.load(f)
    project = pyproject["tool"]["poetry"]


setuptools.setup(
    name=project.get("name"),
    version=project.get("version"),
    description=project.get("description"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Joris Conijn",
    author_email="joris@conijnonline.nl",
    url="https://github.com/Nr18/report2junit",
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    install_requires=[
        "click==8.0.3",
        "junit-xml==1.9",
    ],
    entry_points={
        "console_scripts": [
            "report2junit = report2junit:main",
        ],
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
