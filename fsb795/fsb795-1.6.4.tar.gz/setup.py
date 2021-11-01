import fsb795
from setuptools import setup, find_packages
setup(name='fsb795',
    version='1.6.4',
    py_modules=['fsb795'],
    description='Получение атрибутов квалифицированного сертификата, созданного в соответствии с требованиями Приказа ФСБ РФ N 795', 
    long_description='Получение атрибутов квалифицированного сертификата, \n\tсозданного в соответствии с требованиями Приказа ФСБ РФ N 795 \n\tот декабря 2011 года\n\t(в редакции от 21 января 2021 года)',
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
