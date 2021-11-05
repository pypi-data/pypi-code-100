from setuptools import setup, find_packages

requirements = [l.strip() for l in open('requirements.txt').readlines()]
requirements.append('pytest')

setup(
    name='liveisstracker',
    url='https://gitlab.com/manojm18',
    version='0.0.2',
    author='Manoj Manivannan',
    author_email='manojm18@live.in',
    description='Sample Python Project build using Maven and CI/CD',
    packages=find_packages(),
    entry_points={
    'console_scripts': ['liveisstracker=liveisstracker.command_line:main'],
    },
    install_requires=requirements,
    include_package_data=True,
)

