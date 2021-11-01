# coding: utf-8

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
	
setuptools.setup(
    name="django_rest_admin",
    version="0.0.9",
    author="jiangshan00000",
    author_email="710806594@qq.com",
    description="django app for Adding table CRUD rest api with admin ui and without coding.",
	long_description=long_description,
	long_description_content_type = "text/markdown",
    url="https://github.com/Jiangshan00001/django_rest_admin",
    packages=setuptools.find_packages(),
    include_package_data=True,

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	install_requires=[
    'django',
    'django-filter',
	'djangorestframework',
	],
)