from setuptools import setup

setup(name='pyaem3',
      version='0.0.1',
      description='Python API for AEM',
      py_modules=["pyaem3"],
      packages_src={'': 'src'},
      classifiers=[
              "Development Status :: 1 - Planning",
              "Intended Audience :: Developers",
              "Programming Language :: Python :: 3.8",
              "Operating System :: Unix",
              "Operating System :: MacOS :: MacOS X",
              "Operating System :: Microsoft :: Windows",
          ]
      )
