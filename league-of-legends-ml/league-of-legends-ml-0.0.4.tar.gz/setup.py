import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'league-of-legends-ml',
    version = '0.0.4',
    author = 'Andrea Princic',
    author_email = 'princic.1837592@studenti.uniroma1.it',
    description = 'Tools for machine learning applied to League of Legends',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/Princic-1837592/league-of-legends-ml',
    packages = setuptools.find_packages(),
    python_requires = '>=3.7',
    install_requires = [
        'scikit-learn',
        'numpy'
    ],
    package_data = {
        '': ['*.pkl'],
    }
)
