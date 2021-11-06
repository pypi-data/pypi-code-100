from setuptools import setup, find_packages
from distutils.extension import Extension
import numpy 

setup(name='bioconsertinc',
      version='1.0.0',
      description='BioConsert, c implementation',
      url='https://github.com/pierreandrieu/bioconsertinc',
      long_description='BioConsert algorithm, c implementation',
      author='Pierre Andrieu',
      author_email='pierre.andrieu@lilo.org',
      license='MIT',
      # packages=find_packages(include=['bioconsertc', 'bioconsertc.*']),
      ext_modules=[Extension("bioconsertinc", ["bioconsertinc.c"],
                  include_dirs=[numpy.get_include()])],
      python_requires='>=3',
      zip_safe=False,
      install_requires=['numpy>=1.13'],
      )

