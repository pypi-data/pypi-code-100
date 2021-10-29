from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='acous',
    version='0.0.1',
    description='Acoustics computing package for Python',
    author='Wende Li',
    author_email='wendeli@outlook.com',
    url='https://github.com/wendeli/acous',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs')),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)