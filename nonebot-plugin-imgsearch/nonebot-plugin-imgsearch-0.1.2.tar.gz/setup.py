# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_imgsearch']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'httpx[http2]>=0.20.0,<1.0.0',
 'loguru>=0.5.1,<0.6.0']

setup_kwargs = {
    'name': 'nonebot-plugin-imgsearch',
    'version': '0.1.2',
    'description': 'A image search plugin for nonebot2',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# nonebot-plugin-imgsearch\n\n_✨ NoneBot2 图片搜索插件 ✨_\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/nonebot/nonebot2/master/LICENSE">\n    <img src="https://img.shields.io/github/license/nonebot/nonebot2.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-imgsearch">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-imgsearch.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">\n</p>\n\n## 快速启动\n\n* ### 1. 通过pip安装\n  ```\n  pip install nonebot-plugin-imgsearch\n  ```\n\n\n* ### 2. 申请 SAUCENAO API KEY\n  [点此申请](https://saucenao.com/user.php?page=search-api)  \n  `SauceNAO API KEY` 用于直接向saucenao请求搜索，无需模拟抓包，更快，更方便。  \n  一个 `API KEY` 每30s可请求5次，每24h可请求200次。\n\n* ### 3. 配置`.env`文件\n  在你的`.env.*`文件中添加如下内容：\n  ```\n  search_proxy: <your_proxy>\n  # 代理选项，可留空，如果你的bot位于国内，请填一个代理，\n  # 通常它长这样 -> search_proxy="http://127.0.0.1:7890"\n  \n  saucenao_api_key: <your_saucenao_api_key>\n  # 填你申请到的 SauceNAO API KEY, 是必选项。\n  ```\n\n\n\n## 使用教程\n\n  在群组或私聊中发送 `/search [图片]` 即可进行搜索，支持多张  \n  更多权限设置请修改`source code`\n',
    'author': 'bakashigure',
    'author_email': 'bakashigure@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bakashigure/nonebot_plugin_imgsearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
