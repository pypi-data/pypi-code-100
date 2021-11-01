from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='are_compute',
  version='0.1',
  description='ARE-compute package from the Saint-Malo poster “Evaluating the Effect of Individualized Treatment Rules Using Observational Data.”',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='François Grolleau',
  author_email='francois.grolleau@aphp.fr',
  license='MIT', 
  classifiers=classifiers,
  keywords='', 
  packages=['are_compute'],
  install_requires=['tqdm'] 
)