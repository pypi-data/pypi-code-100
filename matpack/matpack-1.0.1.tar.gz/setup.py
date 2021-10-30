from setuptools import setup
#twine upload dist/* --repository-url https://test.pypi.org/legacy/
setup(
    name = 'matpack',
    version = '1.0.1',
    author = 'Thiarly Souza',
    author_email = 'Thiarly@ufrn.edu.br',
    packages = ['dismat'],
    description = "pacote de funções matemáticas únicas",
    long_description = "matpack é um pacote de funções matemáticas únicas desenvolvidas para facilitar a abordagem de diversos contextos",
    license = "MIT",
    keywords = "matematica, funções"

)