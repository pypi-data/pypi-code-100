from setuptools import find_packages, setup


def find_required():
    with open("requirements.txt") as f:
        return f.read().splitlines()


def find_dev_required():
    with open("requirements-dev.txt") as f:
        return f.read().splitlines()


setup(
    name="district42-exp-types",
    version="0.6.0",
    description="district42 experimental types",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nikita Tsvetkov",
    author_email="nikitanovosibirsk@yandex.com",
    python_requires=">=3.8",
    url="https://github.com/nikitanovosibirsk/district42-exp-types",
    license="Apache-2.0",
    packages=find_packages(exclude=("tests",)),
    package_data={"district42_exp_types": ["py.typed"]},
    install_requires=find_required(),
    tests_require=find_dev_required(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
        "Typing :: Typed",
    ],
)
