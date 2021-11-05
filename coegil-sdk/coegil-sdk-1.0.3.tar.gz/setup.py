from setuptools import setup, find_packages

setup(
    name='coegil-sdk',
    version='1.0.3',
    author="Mike Levine",
    author_email="mike@coegil.com",
    description="Coegil Python SDK",
    packages=find_packages(),
    include_package_data=True,
    url="https://coegil.com",
    python_requires='>=3.6',
    py_modules=[
        'CoegilSdk'
    ],
    install_requires=[
        'boto3',
        'requests'
    ]
)