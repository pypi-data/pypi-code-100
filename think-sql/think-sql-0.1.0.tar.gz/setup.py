# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['think_sql']

package_data = \
{'': ['*']}

install_requires = \
['PyMySQL>=1.0.2,<2.0.0',
 'cacheout>=0.13.1,<0.14.0',
 'dill>=0.3.4,<0.4.0',
 'jsonpath>=0.82,<0.83',
 'loguru>=0.5.3,<0.6.0',
 'pretty-errors>=1.2.24,<2.0.0',
 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'think-sql',
    'version': '0.1.0',
    'description': 'ThinkSQL like think-orm(ThinkPHP)',
    'long_description': '# ThinkSQL 类似ThinkPHP的数据库引擎\n\n## 安装\n```\npip install think-sql\n```\n\n## 使用\n\n### 1. simple demo\n\n> Database: `test` Table: `user`\n\n```\nfrom think-sql.database import DB\n\nconfig = {\n    \'database\': \'test\',\n    \'host\': \'127.0.0.1\',\n    \'port\': 3306,\n    \'username\': \'root\',\n    \'password\': \'root\',\n}\n\nwith DB(**config) as db:\n    data = db.table(\'user\').where(\'id\',1).find()\n    print(data)\n```\nresult\n```\n{\n    "id":1,\n    "username":"hbh112233abc",\n    "age":"36",\n    "address":"FUJIAN.XIAMEN"\n}\n```\n\n## 开发\n\n- `poetry` [Python包管理之poetry的使用](https://blog.csdn.net/zhoubihui0000/article/details/104937285)\n\n```\n# 配置虚拟环境在项目目录下\npoetry config virtualenvs.path true\n# 安装依赖\npoetry install\n# 进入虚拟环境\npoetry shell\n```\n### poetry命令\n\n|名称| 功能|\n|-|-|\n|new|创建一个项目脚手架，包含基本结构、pyproject.toml 文件|\n|init|基于已有的项目代码创建 pyproject.toml 文件，支持交互式填写|\n|install|安装依赖库|\n|update|更新依赖库|\n|add|添加依赖库|\n|remove|移除依赖库|\n|show|查看具体依赖库信息，支持显示树形依赖链|\n|build|构建 tar.gz 或 wheel 包|\n|publish|发布到 PyPI|\n|run|运行脚本和代码|\n\n## 单元测试\n```\npytest --cov --cov-report=html\n```\n',
    'author': 'hbh112233abc',
    'author_email': 'hbh112233abc@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hbh112233abc/think-sql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
