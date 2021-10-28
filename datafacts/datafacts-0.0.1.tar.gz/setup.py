from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

with open('LICENSE', 'r') as f:
    license = f.read()

setup(
    name='datafacts',
    version='0.0.1',
    description='Quickly generate an image with population-level facts about your dataset',
    long_description=long_description,
    license=license,
    author='Eric Yates',
    author_email='eric@medleyagency.com',
    url='https://github.com/MedleyLabs/datafacts',
    packages=['datafacts'],
)
