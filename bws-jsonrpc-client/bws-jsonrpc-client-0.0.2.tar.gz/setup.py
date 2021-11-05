from setuptools import setup


setup(
    name='bws-jsonrpc-client',
    version="0.0.2",
    description='Bws JsonRpc Client',
    url='https://gitlab.com/jad21/bws-jsonrpc-client.git',
    author='Jose Angel Delgado',
    author_email='esojangel@gmail.com',
    license='BSD 2-clause',
    packages=[
        'bws_jsonrpc_client',
    ],
    install_requires=[ 
        "requests>=2.21.0",
    ],
    entry_points={'console_scripts': ['jsonrpc=bws_jsonrpc_client.cli:main']},
    classifiers=[
        # 'Programming Language :: Python == 3.6',
    ],
)
