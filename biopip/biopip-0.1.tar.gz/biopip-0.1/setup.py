from setuptools import setup, find_packages

package = 'biopip'
version = '0.1'

setup(name=package,
      version=version,
      description="biostrand bioinformatics pipelines",
      url='https://github.com/BioStrand/biopip',
      packages=find_packages(),
      install_requires=[
          'appdirs',
          'psutil',
          'jinja2',
          'requests',
          'pandas',
          'matplotlib',
          'docker',
          'gitpython',
          'boto3' # aws Python sdk
        ],
      zip_safe=False,
      entry_points={
        #'console_scripts': ['biopip=biopip.__main__:main']
        },
      include_package_data=True,
      package_data={
          #'biostrand': ['pipelines/templates/*.tmplt']
      }
)
