from distutils.core import setup
setup(
  name = 'BraveWryCubase',
  packages = ['BraveWryCubase'],
  version = 'v0.0.1',
  license='cc-by-sa-4.0',
  description = 'A fast chess library for chess engines development including an interface to play games with easy, efficient and short controls and a simple piece-value evaluation',
  author = 'Albert Mateu Carrasco',
  author_email = 'albertmateucarrasco@gmail.com',
  url = 'https://github.com/Holger-Velisky/BraveWryCubase',
  download_url = 'https://github.com/Holger-Velisky/BraveWryCubase/archive/refs/tags/v0.0.1.tar.gz',    # I explain this later on
  keywords = ['CHESS', 'PYTHON', 'BOARD', 'GAMES', 'IA', 'ENGINE', 'MATEU', 'LICHESS', 'SOCKFISH', "ML"],
  install_requires=[
          'chess',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Natural Language :: English',
    'License :: Free for non-commercial use',
    'Operating System :: POSIX',
    'Operating System :: Microsoft',
    'Operating System :: MacOS',
    'Operating System :: OS Independent',
    'Topic :: Utilities',
    'Topic :: Games/Entertainment :: Board Games',
    'Topic :: Games/Entertainment :: Real Time Strategy',
    'Topic :: Games/Entertainment :: Turn Based Strategy',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
  ],
)