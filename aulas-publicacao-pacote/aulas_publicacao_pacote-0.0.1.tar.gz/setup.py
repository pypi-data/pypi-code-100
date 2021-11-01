from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='aulas_publicacao_pacote',
    version='0.0.1',
    url='',
    license='MIT License',
    author='Marcos Vinicius Vasconcelos Gomes',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='marcossvinc@gmail.com',
    keywords='Pacote',
    description='Pacote python para exibir número de 1 a 9',
    packages=['aulas_publicacao_pacote'],
    install_requires=['numpy'],)