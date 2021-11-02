from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'Python controlled git'
LONG_DESCRIPTION = 'A package that allows to easy automation of git bash commands.'

# Setting up
setup(
    name="pygitinterface",
    version=VERSION,
    author="jocon15 (Jason O)",
    author_email="jaywoc12@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'git', 'git-bash',
              'git bash', 'commands', 'py'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
