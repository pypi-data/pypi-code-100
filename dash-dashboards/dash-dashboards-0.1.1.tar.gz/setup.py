import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()


setuptools.setup(
    name="dash-dashboards",
    version="0.1.1",
    author="Filip Beć",
    description="Packakge to build Dash applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="TODO",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
    include_package_data=True,
    package_dir={"": "src"},
    packages=setuptools.find_namespace_packages(where="src"),
    install_requires=[
        "click",
        "dash-bootstrap-components",
    ],
    extras_require={
        "tests": [
            "isort[colors]",
            "pytest",
            "pytest-cov",
            "pytest-env",
            "flake8",
            "black",
            "tox",
        ],
    },
    entry_points={
        "console_scripts": ["dash-admin = dash_dashboards.__main__:cli"],
    },
)
