import setuptools

INSTALL_REQUIREMENTS = ['numpy', 'torch', 'torchvision', 'tqdm']

setuptools.setup(
    description='AlgoGrad: Making algorithms differentiable',
    author='Felix Petersen',
    author_email='ads0361@felix-petersen.de',
    license='MIT License',
    version='0.0.0',
    name='algograd',
    packages=[],
    install_requires=INSTALL_REQUIREMENTS,
)
