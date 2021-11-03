v = '0.0.18'
projectName = 'datable'
from setuptools import setup, find_packages
import os
import platform
opersys = platform.system()
if opersys=='Darwin'or opersys=='Linux':
    pkgs=list(filter(lambda x: x[-2:] != '__',list(filter(lambda x: x[0:7] == projectName,list(filter(None, [x[0].replace('{}/'.format(os.getcwd()), '').replace('/','.') if '.git' not in x[0] else '' for x in os.walk('{}/'.format(os.getcwd()))]))))))
elif opersys=='Windows':
    pkgs=list(filter(lambda x: x[-2:] != '__',list(filter(lambda x: x[0:7] == projectName,list(filter(None, [x[0].replace('{}\\'.format(os.getcwd()), '').replace('\\','.') if '.git' not in x[0] else '' for x in os.walk('{}\\'.format(os.getcwd()))]))))))

setup(
    name=projectName,
    version=v,
    license='MIT',
    author="Ziplux LHS",
    author_email='ziplux.so@ziplux.so',
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    url='https://github.com/ZipluxLhs/datable',
    keywords='data',
    install_requires=[
           'pip',
	  'setuptools',
      'tk',
      'tksheet',
      'pywin32'
      ],

)