import pymysql
class a(object):
    def __init__(self,host,user,password,port,db,charset) :
        self.bd=pymysql.connect(host=host,user=user,password=password,port=port,db=db,charset=charset)
        self.v=self.bd.cursor()


    def add(self,id,name,price,number):
        sql="select * from newtable where name='{}' ".format(name)
        self.v.execute(sql)
        d=self.v.fetchone()
        if d:
            number +=int(d[3])
            sql="update newtable set number={},price={},where name='{}'".format(number,price,name)
            self.v.execute(sql)
            self.bd.commit()
        else:
            sql="insert into newtable values({0},'{1}',{2},{3})".format(id,name,price,number)
            self.v.execute(sql)
            self.bd.commit()


    def insert(self,id,name,age,phone,address):
        sql='insert into st(id,name,age,phone,address)  values("{}","{}","{}","{}","{}")'.format(id,name,age,phone,address)
        self.v.execute(sql)
        self.bd.commit()

    def update(self,zhi,values,ke,t):
        sql='update st set {}={} where {} ={}'.format(zhi,values,ke,t)
        self.v.execute(sql)
        self.bd.commit()

        
    def remove(self,ke,va):
        sql='delete from st where {}={}'.format(ke,va)
        self.v.execute(sql)
        self.bd.commit()






# d=a('localhost','root','121416',3306,'fc','utf8')
# d.add(5,"app5",1000,50)

