# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nr_datasets_metadata',
 'nr_datasets_metadata.datamodels',
 'nr_datasets_metadata.jsonschemas',
 'nr_datasets_metadata.jsonschemas.nr_datasets_metadata',
 'nr_datasets_metadata.mapping_includes',
 'nr_datasets_metadata.mapping_includes.v7',
 'nr_datasets_metadata.mappings',
 'nr_datasets_metadata.mappings.v7',
 'nr_datasets_metadata.marshmallow',
 'nr_datasets_metadata.marshmallow.subschemas']

package_data = \
{'': ['*']}

install_requires = \
['oarepo-rdm-records>=3.2.0,<4.0.0', 'oarepo>=3.3,<4.0']

entry_points = \
{'invenio_jsonschemas.schemas': ['nr_datasets_metadata = '
                                 'nr_datasets_metadata.jsonschemas'],
 'oarepo_mapping_includes': ['nr_datasets_metadata = '
                             'nr_datasets_metadata.mapping_includes'],
 'oarepo_model_builder.datamodels': ['nr_datasets_metadata = '
                                     'nr_datasets_metadata.datamodels']}

setup_kwargs = {
    'name': 'techlib-nr-datasets-metadata',
    'version': '3.1.5',
    'description': 'Czech National Repository datasets data model.',
    'long_description': '# nr-datasets-metadata\n\n[![Build Status](https://travis-ci.org/Narodni-repozitar/nr-datasets.svg?branch=master)](https://travis-ci.org/Narodni-repozitar/nr-datasets)\n[![Coverage Status](https://coveralls.io/repos/github/Narodni-repozitar/nr-datasets/badge.svg?branch=master)](https://coveralls.io/github/Narodni-repozitar/nr-datasets?branch=master)\n\n\nDisclaimer: The library is part of the Czech National Repository, and therefore the README is written in Czech.\nGeneral libraries extending [Invenio](https://github.com/inveniosoftware) are concentrated under the [Oarepo\n namespace](https://github.com/oarepo).\n\n  ## Instalace\n\n Nejedná se o samostatně funkční knihovnu, proto potřebuje běžící Invenio a závislosti Oarepo.\n Knihovna se instaluje ze zdroje.\n\n ```bash\ngit clone git@github.com:Narodni-repozitar/nr-datasets-metadata.git\ncd nr-datasets-metadata\npip install poetry\npoetry install\n```\n\nPro testování a/nebo samostané fungování knihovny je nutné instalovat tests z extras.\n\n```bash\npoetry install --extras tests\n```\n\n:warning: Pro instalaci se používá Manažer závilostí **Poetry** více infromací lze naleznout v\n[dokumentaci](https://python-poetry.org/docs/)\n\n## Účel\n\nKnihovna rozšiřuje [obecný metadatový model](https://github.com/Narodni-repozitar/nr-common)\no pole pro datasetové záznamy. Datasetům je přiřazen endpoint **/datasets**. Knihovna\nposkytuje API pro CRUD operace pod proxy **nr_datasets**.\n\n## Použití\n\nBude dopsáno.\n',
    'author': 'Miroslav Bauer',
    'author_email': 'Miroslav.Bauer@cesnet.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
