from setuptools import setup,find_packages

setup(name='server_test_new',
      version='0.2',
      description='Server packet',
      packages=find_packages(),
      author_email='isp@mail.ru',
      author='Nikolai Nagornyi',
      install_requeres = ['PyQt5','sqlalchemy','pycruptodome','pycryptodomex']
      )



