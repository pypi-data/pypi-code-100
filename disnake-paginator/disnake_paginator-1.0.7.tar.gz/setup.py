import setuptools

readme_file = open("README.md", "r")
readme_data = readme_file.read()
readme_file.close()

setuptools.setup(
    name = 'disnake_paginator',
    packages = ['disnake_paginator'],
    version = '1.0.7',
    license = 'MIT',
    description = "This is a module that contains paginators for disnake",
    long_description = readme_data,
    long_description_content_type = 'text/markdown',
    author = "ErrorNoInternet",
    url = 'https://github.com/ErrorNoInternet/disnake-paginator',
    keywords = ["discord", "disnake", "paginator"],
    install_requires = [
        "disnake",
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

