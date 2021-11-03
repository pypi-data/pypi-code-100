from setuptools import setup, find_packages

setup(
    name='TSP-Framework',
    version='0.76',
    description='Framework para resolver el problema del vendedor viajero aplicando metaheristicas como Simulated Annealing y Genetic Algorithm',
    long_description=open('README.md').read(),
    author='Javier del Canto, Jorge Polanco',
    author_email='javier.delcanto.m@mail.pucv.cl, jorge.polanco.sanmartin@gmail.com',
    url='https://github.com/Javernaver/TSP-Framework',
    scripts=['TSPF/tspf.py'],
    packages=find_packages(),
    install_requires=['matplotlib'], 
    zip_safe=False,
    classifiers=[
        'License :: Freeware',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires = '>= 3.7',
    include_package_data=True,
    package_data={
        'TSPF': ['instances/*.tsp', 'log/*.csv'],
    }
)