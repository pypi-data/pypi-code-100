from setuptools import setup,find_packages

setup(name='client_test',
      version='0.1',
      description='Client packet',
      packages=find_packages(),
      author_email='isp@mail.ru',
      author='Nikolai Nagornyi',
      install_requeres = ['PyQt5','sqlalchemy','pycruptodome','pycryptodomex']
      )
