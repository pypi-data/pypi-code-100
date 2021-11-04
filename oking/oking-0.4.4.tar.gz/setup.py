from setuptools import setup, find_packages
from os import path


def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()


setup(
    name="oking",
    version='0.4.4',
    author="Openk Tecnologia",
    author_email="<suporte.b2c@openk.com.br>",
    description='Pacote de integração de produtos, preço, estoque e pedidos com o sistema OkVendas da Openk',
    long_description_content_type="text/markdown",
    long_description=read('README.md'),
    packages=find_packages(include=['src', 'src.*']),
    install_requires=['mysql-connector-python',
                      'schedule',
                      'requests',
                      'configparser',
                      'logger',
                      'cx-Oracle',
                      'jsonpickle'],
    keywords=['python', 'oking', 'openk', 'okvendas', 'ok'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        'console_scripts': ['oking=src.__main__:main']
    }
)
