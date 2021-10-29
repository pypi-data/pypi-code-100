import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="web-jelly",
    version="0.0.4",
    author="Jellyfish",
    author_email="hello@web-jelly.com",
    description="web-jelly.com python client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://web-jelly.com",
    project_urls={
        "Bug Tracker": "https://gitlab.com/hello590/jelly-python-client/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"jelly": "src"},
    packages=setuptools.find_packages(where="src", include=['jelly', 'paho-mqtt']),
    python_requires=">=3.6",
)