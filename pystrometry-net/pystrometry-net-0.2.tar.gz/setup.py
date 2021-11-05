from setuptools import setup, find_packages


setup(
    name='pystrometry-net',
    version='0.2',
    license='MIT',
    author="Samuel Grund",
    author_email='samuel_grund@hotmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/samgrund/pystrometry-net',
    keywords='pystrometry',
    install_requires=[
          'astropy',
      ],

)