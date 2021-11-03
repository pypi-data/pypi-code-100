from setuptools import setup

setup(
  name='singgalang',
  version='0.3',
  url='https://github.com/aN4ksaL4y/hariansinggalang',
  author='Muhammad Al Fajri',
  author_email='fajrim228@gmail.com',
  description='Python script dengan tempo yang sesingkat-singkatnya.',
  install_requires=['bs4', 'requests', 'urwid'],
  packages=['singgalang'],
  scripts=['bin/singgalang'],
  zip_safe=False
)
