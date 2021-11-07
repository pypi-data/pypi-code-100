from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='snutshell',
  version='1.2',
  description='create xlsx and dat file from python list, tuple, dictionary, numpy array',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='arn',
  author_email='naziul.arnab@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='simulation',
  packages=find_packages(),
  install_requires=['numpy','XlsxWriter']
)
