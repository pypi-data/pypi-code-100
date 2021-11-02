from setuptools import setup


with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()


setup(
    name="type-annotations-generator",
    version="1.0",
    py_modules=["type_annotations_generator"],
    description="type-annotations-generator provides a function for generating type annotations for a object",
    long_description=description,
    long_description_content_type="text/markdown",
    author="JakobDev",
    author_email="jakobdev@gmx.de",
    url="https://gitlab.com/JakobDev/type-annotations-generator",
    python_requires=">=3.7",
    include_package_data=True,
    license="BSD",
    keywords=["JakobDev", "type", "annotations"],
    project_urls={
        "Bug Tracker": "https://gitlab.com/JakobDev/type-annotations-generator/-/issues"
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Environment :: Other Environment",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ]
)
