from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='NoiseX',
    version='0.0.4',
    description='A python package for perlin noise, simplex noise and perlin worms.',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='somePythonProgrammer',
    author_email='leenagajbhiye1003@gmail.com',
    keywords=['Noise','Perlin','Worms','Simplex'],
    url='https://github.com/somePythonProgrammer/NoiseX',
    download_url='https://pypi.org/project/NoiseX/'
)

install_requires = [
    'vnoise',
    'opensimplex'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)