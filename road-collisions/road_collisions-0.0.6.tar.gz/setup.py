from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = (
)

setup(
    name='road_collisions',
    version='0.0.6',
    python_requires='>=3.6',
    description='Road collision data and tooling',
    author='Robert Lucey',
    url='https://github.com/RobertLucey/road-collisions',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    package_data={
        'road_collisions': ['resources/ireland.json']
    },
    entry_points={
        'console_scripts': [
            'raw_cleaner = road_collisions.bin.raw_cleaner:main',
            'load_road_collisions = road_collisions.bin.load:main',
        ]
    }
)
