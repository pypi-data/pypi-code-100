from setuptools import setup, find_packages

setup(name="async_chat_client_geekbrains",
      version="0.0.2",
      description="mess_client",
      author="Polyakov",
      author_email="ae.polyakov@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
