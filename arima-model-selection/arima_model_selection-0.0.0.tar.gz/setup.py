from setuptools import setup
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='arima_model_selection',
  version='0.0.0',
  description='AUTOCALCULATE P,q,R',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='MAINAK RAY',
  author_email='mainakr748@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='ARIMA', 
  packages=['arima_model_selection'],
  install_requires=['sklearn','statsmodels','numpy'] 
  )