# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zzdb']

package_data = \
{'': ['*']}

install_requires = \
['mysql-connector-python>=8.0.26,<9.0.0', 'psycopg2-binary>=2.9.1,<3.0.0']

setup_kwargs = {
    'name': 'zzdb',
    'version': '0.1.1',
    'description': 'python DB-API wrapper',
    'long_description': '# The light Python DB API wrapper with some ORM functions\n\n## Features:\n ---\n## Connect\n```python\nfrom zzdb.db import ZzDb\n\ndatabase_sqlite = ZzDb("sqlite3", database_name=":memory:")\n\ndatabase_mysql = ZzDb(\n    "mysql",\n    database_name="zztest",\n    host="0.0.0.0",\n    port="3308",\n    user="root",\n    password="zztest"\n)\n\ndatabase_postgresql = ZzDb(\n    "postgresql",\n    database_name="zztest1",\n    host="0.0.0.0",\n    port=5432,\n    user="zzuser",\n    password="zztest"\n)\n```\n---\n## Define & migrate database schema (ADD COLUMN only).\n```python\nzzdb.schema import ZzDbSchema\n\nschema = ZzDbSchema()\n\nschema.add(table="topic_table", column="uid", datatype="int", datalen=9, pk=True)\nschema.add(table="topic_table", column="name", datatype="varchar", datalen=100)\n\nschema.add(table="message_table", column="uid", datatype="int", datalen=9, pk=True)\nschema.add(table="message_table", column="message", datatype="varchar", datalen=100)\nschema.add(\n    table="message_table",\n    column="parent_uid",\n    to_table="topic_table",\n    to_column="uid",\n    related="name"\n)\n\ndatabase.set_schema(schema)\n```\n---\n## INSERT, UPDATE, DELETE\n```python\ndatabase.insert("topic_table", {"name": "topic 0"})\ndatabase.insert("topic_table", {"name": "topic 1"})\ndatabase.insert("topic_table", {"name": "topic 2"})\ndatabase.insert("topic_table", {"name": "topic 3"})\n\ndatabase.insert("message_table", {"message": "Message 0 in 0", "parent_uid": 0})\ndatabase.insert("message_table", {"message": "Message 1 in 0", "parent_uid": 0})\ndatabase.insert("message_table", {"message": "Message 0 in 1", "parent_uid": 1})\ndatabase.insert("message_table", {"message": "Message 1 in 1", "parent_uid": 1})\n\n# this returns False because there is no value 2 in topic_table.id - schema works!\ndatabase.insert("message_table", {"message": "Message 1 in 1", "parent_uid": 2})\n\n\ndatabase.delete("message_table", {"uid": 2})\n\ndatabase.update("message_table", {"uid": 0, "message": "updated message"})\n```\n---\n## Cursor\n```python\ncursor = database.cursor(table_name="topic_table")\ncursor = database.cursor(\n    table_name="topic_table",\n    where=" name like \'%2%\'",\n    order="name desc"\n)\ncursor.insert({"name": "insert record via cursor"})\ncursor.delete({"uid": 2})\ncursor.update({"uid": 0, "message": "updated message"})\n\ncursor = database.cursor(sql="select name from topic_table")\n\nfor x in cursor.records():\n    print(x)\n\ncursor.record(0)[\'name\']\ncursor.row_count()\ncursor.first()\ncursor.last()\ncursor.next()\ncursor.prev()\ncursor.bof()\ncursor.eof()\n```',
    'author': 'Andrei Puchko',
    'author_email': 'andrei.puchko@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
