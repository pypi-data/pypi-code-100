import pymysql

class Student(object):
    def __init__(self):
        self.db = pymysql.connect(host = "localhost",
                                  user="root",
                                  password="Xd12345678",
                                  db = "fc"
                                  )
        self.cursor = self.db.cursor()
    
    def _add(self, id, name, age):
        sql = "insert into student values({},'{}',{})".format(id, name, age)
        self.cursor.execute(sql)
        self.db.commit()
    
    def _select(self):
        pass

    def _delete(self):
        pass

    def _update(self):
        pass

class Bigdata(Student):
    def _select(self):
        sql = "select * from student"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
