from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: Apache Software License',
  'Programming Language :: Python',
   'Programming Language :: Python :: 3 :: Only',
   'Programming Language :: Python :: 3.5',
   'Programming Language :: Python :: 3.6',
   'Programming Language :: Python :: 3.7',
   'Programming Language :: Python :: 3.8',
   'Programming Language :: Python :: 3.9',
   'Programming Language :: Python :: 3.10',
    'Topic :: Database',
    'Topic :: Education',
    'Topic :: Office/Business'
]
 
setup(
  name='unin',
  version='0.0.11',
  description='University North Package.',
  long_description_content_type='text/markdown',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(), 
  author='David Kundih',
  author_email='kundihdavid@gmail.com',
  url='http://github.com/dkundih/unin',
  license='Apache Software License', 
  classifiers=classifiers,
  keywords='data science, machine learning, data manipulation, artificial intelligence, AI',
  packages=find_packages(),
  install_requires=['']
  )