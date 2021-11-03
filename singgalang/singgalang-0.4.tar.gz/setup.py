from setuptools import setup

readme = open('README.md').read()
setup(
  name='singgalang',
  version='0.4',
  url='https://github.com/aN4ksaL4y/hariansinggalang',
  author='Muhammad Al Fajri',
  author_email='fajrim228@gmail.com',
  description='Python script dengan tempo yang sesingkat-singkatnya.',
  long_description=readme,
  long_description_content_type='text/markdown',
  install_requires=['bs4', 'requests', 'urwid'],
  packages=['singgalang'],
  scripts=['bin/singgalang'],
  zip_safe=False
)
