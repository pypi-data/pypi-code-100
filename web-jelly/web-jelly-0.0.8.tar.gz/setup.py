import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="web-jelly",
    version="0.0.8",
    author="Jellyfish",
    author_email="hello@web-jelly.com",
    description="web-jelly.com python client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://web-jelly.com",
    project_urls={
        #'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
        "Bug Tracker": "https://gitlab.com/hello590/jelly-python-client/-/issues",
        #'Funding': 'https://donate.pypi.org',
        #'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://gitlab.com/hello590/jelly-python-client'
        #'Tracker': 'https://github.com/pypa/sampleproject/issues',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'paho-mqtt'
    ],
    python_requires=">=3.6",
)