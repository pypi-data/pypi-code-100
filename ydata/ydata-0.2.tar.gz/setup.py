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
    name='ydata',
    version='0.2',
    description='Download stock symbol historical data from yahoo finance.',
    long_description='Download stock symbol historical data from yahoo finance in a json format (dictionary) beginners friendly.',
    url='https://github.com/anthony16t/ydata',  
    author='anthony16t',
    author_email='info@anthony16t.com',
    license='MIT', 
    classifiers=classifiers,
    keywords=['stock','finance','market'], 
    packages=find_packages(),
    install_requires=['requests','python-dateutil']
)