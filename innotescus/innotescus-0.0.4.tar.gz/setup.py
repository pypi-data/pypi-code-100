from setuptools import setup, find_packages

setup(
    name="innotescus",
    version="0.0.4",
    author="Innotescus, LLC",
    author_email="support@innotescus.io",
    description="Innotescus API Client",
    long_description="Client library for innotescus.io",
    # entry_points={
    #     'console_scripts': [
    #         'innotescus=innotescus.cli:main',
    #     ]
    # },
    url="https://github.com/innotescus/Innotescus",
    packages=find_packages(),
    package_data={"": ["*.ini"]},
    include_package_data=True,
    install_requires= [
        "Authlib>=0.15.5",
        "grpcio==1.41.1",
        "grpc-interceptor==0.13.0",
        "google-api-python-client>=2.28.0",
    ]
)
