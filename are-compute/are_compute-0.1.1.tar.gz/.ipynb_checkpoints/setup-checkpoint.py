from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='asre_compute',
  version='0.0.11',
  description='From a pandas dataframe, this program computes through A-learning the ARE or cognitive biais ASRE along their 95% confidence intervals.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='François Grolleau',
  author_email='francois.grolleau@aphp.fr',
  license='MIT', 
  classifiers=classifiers,
  keywords='', 
  packages=['asre_compute'],
  install_requires=[''] 
)