from setuptools import setup

setup(
    name='package_sh_pkg',
    version='0.0.1',
    description='A example Python package',
    url='https://github.com/mshimanskaya',
    author='Shimanskaya Margarita',
    author_email='mshimanskaya@mail.ru',
    license='BSD 2-clause',
    packages=['package_sh'],
    python_requires='>=3.6',
    install_requires=['numpy<1.17.3'],
)