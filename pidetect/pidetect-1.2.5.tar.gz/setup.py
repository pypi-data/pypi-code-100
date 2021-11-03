import setuptools

setuptools.setup(
    name="pidetect",
    version="1.2.5",
    description="python image detect lib",
    packages=['pidetect'],
    package_data={'pidetect': ['so/*']},
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)

