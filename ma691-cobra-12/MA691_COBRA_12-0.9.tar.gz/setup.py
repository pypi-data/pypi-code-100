from distutils.core import setup
setup(
  name = 'MA691_COBRA_12',         # How you named your package folder (MyLib)
  packages = ['MA691_COBRA_12'],   # Chose the same as "name"
  version = '0.9',      # Start with a small number and increase it with every change you make
  license='AFL',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Regressions on Boston dataset',   # Give a short description about your library
  author = 'Sristy',                   # Type in your name
  author_email = 'sristy.sharma98@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/beertocode/MA691_COBRA_12',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/beertocode/MA691_COBRA_12/archive/refs/tags/0.9.tar.gz',    # I explain this later on
  keywords = ['Cobra', 'Ridge', 'Lasso','KNN','Kernel Cobra','MLR'],   # Keywords that define your package best
  install_requires=[           
          'numpy',
          'pandas',
          'sklearn',
          'matplotlib',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Academic Free License (AFL)',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)