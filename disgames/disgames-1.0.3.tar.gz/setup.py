from setuptools import setup, find_packages

def readme():
    with open("README.md") as f:
        r = f.read()
    return r

setup(
    name="disgames",
    version="1.0.3",
    description="A games module that can be used to instantly add games to your discord bot",
    long_description=readme(),
    author="andrew",
    maintainer="Marcus",
    url="https://github.com/andrewthederp/Disgames",
    license="Apache",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=["discord.py","aiohttp"],
    python_requires='>=3.6',
    packages=find_packages(include=['disgames', 'disgames.*']),
)
