from setuptools import setup, find_packages

setup(name="demo_server",
      version="0.1.0",
      description="chat_server",
      author="Mr.Windmark",
      author_email="agentstorm@ya.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )