import os
import os.path

from setuptools import find_packages
from setuptools import setup


def readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        return f.read()

# Set __version__
exec(open('goenrichment/__init__.py').read())

setup(
    name='goenrichment',
    packages=find_packages(),
    data_files=[('', ['README.rst'])],
    use_scm_version=True,
    setup_requires=['wheel', 'setuptools_scm'],
    description='GO enrichment analysis from a list of gene names using a precomputed database',
    long_description=readme(),
    long_description_content_type='text/markdown',
    license='Public Domain',
    author='Vera Alvarez, Roberto',
    author_email='veraalva' '@' 'ncbi.nlm.nih.gov',
    maintainer='Vera Alvarez, Roberto',
    maintainer_email='veraalva' '@' 'ncbi.nlm.nih.gov',
    url='https://gitlab.com/r78v10a07/goenrichment',
    install_requires=['numpy',
                      'scipy',
                      'statsmodels',
                      'pandas',
                      'networkx'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Jupyter',
        'Intended Audience :: Science/Research',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    keywords='Jupyter NGS',
    project_urls={
        'Documentation': 'https://gitlab.com/r78v10a07/goenrichment/issues',
        'Source': 'https://gitlab.com/r78v10a07/goenrichment',
        'Tracker': 'https://gitlab.com/r78v10a07/goenrichment/issues',
    },
    entry_points={
        'console_scripts': [
            'goenrich = goenrichment.goenrich:main',
            'goenrich_createdb = goenrichment.goenrichDB:main'
        ],
    }
)
