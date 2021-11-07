from setuptools import setup, find_packages

setup(
    name="person-age",
    version="0.4.0",
    author="SDA",
    author_email="mail@mail.com",
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
