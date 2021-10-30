from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='nebulatest',
      version='1.0.2',
      description='A small example package',
      long_description=long_description,
      author='xiaowuhu',
      author_email='hu.xiaowu@hotmail.com',
      url='https://www.msra.cn/zh-cn/news/outreach-articles/%E6%96%B0%E4%B9%A6%E5%8F%91%E5%B8%83%EF%BC%81%E3%80%8A%E6%99%BA%E8%83%BD%E4%B9%8B%E9%97%A8%E3%80%8B%E5%B8%A6%E4%BD%A0%E4%B8%80%E7%AA%A5-ai-%E4%B8%96%E7%95%8C',
      install_requires=[],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
