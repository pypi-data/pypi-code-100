from glob import glob
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

with open('LICENSE', 'r') as f:
    license_file = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setup(
    name='datafacts',
    version='0.0.10',
    description='Quickly generate an image with population-level facts about your dataset',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=license_file,
    author='Eric Yates',
    author_email='eric@medleyagency.com',
    url='https://github.com/MedleyLabs/datafacts',
    packages=['datafacts'],
    install_requires=[req for req in requirements if not req.startswith('#')],
    include_package_data=True
)
