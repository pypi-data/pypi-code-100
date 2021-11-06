import os
from distutils.core import setup

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

# parse version from mjooln/__init__.py
_init_file = os.path.join(ROOT_PATH, "mjooln", "__init__.py")
with open(_init_file) as fi:
    vline = ''
    while '__version__' not in vline:
        vline = fi.readline()
VERSION = vline.strip().split(' = ')[1].replace('\'', '').replace('\"', '')

with open('README') as f:
    long_description = f.read()

setup(
    name='mjooln',
    packages=[
        'mjooln',
        'mjooln.experimental',
    ],
    version=VERSION,
    license='BSD-3-Clause',
    description='Environmentally Friendly File Handling',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vemund Halmø Aarstrand',
    author_email='vemundaa@gmail.com',
    url='https://mjooln.readthedocs.io/en/latest/',
    keywords=['json', 'path', 'file', 'folder', 'file handling',
              'encryption', 'compression', 'aes', 'gzip', 'uuid', 'utc',
              'md5 checksum', 'data science', 'data lake',
              'microservice'],
    install_requires=[
        'python-dateutil',
        'pytz',
        'simplejson',
        'psutil',
        'cryptography',
        'pyyaml',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'Topic :: Artistic Software',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        # 'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
