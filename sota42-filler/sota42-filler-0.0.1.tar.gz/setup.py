import setuptools

entry_points = \
        {'console_scripts': ['sota42_filler = src.sota42_filler:main']}

setuptools.setup(
    name="sota42-filler",
    version="0.0.1",
    author="mnishimi, dhayakaw, toyoshid, rishikaw",
    author_email="mnishimi@student.42tokyo.jp, dhayakaw@student.42tokyo.jp, toyoshid@student.42tokyo.jp, rishikaw@student.42tokyo.jp",
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
