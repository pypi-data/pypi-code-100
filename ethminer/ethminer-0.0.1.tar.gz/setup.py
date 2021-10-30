from setuptools import setup 

setup(
    name = 'ethminer',
    version = '0.0.1',
    description= 'Ethereum Miner for Python',
    py_modules = ['ether_scan', 'scripting', 'beta', 'web3', 'hashlib'],
    package_dir = {'': 'src'},
)