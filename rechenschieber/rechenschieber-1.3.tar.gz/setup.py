from setuptools import setup, find_packages

classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
]

setup(
    name = 'rechenschieber',
    version = '1.3',
    description = "It's a calculator.",
    url='',
    author="Jonas Greis",
    author_email="el-toro-loco@outlook.de",
    licence="MIT",
    classifiers=classifiers,
    keywords="Taschenrechner",
    packages=find_packages(),
    install_requires=['']
)