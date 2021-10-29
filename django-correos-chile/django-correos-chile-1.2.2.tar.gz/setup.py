import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-correos-chile',
    version='1.2.2',
    packages=['correos_chile'],
    include_package_data=True,
    description='Django Correos Chile Integration',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Linets Development Team',
    author_email='dteam@linets.cl',
    url='https://gitlab.com/linets/ecommerce/oms/integrations/oms-correos-chile/',
    license='MIT',
    python_requires=">=3.7",
    install_requires=[
        'Django>=2',
        'zeep>=4.0.0',
        'WeasyPrint>=52.2',
        'python-barcode>=0.13.1'
    ]
)
