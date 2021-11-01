from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Financial and Insurance Industry',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='tradinghalts',
    version='0.04',
    description='Trading halt insights',
    long_description=open('README.txt').read(),
    url='',  
    author='Jovad Uribe',
    author_email='jovuribe@gmail.com',
    license='MIT', 
    classifiers=classifiers,
    keywords='trading', 
    packages=find_packages(),
    install_requires=['datetime', 'pandas', 'python-firebase', 'firebase', 'python_jwt', 'gcloud', 'sseclient', 'pycryptodome', 'requests_toolbelt'] 
)
