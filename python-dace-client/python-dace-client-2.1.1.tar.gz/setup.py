import os
from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'dace', '__version__.py'), 'r') as f:
    exec(f.read(), about)
with open('README.md', 'r') as f:
    readme = f.read()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=['dace', 'dace.atmosphericSpectroscopy', 'dace.catalog', 'dace.cheops', 'dace.exoplanet', 'dace.imaging',
              'dace.lossy', 'dace.opacity', 'dace.opendata', 'dace.photometry', 'dace.population', 'dace.spectroscopy',
              'dace.sun', 'dace.target', 'dace.astrometry'],
    package_data={'dace': ['config.ini'], 'dace.atmosphericSpectroscopy': ['config.ini'],
                  'dace.catalog': ['config.ini'], 'dace.cheops': ['config.ini'],
                  'dace.exoplanet': ['config.ini'], 'dace.imaging': ['config.ini'], 'dace.lossy': ['config.ini'],
                  'dace.opacity': ['config.ini'], 'dace.opendata': ['config.ini'],
                  'dace.observation': ['config.ini'], 'dace.photometry': ['config.ini'],
                  'dace.population': ['config.ini'], 'dace.spectroscopy': ['config.ini'], 'dace.sun': ['config.ini'],
                  'dace.target': ['config.ini'], 'dace.astrometry': ['config.ini']},
    install_requires=[
        'requests >= 2.21.0',
        'astropy',
        'numpy',
        'pandas'
    ])
