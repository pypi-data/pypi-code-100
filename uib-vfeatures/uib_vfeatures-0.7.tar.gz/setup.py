# coding=utf-8
from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='uib_vfeatures',
      version='0.7',
      description='Vision features of generalistic use',
      url='https://github.com/explainingAI/uib_vfeatures',
      author="Miquel Miró Nicolau, Bernat Galmés Rubert, Dr. Gabriel Moyà Alcover",
      author_email='miquelca32@gmail.com, bernat_galmes@hotmail.com, gabriel_moya@uib.es',
      license='MIT',
      packages=['uib_vfeatures'],
      keywords=['Features extraction', 'Machine Learning', 'Computer Vision'],
      install_requires=[
          'scikit-image',
          'opencv-python',
          'matplotlib',
          'scipy',
          'scikit-image',
          'numpy'
      ],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
