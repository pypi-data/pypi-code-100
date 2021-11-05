import setuptools

entry_points = \
        {'console_scripts': ['p21octmmr_filler = src.p21octmmr_filler:main']}

setuptools.setup(
    name="p21octmmr-filler",
    version="0.0.4",
    author="yyokoyam, myagyu, rishikaw",
    author_email="yyokoyam@student.42tokyo.jp, myagyu@student.42tokyo.jp, rishikaw@student.42tokyo.jp",
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
