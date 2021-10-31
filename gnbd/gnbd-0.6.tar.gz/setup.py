from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='gnbd',
      version='0.6',
      description='Gaussian abd Binomial distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['gnbd'],
      author='Mateus Furquim Dev',
      author_email='mateus@mfurquim.dev',
      zip_safe=False,
      install_requires=['matplotlib>=3.4.3'])
