import setuptools

entry_points = \
        {'console_scripts': ['test-cpj-filler = src.filler:main']}

setuptools.setup(
    name="test_cpj_filler",
    version="0.1.1",
    author="rishikaw",
    author_email="rishikaw@student.42tokyo.jp",
    description="",
    package_dir={'src/': 'src'},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points=entry_points,
)
