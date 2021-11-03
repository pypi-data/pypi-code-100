from setuptools import setup
setup(
    entry_points={
        'console_scripts': [
            'papertrack=papertrack.__main__:main',
    ],
},
)