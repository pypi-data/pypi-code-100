from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="console_alarm",
    version="1.0.3",
    description="A small alarm function for your console.",
    url="https://github.com/ruerob/console_alarm",
    author="Robert Rüdiger (ruerob)",
    author_email="info@ruerob.de",
    license="Unlicense License",
    packages=['console_alarm'],
    install_requires=['numpy',
                      'pygame'],
    entry_points={'console_scripts': [
        'console_alarm = console_alarm.command_line:main'
    ]},

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: Public Domain',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Desktop Environment'
    ],

    long_description_content_type='text/markdown',
    long_description=long_description

)