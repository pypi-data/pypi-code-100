from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

# data_files = [str(x) for x in pathlib.Path(here / 'data').glob('*.tif')]

setup(
    name='RRaster', 
    version='0.0.3',
    description='Rasterio function wrappers for simple raster processing in Python that mimics the R Raster syntax.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/colinbrust/RRaster',
    author='Colin Brust',
    author_email='colin.brust@gmail.com',
    keywords='raster, rasterio, R, simplified',
    packages=['rraster'],
    package_dir={'rraster': 'src/rraster'},
    package_data={'rraster': ['data/*.tif']},
    python_requires='>=3.6, <4',
    install_requires=['rasterio', 'numpy', 'matplotlib', 'geopandas'],  # Optional
    # extras_require={  # Optional
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={  # Optional
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
)
