from setuptools import find_packages, setup

with open("requirements.txt",'r+') as f:
    lines = f.readlines()

requirements = [str(x).strip() for x in lines]

print(requirements)


setup(
    name='rltrade_test',
    packages=find_packages(),
    version='0.0.11',
    description="Easy to use Reinforcement Library for finance",
    install_requires=requirements
)