from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(name='NitroFE',
      version='0.0.4',
      url='https://github.com/NITRO-AI/NitroFE',
      author='Nitro-AI',
      author_email='nitro.ai.solutions@gmail.com',
      license='Apache License 2.0',
      packages=find_packages('NitroFE'),
      package_dir={'':'NitroFE'},
      zip_safe=True,
	description="NitroFE is a Python feature engineering engine which provides a variety of feature engineering modules designed to handle continous calcualtion.",
      long_description=long_description  ,
	long_description_content_type='text/markdown',
	  install_requires=[
		"pandas",
		"numpy",
		"scipy",
            "plotly"
		],
      )