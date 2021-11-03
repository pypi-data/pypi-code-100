from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name = 'homage-to-the-square',
    packages=['homage'],
    description = 'runs an homage to the square a la josef albers',
    version = '1.1.0',
    author="Tal Noznisky",
    keyword="josef albers, bauhaus, homage to the square",
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/talnoznisky/homage-to-the-square',
    python_requires='>=3.0', # any python greater than 2.7
    entry_points='''
            [console_scripts]
            homage-to-the-square=homage.main:main
        ''',
)
