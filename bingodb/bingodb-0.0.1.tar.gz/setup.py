from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='bingodb',
  version='0.0.1',
  description='Postgres adapter for python flask',
  long_description=r"""Aquesa Bingo DB is a lightweight postgresql adapter written on top of psycopg2 module for flask developers to facilitate postgresql database connectivity in not less then 1 line, i.e., connecting to database is now only 1 line of code. In future versions, multiple databases connectivity possibility will be added.# Connection Example```import bingodbbingodb.BingoDB().db_connect(database="database_name", credentials={"USER":'your username here', "PASSWORD":'your password here'})```# Operation Example```bingodb.BingoDB().db_operation(operationName="insert", tablename="your tablename here", columns="list of your column name(s) here (only string(s))", values="list of your column value(s) here (only string(s))"])```# Command Example```bingodb.BingoDB().db_operation(command="truncate table your_table_name;")```""",
  author='Dheeraj Shyam P.V.S',
  author_email='aquesasolutions@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='adapter', 
  packages=find_packages(),
  install_requires=[''] 
)