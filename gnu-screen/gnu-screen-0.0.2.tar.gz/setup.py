import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gnu-screen",
    version="0.0.2",
    author="Lucas Maillet",
    author_email="loucas.maillet.pro@gmail.com",
    description="GNU-Screen session module handler for NodeJs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LoucasMaillet/Lib-GNU-Screen/tree/main/Python",
    project_urls={
        "Bug Tracker": "https://github.com/LoucasMaillet/Lib-GNU-Screen/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    package_dir={"gnu_screen": "src"},
    packages=["gnu_screen"],
    python_requires=">=3",
)