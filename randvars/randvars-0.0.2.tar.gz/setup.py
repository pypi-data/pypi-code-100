from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='randvars',
    version='0.0.2',
    description='A library of random variate generation routines',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='John Goodman',
    author_email='john.goodman@gmail.com',
    keywords=['Random', 'Random Generator', 'Random Variates', 'Random Variables'],
    url='https://github.com/jgoodie/randomvariates',
    download_url='https://pypi.org/project/randvars/'
)

install_requires = [
    'numpy'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires, include_package_data=True)
