from setuptools import setup, find_packages

setup(
    name='demand_sigmoid',
    version='0.1.5',
    packages=find_packages(),
    install_requires = ['pandas', 'numpy', 'catboost']
)


