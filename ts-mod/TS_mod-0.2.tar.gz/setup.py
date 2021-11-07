from setuptools import setup
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='TS_mod',
  version='0.2',
  description='AUTOCALCULATE ARIMA MODEL',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='MAINAK RAY',
  author_email='mainakr748@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='ARIMA', 
  packages=['TS_mod'],
  install_requires=['sklearn','statsmodels','numpy'] 
  )
