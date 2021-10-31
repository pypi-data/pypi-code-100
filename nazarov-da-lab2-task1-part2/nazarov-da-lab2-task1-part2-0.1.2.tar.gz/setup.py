from setuptools import setup

setup(
    name='nazarov-da-lab2-task1-part2',
    version='0.1.2',
    description='Lagrange interpolation',
    url='https://github.com/geranazavr555',
    author='Georgiy Nazarov',
    author_email='geranazavr555@yandex.ru',
    license='BSD 2-clause',
    packages=['interpolation'],
    install_requires=['numpy==1.21.0',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.9',
    ],
)