from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    "Operating System :: Unix",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    'Programming Language :: Python :: 3'
]

setup(
    name='twitterplus',
    version='2.0',
    description='A simple module to work with the twitter api.',
    long_description='A simple module to work with the twitter api.',
    url='https://github.com/anthony16t/twitterplus',  
    author='anthony16t',
    author_email='info@anthony16t.com',
    license='MIT', 
    classifiers=classifiers,
    keywords=['twitter','api','developer'], 
    packages=find_packages(),
    install_requires=['requests']
)