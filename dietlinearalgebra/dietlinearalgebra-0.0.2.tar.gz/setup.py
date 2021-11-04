from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='dietlinearalgebra',
  version='0.0.2',
  description='Fast and lightweight linear algebra library',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Sol Zilberman',
  author_email='sol.zilberman@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['algebra', 'linalg', 'linear algebra'], 
  packages=find_packages(),
  install_requires=[''] 
)