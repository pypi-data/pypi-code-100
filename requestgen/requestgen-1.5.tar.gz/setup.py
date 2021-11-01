from setuptools import setup, find_packages

VERSION = '1.5'
DESCRIPTION = 'Converter package'
LONG_DESCRIPTION = 'This package can be used to generate the code to send http requests in several languages. It can also be used to convert ' \
                   'the code from curl to other languages'

REQUIREMENTS = []

setup(
    name="requestgen",
    version=VERSION,
    author="Prajwal Ramakrishna",
    url='https://github.com/prajwaldr9/requestgen',
    author_email="prajwaldr9@gmail.com",
    license='GNU GPL',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    entry_points={'console_scripts': [
        'convert = requestgen.converter:main',
    ], },
    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Internet",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
