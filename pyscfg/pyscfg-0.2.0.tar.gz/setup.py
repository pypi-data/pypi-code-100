from setuptools import setup


name = "pyscfg"
version = "0.2.0"

# get list of requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# get README as long description
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=name,
    version=version,
    author="Christopher Mertens",
    author_email="suppetia@gmx.de",
    description="simple handling of user configuration",
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls={
                    "Github": "https://github.com/suppetia/pyscfg",
                 },
    packages=["pyscfg"],
    install_requires=requirements,
    python_requires=">=3.6.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
