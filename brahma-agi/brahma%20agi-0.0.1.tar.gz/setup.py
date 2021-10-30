from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='brahma agi',
  version='0.0.1',
  description='A library for Artificial General Intelligence',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='DR.A.SANJAY',
  author_email='dr.sanjayanbu@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='AGI', 
  packages=find_packages(),
  install_requires=[''] 
)
