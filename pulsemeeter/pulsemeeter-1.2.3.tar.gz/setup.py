import os
import sys
import pathlib
from setuptools import setup
try:
    import pulsemeeter
except ImportError:
    print("error: pulsemeeter requires Python 3.5 or greater")
    sys.exit(1)

VERSION = pulsemeeter.__version__
ORIG_CONFIG_DIR = pulsemeeter.ORIG_CONFIG_DIR
README = (pathlib.Path(__file__).parent / "README.md").read_text()

data_files = [
    ('share/licenses/pulsemeeter/', ['LICENSE']),
    (ORIG_CONFIG_DIR[1:], ['pulsemeeter/config.json']),
]

for directory, _, filenames in os.walk(u'share'):
    dest = directory[6:]
    if filenames:
        files = [os.path.join(directory, filename) for filename in filenames]
        data_files.append((os.path.join('share', dest), files))

setup(
    name='pulsemeeter',
    version=VERSION,
    description='A pulseaudio audio routing application',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Gabriel Carneiro',
    author_email='therealcarneiro@gmail.com',
    license="MIT",
    license_files='LICENSE',
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
    ],
    url='https://github.com/theRealCarneiro/pulsemeeter',
    packages=['pulsemeeter'],
    install_requires=['pygobject', 'appdirs'],
    data_files=data_files,
    entry_points={
        "console_scripts": [
            "pulsemeeter = pulsemeeter.__main__:main",
        ],
    },

    python_requires=">=3.5",
    scripts=[
        'scripts/pmctl',
    ],
    include_package_data=True
)
