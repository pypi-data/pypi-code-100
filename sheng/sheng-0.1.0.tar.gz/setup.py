import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sheng",
    version="0.1.0",
    author="luojiahai",
    author_email="luo@jiahai.co",
    description="The Sheng programming language: A Chinese programming language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luojiahai/sheng",
    project_urls={
        "Bug Tracker": "https://github.com/luojiahai/sheng/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.9",
    entry_points = {
        'console_scripts': ['sheng=src.driver:main'],
    }
)
