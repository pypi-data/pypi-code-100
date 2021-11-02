VERSION = '1.0.1'

from setuptools import (
    setup,
)

setup(
    name='minio_sdk',
    version=VERSION,
    author='Jucheng Mo',
    author_email='mojucheng@bytedance.com',
    description='python sdk for minio',
    packages=[
        'minio_sdk',
    ],
    scripts=[
    ],
    package_data={
    },
    install_requires=[
        'minio'
    ],
)