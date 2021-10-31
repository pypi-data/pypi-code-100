# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kaskade',
 'kaskade.kafka',
 'kaskade.renderables',
 'kaskade.utils',
 'kaskade.widgets']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.1,<9.0.0',
 'confluent-kafka>=1.7.0,<2.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'rich>=10.9.0,<11.0.0',
 'textual>=0.1.12,<0.2.0',
 'typing-extensions>=3.10.0,<4.0.0']

entry_points = \
{'console_scripts': ['kaskade = kaskade.app:main', 'kskd = kaskade.app:main']}

setup_kwargs = {
    'name': 'kaskade',
    'version': '0.2.9',
    'description': 'kaskade is a terminal user interface for kafka',
    'long_description': '<p align="center">\n<a href="https://github.com/sauljabin/kaskade"><img alt="kaskade" src="https://raw.githubusercontent.com/sauljabin/kaskade/main/screenshots/banner.png"></a>\n</p>\n\n<a href="https://github.com"><img alt="GitHub" src="https://img.shields.io/badge/-github-0da5e0?logo=github&logoColor=white"></a>\n<a href="https://github.com/sauljabin/kaskade"><img alt="GitHub" src="https://img.shields.io/badge/status-wip-orange"></a>\n<a href="https://github.com/sauljabin/kaskade"><img alt="GitHub" src="https://badges.pufler.dev/updated/sauljabin/kaskade?label=updated"></a>\n<a href="https://github.com/sauljabin/kaskade/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/github/license/sauljabin/kaskade"></a>\n<a href="https://github.com/sauljabin/kaskade/actions"><img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/sauljabin/kaskade/CI?label=tests"></a>\n<a href="https://app.codecov.io/gh/sauljabin/kaskade"><img alt="Codecov" src="https://img.shields.io/codecov/c/github/sauljabin/kaskade"></a>\n<br>\n<a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/-python-brightgreen?logo=python&logoColor=white"></a>\n<a href="https://pypi.org/project/kaskade"><img alt="Version" src="https://img.shields.io/pypi/v/kaskade"></a>\n<a href="https://pypi.org/project/kaskade"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/kaskade"></a>\n<a href="https://libraries.io/pypi/kaskade"><img alt="Dependencies" src="https://img.shields.io/librariesio/release/pypi/kaskade"></a>\n<a href="https://pypi.org/project/kaskade"><img alt="Platform" src="https://img.shields.io/badge/platform-linux%20%7C%20osx-0da5e0"></a>\n<br>\n<a href="https://kafka.apache.org/"><img alt="Kafka" src="https://img.shields.io/badge/-kafka-e3e3e3?logo=apache-kafka&logoColor=202020"></a>\n<a href="https://kafka.apache.org/"><img alt="Kafka" src="https://img.shields.io/badge/kafka-2.8%20%7C%203.0-blue"/></a>\n<a href="https://pypi.org/project/confluent-kafka/"><img alt="Kafka Client" src="https://img.shields.io/pypi/v/confluent-kafka?label=kafka%20client"></a>\n<br>\n<a href="https://www.docker.com/"><img alt="Docker" src="https://img.shields.io/badge/-docker-blue?logo=docker&logoColor=white"></a>\n<a href="https://hub.docker.com/r/sauljabin/kaskade"><img alt="Docker Image Version (latest by date)" src="https://img.shields.io/docker/v/sauljabin/kaskade?label=tag"></a>\n<a href="https://hub.docker.com/r/sauljabin/kaskade"><img alt="Docker Image Size (latest by date)" src="https://img.shields.io/docker/image-size/sauljabin/kaskade"></a>\n\n**kaskade** is a tui (text user interface) for [kafka](https://kafka.apache.org/). \n:rocket: This project is powered by [textual](https://github.com/willmcgugan/textual) and [rich](https://github.com/willmcgugan/rich)!. \n\nFor a local kafka environment go to https://github.com/sauljabin/kafka-docker.\n\n> :construction: This project is currently a work in progress, but usable by early adopters. \n\n# Table of Contents\n\n* [Installation and Usage](#installation-and-usage)\n* [Running with Docker](#running-with-docker)\n* [Configuration](#configuration)\n* [Screenshots](#screenshots)\n* [Alternatives](#alternatives)\n* [To Do](#to-do)\n* [Development](#development)\n  * [Scripts](#scripts)\n  * [Docker](#docker)\n  * [Bumping Version](#bumping-version)\n\n# Installation and Usage\n\nInstall with pip:\n\n```sh\npip install kaskade\n```\n\n> `pip` will install `kaskade` and `kskd` aliases.\n\nUpgrade with pip:\n\n```sh\npip install --upgrade kaskade\n```\n\nHelp:\n\n```sh\nkaskade --help\n```\n\nVersion:\n\n```sh\nkaskade --version\n```\n\nRun without config file (it\'ll take any of `kaskade.yml`, `kaskade.yaml`, `config.yml` or `config.yaml`):\n\n```sh\nkaskade\n```\n\nRun with config file:\n\n```sh\nkaskade my-file.yml\n```\n\n# Running with Docker\n\nUsing docker (remember to set a `network` and `volume`):\n\n```sh\ndocker run --rm -it --network kafka \\\n--volume $(pwd):/kaskade \\\nsauljabin/kaskade:latest\n```\n\nAliases:\n\n```sh\nalias kaskade=\'docker run --rm -it --network kafka \\\n--volume $(pwd):/kaskade \\\nsauljabin/kaskade:latest\'\n\nalias kskd=kaskade\n```\n\n> These aliases will mount the current directory as a volume.\n\n# Configuration\n\nA default [yaml](https://yaml.org/spec/1.2/spec.html) configuration file name can be either `kaskade.yml`\n, `kaskade.yaml`, `config.yml` or `config.yaml`. It supports all the configuration\non [kafka consumer configuration](https://kafka.apache.org/documentation/#consumerconfigs) page.\n\nSimple connection example:\n\n```yml\nkafka:\n  bootstrap.servers: localhost:9093\n```\n\nSSL encryption example:\n\n```yml\nkafka:\n  bootstrap.servers: kafka:9092\n  security.protocol: SSL\n  ssl.truststore.location: {{path}}/truststore.jks\n  ssl.truststore.password: {{password}}\n```\n\nSSL auth example:\n\n```yml\nkafka:\n  bootstrap.servers: kafka:9092\n  security.protocol: SSL\n  ssl.truststore.location: {{path}}/truststore.jks\n  ssl.truststore.password: {{password}}\n  ssl.keystore.location: {{path}}/keystore.jks\n  ssl.keystore.password: {{password}}\n  ssl.key.password: {{password}}\n```\n\nSupport for env variables:\n\n```yml\nkafka:\n  bootstrap.servers: ${BOOTSTRAP_SERVERS}\n```\n\n# Screenshots\n\n<p align="center">\n<img alt="kaskade" src="https://raw.githubusercontent.com/sauljabin/kaskade/main/screenshots/dashboard.png">\n</p>\n\n<p align="center">\n<img alt="kaskade" src="https://raw.githubusercontent.com/sauljabin/kaskade/main/screenshots/help.png">\n</p>\n\n# Alternatives\n\n- cli [kcat](https://github.com/edenhill/kcat)\n- cli [zoe](https://github.com/adevinta/zoe)\n- cli [kaf](https://github.com/birdayz/kaf)\n- wui [akhq](https://github.com/tchiotludo/akhq)\n- tui [kcli](https://github.com/cswank/kcli)\n\n# To Do\n\n- Group members table\n- Group partitions table\n- Messages table\n- Schema registry support\n- Interactive search\n- Produce messages\n- Create topic\n- Increment test coverage\n\n# Development\n\nPython supported versions:\n\n<a href="https://pypi.org/project/kaskade"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/kaskade?label="></a>\n\nInstalling poetry:\n\n```sh\npip install poetry\n```\n\nInstalling development dependencies:\n\n```sh\npoetry install\n```\n\nInstalling pre-commit hooks:\n\n```sh\npoetry run pre-commit install\n```\n\nRunning kaskade:\n\n```sh\npoetry run kaskade\n```\n\n### Scripts\n\nRunning unit tests:\n\n```sh\npoetry run python -m scripts.tests\n```\n\nApplying code styles:\n\n```sh\npoetry run python -m scripts.styles\n```\n\nRunning code analysis:\n\n```sh\npoetry run python -m scripts.analyze\n```\n\nRunning code coverage:\n\n```sh\npoetry run python -m scripts.tests-coverage\n```\n\nRunning pre-commit hooks:\n\n```sh\npoetry run python -m scripts.pre-commit\n```\n\nGenerate readme banner:\n\n```sh\npoetry run python -m scripts.banner\n```\n\n### Docker\n\nBuild docker:\n\n```sh\npoetry run python -m scripts.docker-build\n```\n\n> Image tag `sauljabin/kaskade:latest`.\n\nRun with docker (create a `config.yml` file):\n\n```sh\ndocker run --rm -it --network kafka \\\n--volume $(pwd):/kaskade \\\nsauljabin/kaskade:latest\n```\n\n### Bumping Version\n\nHelp:\n\n```sh\npoetry run python -m scripts.release --help\n```\n\n> More info at https://python-poetry.org/docs/cli/#version and https://semver.org/.\n\nUpgrade (`major.minor.patch`):\n\n```sh\npoetry run python -m scripts.release patch\n```\n',
    'author': 'Saúl Piña',
    'author_email': 'sauljabin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sauljabin/kaskade',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
