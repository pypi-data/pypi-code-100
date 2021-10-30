from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='geography',
    version='0.0.1',
    description='Get info about countries and states',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='FrenchFries8854',
    author_email='frenchfries8854@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='geography',
    packages=find_packages(),
    install_requires=['']
)
