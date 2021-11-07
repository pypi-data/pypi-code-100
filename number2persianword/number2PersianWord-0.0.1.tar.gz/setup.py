from setuptools import setup, find_packages

setup(
    name='number2PersianWord',
    version='0.0.1',
    description='A short summary about your package',
    Long_description=open('README').read() + '\n\n' + open('CHANGELOG').read(),
    url='',
    author='Alireza Esrafili',
    author_email='aesi1050@gmail.com',
    license='MIT',
    keywords='number2PersianWord',
    packages=find_packages(),
    install_requires=['']
)