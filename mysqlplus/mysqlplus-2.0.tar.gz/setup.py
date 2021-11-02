from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    "Operating System :: Unix",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    'Programming Language :: Python :: 3'
]

setup(
    name='mysqlplus',
    version='2.0',
    description='A simple wrapper for the module mysql-connector-python.',
    long_description='A simple wrapper for the module mysql-connector-python.',
    url='https://github.com/anthony16t/mysqlplus',  
    author='anthony16t',
    author_email='info@anthony16t.com',
    license='MIT', 
    classifiers=classifiers,
    keywords=['mysql','database','sql'], 
    packages=find_packages(),
    install_requires=['mysql-connector-python'] 
)