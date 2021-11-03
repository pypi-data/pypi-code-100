import os
import setuptools

from version import __version__

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(THIS_DIR, 'README.md')) as readme:
    long_description = readme.read()

# Note: distutils will complain about the long_description_content_type. It does not cause any problems.
#  It is a known deficiency and will not be fixed.
setuptools.setup(
    name='sdvi-rally-token-auth',
    license='Proprietary',
    version=__version__,
    author='SDVI Corp',
    description='The Rally Token Auth Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(exclude=['test', 'test.*', 'conftest.py']),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    py_modules=['rally_token_auth.token_auth'],
    install_requires=['requests'],
    package_data={'': ['LICENSE', 'README.md', 'RELEASE']},
)
