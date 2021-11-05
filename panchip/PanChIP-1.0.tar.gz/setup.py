from distutils.core import setup
setup(
  name = 'PanChIP',
  packages = ['PanChIP'],
  version = '1.0',
  license='MIT',
  description = 'Pan-ChIP-seq Analysis of Peak Sets',
  author = 'Hanjun Lee',
  author_email = 'hanjun@mit.edu',
  url = 'https://github.com/hanjunlee21/PanChIP',
  download_url = 'https://github.com/hanjunlee21/PanChIP/archive/refs/tags/v.1.0.tar.gz',
  keywords = ['chip-seq', 'bedfile'],   
  install_requires=[            
          'subprocess',
          'gdown',
          'argparse',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Science/Research',      
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.0',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Awk',
    'Programming Language :: Unix Shell',
  ],
)
