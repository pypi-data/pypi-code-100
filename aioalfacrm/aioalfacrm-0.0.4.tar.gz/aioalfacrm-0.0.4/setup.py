import setuptools

__version__ = '0.0.4'


def get_description():
    """
    Read full description from 'Readme.md'
    :return: desciprion
    """
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setuptools.setup(
    name='aioalfacrm',
    version=__version__,
    author='Stanislav Rush',
    license='MIT license',
    author_email='911rush@gmail.com',
    description='Is an asynchronous implementation for AlfaCRM API',
    long_description=get_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/stas12312/aioalfacrm',
    packages=['aioalfacrm'],
    classifiers=[
        'Framework :: AsyncIO',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
    install_requires=[
        'aiohttp>=3.7.2,<4.0.0',
        'Babel>=2.8.0',
        'certifi>=2020.6.20',
    ],
)
