from setuptools import setup, find_packages

setup(
    name="age_descriptor",
    version="0.1",
    author="SDA",
    author_email="maila@mail.com",
    packages=find_packages(),
    python_requires=">=3.8",
    description="Our first super useful library",
    install_requires=[
        "pylint==2.11.1"
    ],
    entry_points="""
    [console_scripts]
    person_descriptor=person_descriptor.runner:start_app
    """
)