from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mCSSMapi',
    version='0.2',
    author='Michael Mikulic',
    author_email='',
    description='The mcssmapi library providing access to Cisco Smart Account licensing API with python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mmikulic212/mcssmapi",
    project_urls={
        "Bug Tracker": "https://github.com/mmikulic212/mcssmapi/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)
