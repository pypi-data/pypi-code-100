from setuptools import setup
# To use a consistent encoding
# python setup.py sdist bdist_wheel
# twine upload dist/*
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

requirements = [
    'pygame',
    'Box2D',
]

#setup_requirements = [
#    'pytest-runner',
#]

#test_requirements = [
#    'pytest',
#]


setup(
    name='wonder',
    version='0.1.0',
    description='Python Game Engine',
    long_description=long_description,
    long_description_content_type='text/x-rst',
#    long_description_content_type='text/plain',
    url='https://github.com/hebi-python-ninja/wonder',
    author='hebi-python-ninja',
    author_email='hebi@python-ninja.com',
#    packages=[
#        'wonder',
#    ],
    py_modules= [
        'wonder',
    ],
    license='MIT',
    zip_safe=False,
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    keywords= [
       'game',
       'pygame',
       'game engine',
       'unity',
       'box2d',
    ],
    #test_suite='tests',
    #tests_require=test_requirements,
    #setup_requires=setup_requirements,
)
