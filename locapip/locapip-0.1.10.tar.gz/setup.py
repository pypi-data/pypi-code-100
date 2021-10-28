import setuptools

from locapip import name, version

import os
from pathlib import Path

long_description = (Path(os.path.dirname(__file__)) / 'README.md').read_text('utf-8')

setuptools.setup(
    name=name,
    version=version,
    author='sjtu_6547',
    author_email='88172828@qq.com',
    description='C++ embedded Python microservices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/locapidio/locapip',
    keywords='protobuf grpcio grpcio-tools',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.proto'],
    },
    python_requires='>=3.7',
    install_requires=[
        'click>=8', 'grpcio-tools>=1.41.0', ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Framework :: AsyncIO',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
)
