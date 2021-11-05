from setuptools import setup, find_packages
from codecs import open

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cypackage',
    version='1.0',
    description='This is a console script that used to easily generate cython base on your package.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/aminor-z/cypackage',
    author='Aminor_z',
    author_email='aminor_z@qq.com',
    license='MIT',
    keywords='cython',
    packages=find_packages(),
    install_requires=['easycython','cython', 'numpy', 'begins'],
    entry_points={
        'console_scripts': [
            'cypackage=cypackage.cypackage:main.start',
        ],
    },
)
