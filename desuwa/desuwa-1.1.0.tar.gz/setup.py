# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['desuwa', 'desuwa.rule']

package_data = \
{'': ['*'], 'desuwa': ['knp_rules/*']}

install_requires = \
['dataclasses-json>=0.5.2,<0.6.0',
 'pyknp>=0.4.5,<0.5.0',
 'sexpdata>=0.0.3,<0.0.4']

entry_points = \
{'console_scripts': ['desuwa = desuwa.cli:main']}

setup_kwargs = {
    'name': 'desuwa',
    'version': '1.1.0',
    'description': 'Feature annotator based on KNP rule files',
    'long_description': '\n# Desuwa\n\n[![PyPI version](https://badge.fury.io/py/desuwa.svg)](https://badge.fury.io/py/desuwa)\n[![Python Versions](https://img.shields.io/pypi/pyversions/desuwa.svg)](https://pypi.org/project/desuwa/)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Downloads](https://pepy.tech/badge/desuwa/week)](https://pepy.tech/project/desuwa)\n\n[![CircleCI](https://circleci.com/gh/megagonlabs/desuwa.svg?style=svg&circle-token=b10ac94d6822fadf276297d457cf219ba1bea7f6)](https://app.circleci.com/pipelines/github/megagonlabs/desuwa)\n[![CodeQL](https://github.com/megagonlabs/desuwa/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/megagonlabs/desuwa/actions/workflows/codeql-analysis.yml)\n[![Maintainability](https://api.codeclimate.com/v1/badges/b8277e89862471dcf827/maintainability)](https://codeclimate.com/github/megagonlabs/desuwa/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/b8277e89862471dcf827/test_coverage)](https://codeclimate.com/github/megagonlabs/desuwa/test_coverage)\n[![markdownlint](https://img.shields.io/badge/markdown-lint-lightgrey)](https://github.com/markdownlint/markdownlint)\n[![jsonlint](https://img.shields.io/badge/json-lint-lightgrey)](https://github.com/dmeranda/demjson)\n[![yamllint](https://img.shields.io/badge/yaml-lint-lightgrey)](https://github.com/adrienverge/yamllint)\n\nFeature annotator to morphemes and phrases based on KNP rule files (pure-Python)\n\n## Quick Start\n\nDesuwa exploits [Juman++](https://github.com/ku-nlp/jumanpp) outputs.\n\n```console\n$ pip install desuwa\n$ echo \'歌うのは楽しいですわ\' | jumanpp | desuwa\n+\t["&表層:付与", "連体修飾", "用言:動"]\n歌う うたう 歌う 動詞 2 * 0 子音動詞ワ行 12 基本形 2 "代表表記:歌う/うたう ドメイン:文化・芸術;レクリエーション"\t["タグ単位始", "形態素連結-数詞", "固有修飾", "活用語", "文頭", "文節始", "Ｔ連体修飾", "ドメイン:文化・芸術;レクリエーション", "Ｔ固有付属", "内容語", "Ｔ固有末尾", "自立"]\n+\t["受けNONE", "外の関係", "形副名詞", "助詞", "Ｔ連用", "ハ", "タグ単位受:-1"]\nの の の 名詞 6 形式名詞 8 * 0 * 0 NIL\t["タグ単位始", "Ｔ動連用名詞化前文脈", "形態素連結-数詞", "固有修飾", "形副名詞", "特殊非見出語", "名詞相当語", "Ｔ固有付属", "付属", "内容語", "Ｔ固有末尾"]\nは は は 助詞 9 副助詞 2 * 0 * 0 NIL\t["形態素連結-数詞", "固有修飾", "Ｔ固有付属", "付属", "Ｔ固有末尾"]\n+\t["&表層:付与", "用言:形", "連体修飾", "助詞"]\n楽しい たのしい 楽しい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2 "代表表記:楽しい/たのしい"\t["タグ単位始", "形態素連結-数詞", "固有修飾", "活用語", "文節始", "Ｔ連体修飾", "Ｔ固有付属", "内容語", "Ｔ固有末尾", "自立"]\nです です です 助動詞 5 * 0 無活用型 26 基本形 2 NIL\t["形態素連結-数詞", "固有修飾", "活用語", "Ｔ連体修飾", "Ｔ固有付属", "付属", "Ｔ固有末尾"]\nわ わ わ 助詞 9 終助詞 4 * 0 * 0 NIL\t["形態素連結-数詞", "固有修飾", "文末", "表現文末", "Ｔ固有付属", "付属", "Ｔ固有末尾"]\nEOS\n\n$ echo \'歌うのは楽しいですわ\' | jumanpp | desuwa | desuwa --predicate\n歌う\t歌う/うたう\t1\t動\n楽しいですわ\t楽しい/たのしい\t1\t形\n\n$ echo \'歌うのは楽しいですわ\' | jumanpp | desuwa --segment\n歌う│のは│楽しいですわ\n```\n\n## Note\n\nDesuwa is currently confirmed to work with the following rule files.\n\n- ``mrph_filter.rule``\n- ``mrph_basic.rule``\n- ``bnst_basic.rule``\n\n## License\n\nApache License 2.0 except for rules files in [desuwa/knp_rules](desuwa/knp_rules) imported from [KNP](https://github.com/ku-nlp/knp)\n',
    'author': 'Yuta Hayashibe',
    'author_email': 'hayashibe@megagon.ai',
    'maintainer': 'Yuta Hayashibe',
    'maintainer_email': 'hayashibe@megagon.ai',
    'url': 'https://github.com/megagonlabs/desuwa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
