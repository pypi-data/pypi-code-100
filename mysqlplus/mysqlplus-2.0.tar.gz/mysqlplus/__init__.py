class Colors: fail = '\033[91m' ; good = '\033[92m' ; end = '\033[0m'
class MysqlPlus:
    def __init__(self,user:str,password:str,host:str,database:str=''):
        import mysql.connector as mysql
        # create database connection
        if database: conn = mysql.connect(user=user,password=password,host=host,database=database)
        else: conn = mysql.connect(user=user,password=password,host=host)
        self.conn = conn
        self.mysql = mysql
        self.cursor = conn.cursor(dictionary=True,buffered=True)
    
    def show_databases(self):
        self.cursor.execute('SHOW DATABASES')
        return self.cursor.fetchall()

    def create_database(self,db_name:str):
        try: self.cursor.execute(f'CREATE DATABASE {db_name}') ; return True
        except self.mysql.Error as error: print(Colors.fail+str(error)+Colors.end) ; return False

    def drop_database(self,db_name:str):
        try: self.cursor.execute(f'DROP DATABASE {db_name}') ; return True
        except self.mysql.Error as error: print(Colors.fail+str(error)+Colors.end) ; return False

    def show_tables(self):
        return self.cursor.execute('SHOW TABLES') ; self.cursor.fetchall()

    def create_table(self,tableName:str,**kwarg):
        sql = f'CREATE TABLE {tableName} (id INT(10) AUTO_INCREMENT, '
        for rowName,rowType in kwarg.items(): sql=sql+f'{rowName} {rowType},'
        # close sql tag and remove last , from loop
        sql=sql[:-1]+',PRIMARY KEY(id))'
        try: self.cursor.execute(sql) ; return True
        except self.mysql.Error as error: print(Colors.fail+str(error)+Colors.end) ; return False

    def drop_table(self,tableName:str):
        try: self.cursor.execute(f'DROP TABLE {tableName}') ; return True
        except self.mysql.Error as error: print(Colors.fail+str(error)+Colors.end) ; return False

    def insert(self,tableName:str,**kwarg):
        sql = f"INSERT INTO {tableName} "
        valS,rows,val = [],[],[]
        for rowName,rowVal in kwarg.items():
            valS.append('%s') ; rows.append(rowName) ; val.append(rowVal)
        valS=' VALUES '+str(tuple(valS)).replace("'",'')
        sql=sql+str(tuple(rows)).replace("'",'').replace(',)',')')+valS.replace(',)',')')
        val=tuple(val)
        try: self.cursor.execute(sql,val) ; self.conn.commit() ;return True
        except self.mysql.Error as error: print(Colors.fail+str(error)+Colors.end) ; return False

    def fetch_one(self,tableName:str,whereSql:str):
        #whereSql example: name='juan' AND age > 21
        try: self.cursor.execute(f"SELECT * FROM {tableName} WHERE {whereSql}") ; return self.cursor.fetchone()
        except self.mysql.Error as error: print(Colors.fail+str(error)+Colors.end) ; return False

    def fetch_all(self,tableName:str,whereSql:str):
        #whereSql example: name='juan' AND age > 21
        try: self.cursor.execute(f"SELECT * FROM {tableName} WHERE {whereSql}") ; return self.cursor.fetchall()
        except self.mysql.Error as error: print(Colors.fail+str(error)+Colors.end) ; return False

    def update(self,tableName,setSql:str,whereSql:str):
        # whereSql example: name='tesla' AND date > '2021-10-10'
        # setSql example: name='Tesla', ceo='Elon musk'
        sql = f'UPDATE {tableName} SET {setSql} WHERE {whereSql}'
        try: self.cursor.execute(sql) ; self.conn.commit() ;return self.cursor.fetchone()
        except self.mysql.Error as error: print(Colors.fail+str(error)+Colors.end) ; return False

    def delete(self,tableName,whereSql:str):
        #whereSql example: name='juan' AND age > 21
        try: self.cursor.execute(f"DELETE FROM {tableName} WHERE {whereSql}") ; self.conn.commit() ;return self.cursor.fetchone()
        except self.mysql.Error as error: print(Colors.fail+str(error)+Colors.end) ; return False

    def sql(self,sql:str,commit=False):
        try:
            self.cursor.execute(sql)
            if commit: self.conn.commit()
            return self.cursor.fetch()
        except self.mysql.Error as error: print(Colors.fail+str(error)+Colors.end) ; return False