from setuptools import setup
#twine upload dist/* --repository-url https://test.pypi.org/legacy/
setup(
    name = 'matpack',
    version = '1.0.0',
    author = 'Thiarly Souza',
    author_email = 'Thiarly@ufrn.edu.br',
    packages = ['matpack'],
    description = "pacote de funções matemáticas únicas",
    license = "MIT",
    keywords = "matematica, funções"

)