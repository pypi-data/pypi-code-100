from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'geopandas',
    'unidecode',
    'sparse_dot_topn',
    'dash',
    'pandas', 
    'plotly',
    'geopy==2.2.0', 
    'sklearn',
    'numpy',
    'scipy',
    'matplotlib',
    'requests' 


]


setup(
    name='terralabgeoapi',
    packages=find_packages(exclude=["*test*"]),
    version='0.0.5',
    description='GeoAPI do TerraLab',
    author='TerraLab',
    author_email='alan.ufop@gmail.com',
    url = 'https://gitlab.com/ufopterralab/data-analytics-group/geoapi.git',
    install_requires= INSTALL_REQUIRES,
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    package_data = {"GeoAPI": ['Data/*.csv', 'Data/*.xls'] },
)