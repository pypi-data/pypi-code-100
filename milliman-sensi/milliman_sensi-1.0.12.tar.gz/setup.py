from setuptools import setup
import os


# specify requirements of your package here
REQUIREMENTS = ['pandas', 'objectpath']

# some more details
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    ]

# calling the setup function
setup(name='milliman_sensi',
      # version=os.getenv('VERSION_TAG'), # Needs to be %VERSION_TAG% on Windows CMD
      version="1.0.12",
      description='A parser and modifier of the configuration in Milliman-CHESS',
      long_description="""A parser and modifier of CHESS's configuration
To parse configuration files and apply them to create new sensitivity tables""",
      url='https://dev.azure.com/millimanparis/CHESS-Sensitivity-Manager',
      author='Quincy HSIEH',
      author_email='quincy.hsieh@milliman.com',
      license='MIT',
      packages=['milliman_sensi'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='Milliman CHESS, configuration, parsers, sensitibity'
      )
