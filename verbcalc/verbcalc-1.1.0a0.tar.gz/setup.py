from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='verbcalc',
    version='v1.1.0-alpha',
    packages=['verbcalc', 'verbcalc.core', 'verbcalc.tests'],
    url='https://github.com/ErykPiasecki07/VerbCalc',
    project_urls={
        'Bug Tracker': 'https://github.com/ErykPiasecki07/VerbCalc/labels/bug',
        'Documentation': 'https://verbcalc.readthedocs.io'
    },
    license='BSD-3-Clause Licence',
    author='Eryk Piasecki',
    author_email='eryk.piasecki@outlook.com',
    description='VerbCalc is a Python library that allows to '
                'perform calculations based on human speech.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Topic :: Communications',
        'Operating System :: OS Independent',
    ],
    python_requires=">=3.6"
)
