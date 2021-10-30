#python setup.py sdist --formats=gztar,zip
from setuptools import setup, find_packages

setup(name='canivete',
      version='0.1',
      url='https://github.com/joilsouza/canivete',
      license='MIT',
      author='joilsouza',
      author_email='joilsouza@hotmail.com',
      description='bla bla bla',
      scripts=['menu.py'],
      packages=find_packages(),
      zip_safe=False)