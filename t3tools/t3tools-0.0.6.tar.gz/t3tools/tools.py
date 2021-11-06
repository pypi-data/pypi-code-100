# ■■■■导入■■■■
import numpy as np
import pandas as pd
# import matplotlib as mpl
# from matplotlib.pyplot import *
from datetime import datetime, timedelta
from pprint import pprint

import time
import io
import os
import json
from functools import wraps
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, Date, Time, DateTime, String, ForeignKey
from sqlalchemy.pool import NullPool
from sqlalchemy.pool import NullPool



# from django.http import HttpResponse
# from django.core import serializers


# ■■■■定义■■■■
# 统计函数执行时间
def fn_timer(function):
	@wraps(function)
	def function_timer(*args, **kwargs):
		t0 = time.time()
		result = function(*args, **kwargs)
		t1 = time.time()
		print("耗时: %s 秒" % (str(round(t1 - t0, 2))))
		return result



	return function_timer



# 基础环境设置
def baseConfig():
	'''基础设置（numpy打印宽度、matplotlib字体、等等）
	:return: 无
	'''
	np.set_printoptions(linewidth=200)
	pd.set_option('display.width', 200)
	mpl.rcParams['font.sans-serif'] = ['SimHei']
	mpl.rcParams['axes.unicode_minus'] = False



# 类型转换：str->date
def str2date(inStr):
	'''类型转换：str->date
	:param inStr: yyyy-mm-dd格式
	:return: datetime.date
	'''
	return datetime.strptime(inStr, '%Y-%m-%d').date()



# 类型转换：date->str
def date2str(inDate):
	return datetime.strftime(inDate, '%Y-%m-%d')



def dttm2str(dttm):
	return dttm.strftime('%Y-%m-%d_%H%M%S')



def curDttm2str():
	return datetime.now().strftime('%Y-%m-%d_%H%M%S')



# 读文件
def readFileLines(fname, encoding='utf8'):
	f = open(fname, 'r', encoding=encoding)
	lines = f.readlines()
	f.close()

	# newLines = [line[:-1] for line in lines]
	newLines = []
	for line in lines:
		if line[-1] == '\n':
			newLines.append(line[:-1])
		else:
			newLines.append(line)

	return newLines



# 读文件（to字符串）
def readFileString(fname, encoding='utf8'):
	f = open(fname, 'r', encoding=encoding)
	string = f.read()
	f.close()

	return string



# 写文件
def writeToFile(fname, content, encoding='utf8'):
	f = open(fname, 'w', encoding=encoding)
	f.write(content)
	f.close()



# ■■■■HTTP■■■■
# 成功
def done():
	return HttpResponse('DONE')



# 失败
def fail():
	return HttpResponse('FAIL')



# 返回JSON PAYLOAD
def jsonPayload(obj, replaceNone=False):
	s = json.dumps(obj)

	if replaceNone:
		s = s.replace('None', '')

	return HttpResponse(s, content_type='application/json')



# 装饰器: Log网络请求
def logwebreq(function):
	@wraps(function)
	def function_logwebreq(req):
		print('■■Web请求■■' + function.__name__ + '■■')
		x = function(req)
		print('■■Web请求■■' + function.__name__ + '■■DONE')
		print()
		return x



	return function_logwebreq



# 装饰器: Log函数调用
def logfunc(function):
	@wraps(function)
	def theFunc(req):
		print('■■函数■■' + function.__name__ + '■■')
		x = function(req)
		print('■■函数■■' + function.__name__ + '■■DONE■■')
		return x



	return theFunc



# 姜戈to杰森
def django2json(objCol):
	return json.loads(serializers.serialize('json', objCol))



# ■■■■DB相关■■■■
# 获取DB连接
def getDb():
	# engn = create_engine('oracle+cx_oracle://MYATM:123456@localhost:1521/MYATM?allow_twophase=False', poolclass=NullPool, echo=False)
	# engn = create_engine('oracle+cx_oracle://MYATM:ifwedream9@localhost:1521/MYATM?allow_twophase=False', poolclass=NullPool, echo=False)
	engn = create_engine(r'sqlite:///D:\DEV\DEVTOOL_REMOTE\web\db.sqlite3',
						 poolclass=NullPool, echo=False, connect_args={'check_same_thread': False})

	conn = engn.connect()
	meta = MetaData(engn)

	return conn, meta



def getDevDb():
	engn = create_engine(
		'oracle+cx_oracle://SYSADM:SYSADM@l-peoplesoft2.ops.dev.cn0.qunar.com:1521/HCMDEV2?allow_twophase=False', poolclass=NullPool, echo=False)

	conn = engn.connect()
	meta = MetaData(engn)

	return conn, meta



def getUatDb():
	engn = create_engine(
		'oracle+cx_oracle://SYSADM:SYSADM@l-peoplesoft2.ops.dev.cn0.qunar.com:1521/HCMUAT?allow_twophase=False', poolclass=NullPool, echo=False)

	conn = engn.connect()
	meta = MetaData(engn)

	return conn, meta



def getCdeDb():
	engn = create_engine(
		'oracle+cx_oracle://SYSADM:SYSADM@l-psdb3.ops.cn5.qunar.com:1521/HCMCDE?allow_twophase=False', poolclass=NullPool, echo=False)

	conn = engn.connect()
	meta = MetaData(engn)

	return conn, meta



def getDmoDb():
	engn = create_engine(
		'oracle+cx_oracle://SYSADM:PSqaz019@l-psdb3.ops.cn5.qunar.com:1521/HCMDMO?allow_twophase=False', poolclass=NullPool, echo=False)

	conn = engn.connect()
	meta = MetaData(engn)

	return conn, meta



def getUatDb4INF():
	engn = create_engine(
		'oracle+cx_oracle://PSINF:Passw0rd@l-peoplesoft2.ops.dev.cn0.qunar.com:1521/HCMUAT?allow_twophase=False', poolclass=NullPool, echo=False)

	conn = engn.connect()
	meta = MetaData(engn)

	return conn, meta



def getPrdDb():
	engn = create_engine(
		'oracle+cx_oracle://SYSADM:PSqaz019@l-psdbvip1.ops.cn2.qunar.com:1521/HCMPRD?allow_twophase=False', poolclass=NullPool, echo=False)

	conn = engn.connect()
	meta = MetaData(engn)

	return conn, meta



# 创建自增序列
def createAutoIncSeq(conn, tableName):
	try:
		conn.execute(f'DROP SEQUENCE PK_SEQ_{tableName}')
	except:
		pass

	conn.execute(f'''
		CREATE SEQUENCE PK_SEQ_{tableName} MINVALUE 1 MAXVALUE 999999999999
		INCREMENT BY 1
		START WITH 1
	''')



# 处理自增主键
def makeAutoIncId(conn, tableName):
	# 创建自增序列
	createAutoIncSeq(conn, tableName)

	# 创建触发器
	conn.execute(f'''
		CREATE OR REPLACE TRIGGER PK_TGR_{tableName}
		BEFORE INSERT ON {tableName}
		FOR EACH ROW
		  BEGIN
			SELECT PK_SEQ_{tableName}.NEXTVAL
			INTO :NEW.ID
			FROM DUAL;
		  END;
	''')

	conn.execute('commit')



# 建表
def createTable(conn, meta, name, table, autoKey=True):
	try:
		conn.execute(F'DROP TABLE {name}')
	except Exception as e:
		pass

	meta.create_all(tables=[table])

	if autoKey:
		makeAutoIncId(conn, name)
	else:
		createAutoIncSeq(conn, name)



# 建索引
def createIndex(conn, tableName, fieldName):
	conn.execute(
		F"""CREATE INDEX {tableName}_{fieldName}_INDEX ON {tableName}({fieldName})""")



# 批量插入数据
def batchInsert(tableName, rows, conn, meta):
	if len(rows) == 0:
		return

	# 引用
	theTable = Table(tableName, meta, autoload=True)

	# 插入
	conn.execute(theTable.insert(), rows)



# 获取一个标量
def getScalar(sql, conn):
	rows = conn.execute(sql)

	rslt = None
	for row in rows:
		rslt = row[0]

	return rslt



# 获取一行
def getOneRow(sql, conn):
	rows = conn.execute(sql)

	rslt = None
	for row in rows:
		rslt = row

	return rslt



# 转换：SQL2CSV
def sql2csv(sql, conn):
	rcol = []
	rows = conn.execute(sql)
	for row in rows:
		newrow = [str(x) for x in row]
		s = ','.join(newrow)
		rcol.append(s)
	rstr = '\n'.join(rcol)

	fcol = []
	for f in rows._metadata.keys:
		fcol.append(f.upper())
	fstr = ','.join(fcol) + '\n'

	return fstr + rstr



# 转换：SQL2HTML Table
def sql2htmlTable(sql, conn, hdrFldCol=[]):
	rows = conn.execute(sql)

	fcol = []
	if hdrFldCol == []:
		for f in rows._metadata.keys:
			fcol.append(f"<td>{f.upper()}</td>")
	else:
		for f in hdrFldCol:
			fcol.append(f"<td>{f}</td>")

	fstr = '\n'.join(fcol)
	fstr = f"<tr style='background-color: #d6e4ff;'>\n{fstr}\n</tr>" + '\n'

	rcol = []
	for row in rows:
		newrow = [f"<td>{str(x)}</td>" for x in row]
		# s = '\n'.join(newrow)
		rcol.append(f"<tr>{''.join(newrow)}</tr>")
	rstr = '\n'.join(rcol) + '\n'

	return '<table border=1 cellspacing=0 style="border-collapse: collapse;">\n' + fstr + rstr + '</table>\n'



# 转换：SQL2DF
def sql2df(sql, conn, indexCol=-1):
	csv = sql2csv(sql, conn)

	if indexCol == -1:
		df = pd.read_csv(io.StringIO(csv), parse_dates=True)
	else:
		df = pd.read_csv(io.StringIO(csv), parse_dates=True,
						 index_col=indexCol)

	return df



# 转换：SQL2DICT
def sql2dict(sql, conn):
	pass



# 转换: SQL2JSON
def sql2col(sql, conn, showSql=False):
	if showSql:
		print(sql)

	rows = conn.execute(sql)

	fcol = []
	for f in rows._metadata.keys:
		fcol.append(f.lower())

	rcol = []
	for row in rows:
		d = {}
		for idx, x in enumerate(row):
			d[fcol[idx]] = str(x)

		rcol.append(d)

	return rcol



def sql2obj(sql, conn, showSql=False):
	if showSql:
		print(sql)

	rows = conn.execute(sql)

	if rows is None:
		return None

	fcol = []
	for f in rows._metadata.keys:
		fcol.append(f.lower())

	xxx = None
	for row in rows:
		xxx = row

	if xxx is None:
		return None

	d = {}
	for idx, x in enumerate(xxx):
		d[fcol[idx]] = str(x)

	return d



# 执行SQL语句
def sqlExec(sql, conn, showSql=False):
	if showSql:
		print(sql)

	conn.execute(sql)



# ■■■■DB包装■■■■
# 获取SimSig的Avmood
def getSimSigAvmood():
	r = []

	conn, meta = getDb()
	rows = conn.execute('SELECT AVMOOD FROM SIMSIG')

	for row in rows:
		r.append(row[0])

	return r



# 集合相关
# 组内提升一级
def liftOneGroup(col, fldName):
	r = []
	curKey = ''
	curCol = []
	for idx, row in enumerate(col):
		if idx == 0:
			curKey = row[fldName]
		else:
			if row[fldName] != curKey:
				r.append({
					'key': curKey,
					'col': curCol
				})
				curKey = row[fldName]
				curCol = []

		curCol.append(row)

	r.append({
		'key': curKey,
		'col': curCol
	})

	return r



# ■■■■字符串■■■■
def left(inStr, theLen):
	if theLen > len(inStr):
		theLen = len(inStr)

	return inStr[:theLen]



def right(inStr, theLen):
	if theLen > len(inStr):
		theLen = len(inStr)

	return inStr[len(inStr) - theLen:]



def lpad(inStr, padStr, totLen):
	return right(str(padStr) * totLen + str(inStr), totLen)



# ■■■■打印■■■■
# 突出打印
def cprint(msg):
	print('\033[1;31m' + str(msg))
	print('\033[0m', end='')



# 泰伯分隔打印
def tprint(msg):
	print(msg, sep='\t')



# ■■■■其他■■■■
# 获取RunBatch
def getRunBatch():
	return datetime.now().strftime("%y%m%d.%H%M%S")



# 耗时统计：tick
def tick():
	global tickTock_bgnTime

	tickTock_bgnTime = datetime.now()



# 耗时统计：tock
def tock():
	global tickTock_bgnTime

	tickTock_endTime = datetime.now()
	durTime = tickTock_endTime - tickTock_bgnTime

	print('    耗时 %16.2f 秒' % durTime.total_seconds())



# 耗时统计：bigTick
def bigTick():
	global bigTickTock_bgnTime

	bigTickTock_bgnTime = datetime.now()



# 耗时统计：bigTock
def bigTock():
	global bigTickTock_bgnTime

	bigTickTock_endTime = datetime.now()
	durTime = bigTickTock_endTime - bigTickTock_bgnTime

	print('    ------------------------')
	print('    整体耗时 %12.2f 秒' % durTime.total_seconds())
	print('    ------------------------')



# ■■■■我的模板■■■■
def myTemplate(name):
	import shutil

	srcDir = r'C:\Anaconda3\Lib\site-packages\tang'
	dstDir = r'C:\Users\TANG\DEV\ALL-IN\web\soul\static\soul'

	srcPath = srcDir + '/myTemplate.coffee'
	dstPath = dstDir + '/' + name + '.coffee'
	shutil.copy(src=srcPath, dst=dstPath)

	srcPath = srcDir + '/myTemplate.css'
	dstPath = dstDir + '/' + name + '.css'
	shutil.copy(src=srcPath, dst=dstPath)

	newh = []
	h = readFileLines(srcDir + '/myTemplate.html')
	for l in h:
		newh.append(l.replace('$$$', name))

	o = '\n'.join(newh)

	writeToFile(dstDir + '/' + name + '.html', o)



# ■■拼音■■
# 我的拼音化格式
def myPinyinFormat(theStr):
	from pypinyin import pinyin, lazy_pinyin, Style

	sm = pinyin(theStr, style=Style.INITIALS)
	ym = pinyin(theStr, style=Style.FINALS_TONE)

	# print(sm)
	# print(ym)

	sm2 = [x[0] for x in sm]
	ym2 = [x[0] for x in ym]

	# print(sm2, ym2)

	return sm2, ym2


# ■■■■结束■■■■
