import setuptools

INSTALL_REQUIREMENTS = ['numpy', 'torch', 'torchvision', 'tqdm']

setuptools.setup(
    description='AlgoVision: Learning with Algorithmic Supervision',
    author='Felix Petersen',
    author_email='ads0361@felix-petersen.de',
    license='MIT License',
    version='0.0.0',
    name='algovision',
    packages=[],
    install_requires=INSTALL_REQUIREMENTS,
)
