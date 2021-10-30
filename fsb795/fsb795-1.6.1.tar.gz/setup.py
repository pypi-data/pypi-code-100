import fsb795
from setuptools import setup, find_packages
setup(name='fsb795',
    version='1.6.1',
    py_modules=['fsb795'],
    description='Obtaining the attributes of a qualified certificate, defined by the Order of the FSB 795', 
    long_description='Obtaining the attributes of a qualified certificate, \n\tdefined by the Order of the Federal Security Service \n\tof the Russian Federation of December 27, 2011 No. 795 \n\t(editorial dated January 21, 2021)',
    packages=find_packages(),
    install_requires=[
	'pyasn1>=0.4.4', 'pyasn1-modules>=0.2.2', 'six'
    ],
    platforms=['any'],
    classifiers=[
	'Development Status :: 4 - Beta',
	'Intended Audience :: Developers',
	'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
	'Programming Language :: Python',
        'Programming Language :: Python :: 2',
	'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.5',
        'Natural Language :: Russian',
	],
    test_suite='test795',
    author='Vladimir Orlov', 
    author_email='vorlov@lissi.ru',
    url='https://pypi.org/project/fsb795/',
    license='MIT License')
