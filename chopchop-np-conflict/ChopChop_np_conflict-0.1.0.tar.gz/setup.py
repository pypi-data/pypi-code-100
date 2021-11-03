from setuptools import find_packages, setup


setup(name='ChopChop_np_conflict',
      version='0.1.0',
      author='Karen Armenakyan',
      author_email='284567@niuitmo.ru',
      description='Data Analysis conflicting dependencies taks',
      packages=find_packages(),
      zip_safe=False,
      setup_requires=['numpy<=1.17.5'])
