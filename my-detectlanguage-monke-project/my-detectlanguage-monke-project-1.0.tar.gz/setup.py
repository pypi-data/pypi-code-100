from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='my-detectlanguage-monke-project',
  version='1.0',
  description='Detect Languages (WIP)',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Phuc ANH',
  author_email='phucanhle06@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='detect lang', 
  packages=find_packages(),
  install_requires=[''] 
)