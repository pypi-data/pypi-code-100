import setuptools
reqs = ['utils-s']
version = '2.0'

setuptools.setup(
    name='playerFramework',
    version=version,
    author="Sal Faris",
    description="A Bridge between Swift based players and Python",
    packages=setuptools.find_packages(),
    author_email='salmanfaris2005@hotmail.com',
    install_requires=reqs
)