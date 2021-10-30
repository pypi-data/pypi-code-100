from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')
setup(
  name = 'mnl_punct_norm',  
  packages = ['mnl_punct_norm'], 
  version = '0.0.7', 
  license='apache-2.0',
  description = "Light-weight tool for removing punctuation. Supports multiple natural languages.",
  author = 'Rairye', 
  url = 'https://github.com/Rairye/mnl-punct-norm',   
  download_url = 'https://github.com/Rairye/mnl-punct-norm/archive/refs/tags/v0.0.7.tar.gz',
  keywords = ['punctuation', 'multi-language', 'normalization'],
  long_description=long_description,
  long_description_content_type='text/markdown',

  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License', 
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
