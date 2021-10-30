from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='revamp',
  version='1.0.0',
  description='Data pre-processing',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='',  
  author='Ajeet Rai',
  author_email='ajeetrai2293@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='data cleansing', 
  packages=find_packages(),
  install_requires=[''] 
)
