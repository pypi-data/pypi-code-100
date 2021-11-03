# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tuat_feed']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'tuat-feed',
    'version': '0.2.1',
    'description': 'Unofficial library for fetching the feed for TUAT',
    'long_description': '# (非公式)TUAT掲示板ライブラリ\n\n## インストール\n* `python` >= 3.7\n\n```sh\n$ pip install tuat-feed\n```\n\n## 使い方\n\n```python\n>>> import tuat_feed\n>>> feed = tuat_feed.fetch()\n>>> len(feed)\n40\n>>> feed[0]\nPost(...)\n```\n\n### fetch\n`fetch()`を使って投稿情報をダウンロードします。結果は`Post`の配列になっています。\n### Post\n\n`Post`の定義はかんたんに書くと次のようになっています。\n\n```python\nclass Post:\n    post_id: int  # 投稿ID（内部処理用）\n    title: str  # タイトル\n    description: str  # 本文\n    update_date: date  # 最終更新日\n    show_date: (date, date)  # 公開期間\n    author: str  # 担当者\n    origin: str  # 発信元\n    category: str  # カテゴリー\n    attachment: List[Attachment]  # 添付ファイル\n    other: Dict[str, str]  # その他のフィールド\n```\n\n### Attachment\n\n`Attachment`の定義はかんたんに書くと次のようになっています。\n\n```python\nclass Attachment:\n    name: str  # ファイル名\n    url: str  # URL\n```',
    'author': 'Shogo Takata',
    'author_email': 's196643z@st.go.tuat.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pineapplehunter/tuat-feed',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
