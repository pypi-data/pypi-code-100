# 负责对接核心数据数据库sqlite3
# 单一实例CoreDB
# 管理Main1的框架参数
# CHJ不处理错误，错误调用方要使用就要调用方去try
'''
使用方式例子
from Cmaster.HCore.sqlitecore import Table
corefile = "./bin/coretemp"
eventcoretab = Table(corefile, 'P_Event_Now', ['Name', 'file', 'lineno', 'cFunc'])
eventcoretab.delete_all() #清除全部
'''

import sqlite3
import time
import uuid

queries = {
    'SELECT': 'SELECT %s FROM %s WHERE %s',
    'SELECT_ALL': 'SELECT %s FROM %s',
    'INSERT': 'INSERT INTO %s VALUES(%s)',
    'UPDATE': 'UPDATE %s SET %s WHERE %s',
    'DELETE': 'DELETE FROM %s where %s',
    'DELETE_ALL': 'DELETE FROM %s',
    'CREATE_TABLE': 'CREATE TABLE IF NOT EXISTS %s(%s)',
    'DROP_TABLE': 'DROP TABLE %s'}


class DatabaseObject(object):

    def __init__(self, data_file):
        self.db = sqlite3.connect(data_file, check_same_thread=False)
        self.data_file = data_file
        self.busy = False #数据库串行锁信号

    def func(self, FuncName: str, ParaNum: int, Func):
        # 当前链接增加回调函数
        self.db.create_function(FuncName, ParaNum, Func)

    def free(self, cursor):
        cursor.close()

    def write(self, query, values=None):
        num = 0
        while self.busy and num < 10:
            time.sleep(0.02)
            num += 1
        self.busy = True
        cursor = self.db.cursor()
        if values is not None:
            cursor.execute(query, list(values))
        else:
            cursor.execute(query)
        self.db.commit()
        self.busy = False
        return cursor

    def read(self, query, values=None):
        num = 0
        while self.busy and num < 10:
            time.sleep(0.02)
            num += 1
        self.busy = True
        cursor = self.db.cursor()
        if values is not None:
            cursor.execute(query, list(values))
        else:
            cursor.execute(query)
        self.busy = False
        return cursor

    def select(self, tables, *args, **kwargs):
        vals = ','.join([l for l in args])
        locs = ','.join(tables)
        conds = ' and '.join(['%s=?' % k for k in kwargs])
        subs = [kwargs[k] for k in kwargs]
        query = queries['SELECT'] % (vals, locs, conds)
        return self.read(query, subs)

    def select_all(self, tables, *args):
        vals = ','.join([l for l in args])
        locs = ','.join(tables)
        query = queries['SELECT_ALL'] % (vals, locs)
        return self.read(query)

    def insert(self, table_name, *args):
        values = ','.join(['?' for l in args])
        query = queries['INSERT'] % (table_name, values)
        return self.write(query, args)

    def update(self, table_name, set_args, **kwargs):
        updates = ','.join(['%s=?' % k for k in set_args])
        conds = ' and '.join(['%s=?' % k for k in kwargs])
        vals = [set_args[k] for k in set_args]
        subs = [kwargs[k] for k in kwargs]
        query = queries['UPDATE'] % (table_name, updates, conds)
        return self.write(query, vals + subs)

    def delete(self, table_name, **kwargs):
        conds = ' and '.join(['%s=?' % k for k in kwargs])
        subs = [kwargs[k] for k in kwargs]
        query = queries['DELETE'] % (table_name, conds)
        return self.write(query, subs)

    def delete_all(self, table_name):
        query = queries['DELETE_ALL'] % table_name
        return self.write(query)

    def create_table(self, table_name, values):
        query = queries['CREATE_TABLE'] % (table_name, ','.join(values))
        self.free(self.write(query))

    def drop_table(self, table_name):
        query = queries['DROP_TABLE'] % table_name
        self.free(self.write(query))

    def disconnect(self):
        self.db.close()


class Table(DatabaseObject):

    def __init__(self, data_file, table_name, values):
        '''
        CREATE TABLE IF NOT EXISTS %s[table_name](%s)[values]
        :param data_file: 数据库
        :param table_name: 表名称
        :param values: 表头Colume
        '''
        super(Table, self).__init__(data_file)
        self.create_table(table_name, values)
        self.table_name = table_name

    def select(self, *args, **kwargs):
        '''
        SELECT %s[Table] FROM %s[*args] WHERE %s[**kwargs]
        :param args: 多个参数作为select输出
        :param kwargs: 每个传递参数Name=xx都and起来作为Where条件
        :exp:_table.select("Type", "Row", "Col",Name='SelectName',Tag='TagName')
        '''
        return super(Table, self).select([self.table_name], *args, **kwargs)

    def select_all(self, *args):
        '''
        SELECT %s[Table] FROM %s[*args]
        :param args: 对应参数对应表头Column
        :exp: _tabel.select_all('ID','Name','Type')
        '''
        return super(Table, self).select_all([self.table_name], *args)

    def insert(self, *args):
        '''
        INSERT INTO %s[Table] VALUES(%s)[*args]
        :param args: 直接安装表头顺序，插入字符串数据
        :exp: _table.insert('Name','Type','Value')
        '''
        return super(Table, self).insert(self.table_name, *args)

    def update(self, set_args, **kwargs):
        '''
        UPDATE %s[Table] SET %s[set_args] WHERE %s[**kwargs]
        :param set_args: 传递写入的字典
        :param kwargs: 每个传递参数Name=xx都and起来作为Where条件
        :exp: _table.update({"Value":"New","LastValue":"Now"},Tab='TabName', Pane='PaneName')
        '''
        return super(Table, self).update(self.table_name, set_args, **kwargs)

    def delete(self, **kwargs):
        '''
        DELETE FROM %s[Table] where %s[**kwargs]
        :param kwargs: 每个传递参数Name=xx都and起来作为Where条件
        :exp: _table.delete(Tab='TabName', Pane='PaneName')
        '''
        return super(Table, self).delete(self.table_name, **kwargs)

    def delete_all(self):
        return super(Table, self).delete_all(self.table_name)

    def drop(self):
        return super(Table, self).drop_table(self.table_name)
class log2db(object):
    def __init__(self, dbstr='sqlite:///log_db.db'):
        self.skip=not dbstr
        if (self.skip): return
        dbpath="%s"%dbstr.split("sqlite:///")[-1]
        self.log_report=Table(dbpath,"log_data",["boxid","item","result","elpstime","gid"])
        self.log_items=Table(dbpath,"log_item",["boxid","item","key","value","gid"])
        self.log_plan=Table(dbpath,"log_plan",["boxid","plan","report","start","end","num"])
    def plan(self, boxid, plan=None, report=None):
        try:
            if (self.skip): return
            l=self.log_plan.select("num",boxid=boxid,report="")
            lnum=len(list(l))
            l = self.log_plan.select("num", boxid=boxid)
            new_num=[i for i, in l]
            if(new_num):
                now_num=max(new_num)
                next_num=now_num+1
            else:
                now_num=1
                next_num=now_num
            if(plan!=None):
                if(lnum):
                    self.log_plan.update({"plan":plan},boxid=boxid,num=str(now_num))
                else:
                    self.log_plan.insert(boxid,plan,"",time.strftime("%Y-%m-%d %H:%M:%S"),"",str(next_num))
            if(report!=None and lnum):
                self.log_plan.update({"report": report,"end":time.strftime("%Y-%m-%d %H:%M:%S")}, boxid=boxid,num=str(now_num))
        except Exception as e:
            print("[db_plan]%s"%e)
    def add_report(self, boxid,item,elpstime,result,report,*args):
        try:
            # print(boxid,item,report,args)
            if(self.skip):return
            _report=report.copy()
            _report.pop("result")
            _report.pop("elpstime")
            gid=str(uuid.uuid1())
            self.log_report.insert(boxid,item,result,elpstime,gid)
            for i, j in _report.items():
                self.log_items.insert(boxid,item,i,j,gid)
        except Exception as e:
            print("[db_report]%s"%e)
