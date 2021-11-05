import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paseofyou",
    version="0.0.13",
    author="markstar",
    author_email="863630017@qq.com",
    description="A small spider",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paseofyou/myspider",
    project_urls={
        "Bug Tracker": "https://github.com/paseofyou/myspider/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'lxml',
        'requests'
    ]
)