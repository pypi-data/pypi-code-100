# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['adze_modeler',
 'adze_modeler.platforms',
 'adze_modeler.resources.model_template']

package_data = \
{'': ['*'],
 'adze_modeler': ['resources/doc_template/*',
                  'resources/doc_template/docs/*',
                  'resources/doc_template/docs/images/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'aiofiles>=0.7.0,<0.8.0',
 'ezdxf>=0.16.5,<0.17.0',
 'fastapi>=0.70,<0.71',
 'gitlint',
 'gmsh>=4.8.4,<5.0.0',
 'importlib-resources>=5.4.0,<6.0.0',
 'mkdocs-git-revision-date-plugin>=0.3.1,<0.4.0',
 'mkdocs-material>=7.3.6,<8.0.0',
 'mkdocs>=1.2.3,<2.0.0',
 'mkdocstrings>=0.16.2,<0.17.0',
 'networkx>=2.6.3,<3.0.0',
 'numpy>=1.21.0,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pygmsh>=7.1.13,<8.0.0',
 'pyvista>=0.32.1,<0.33.0',
 'scipy>=1.7.0,<2.0.0',
 'svgpathtools>=1.4.2,<2.0.0',
 'uvicorn>=0.15.0,<0.16.0',
 'vedo>=2021,<2022']

setup_kwargs = {
    'name': 'adze-modeler',
    'version': '0.0.1',
    'description': 'Creates an encapsulated FEM simulation',
    'long_description': None,
    'author': 'Tamas Orosz',
    'author_email': 'orosz.tamas@montana.hu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
