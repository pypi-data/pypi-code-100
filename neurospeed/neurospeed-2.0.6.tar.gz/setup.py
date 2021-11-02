from setuptools import setup, find_packages

setup(
   name='neurospeed',
   version='2.0.6',
   author='Eli Shamis',
   contact_email='oleg@neurobrave.com',
   packages=find_packages(),
   scripts=[],
   package_data={'neurospeed': ['config/*']},
   url='https://bitbucket.org/neurobrave/neurospeed_python_api',
   license='LICENSE.txt',
   description='NeuroSpeed Python API',
   install_requires=[
       "python-socketio[client]==5.3.0"
   ],
)

