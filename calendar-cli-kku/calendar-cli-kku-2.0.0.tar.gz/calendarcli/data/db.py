from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
import os,sys, sqlite3
import julian
from rich import print
from tzlocal import get_localzone

database = "schedule.db"
tables = "events"
today = datetime.today().replace(tzinfo=get_localzone())

@dataclass
class Data:
    name:str
    uuid:str=''
    detail:str=''
    location:str=''
    htmllink:str=''
    juliandate:float = field(default=julian.to_jd(today,fmt='jd'))
    juliandateEnd: float = field(default=julian.to_jd(today+timedelta(hours=1), fmt='jd'))

    @property
    def start(self):return Data.__jd_to_date(self.juliandate)
    @property
    def end(self):return Data.__jd_to_date(self.juliandateEnd)
    
    @start.setter
    def start(self, value):
        self.juliandate = Data.__to_jd(value)
        self.juliandateEnd = Data.__to_jd(Data.__jd_to_date(self.juliandate)+timedelta(hours=1))
    @end.setter
    def end(self, value):
        self.juliandateEnd = Data.__to_jd(value)

    def __jd_to_date(jd:float):
        return julian.from_jd(jd, fmt='jd').replace(tzinfo=get_localzone())

    def __to_jd(v):
      try:
        return julian.to_jd(v, fmt='jd')
      except AttributeError:
        try:
          return  julian.to_jd(datetime(v.year, v.month, v.day), fmt='jd')
        except AttributeError:
          return float(v)


    @property
    def date(self):
      return julian.from_jd(self.juliandate, fmt='jd').replace(tzinfo=get_localzone())
    
    @date.setter
    def date(self,v):
      try:
        self.juliandate = julian.to_jd(v, fmt='jd')
      except AttributeError:
        try:
          self.juliandate = julian.to_jd(datetime(v.year, v.month, v.day), fmt='jd')
        except AttributeError:
          self.juliandate = float(v)



def getPath(filename):
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.abspath(os.path.join(bundle_dir, filename))



class Database:

    def __init__(self, database = database, tables = tables):        
        self.database = database
        self.tables = tables
        self.callback = None       
        try:
            with sqlite3.connect(getPath(database)) as connection:
                a=list(connection.execute(f"""
                    SELECT name FROM sqlite_master WHERE type='table' AND name='{self.tables}';
                """))
                if(not (self.tables,) in a): self.create_table().execute()
        except Exception as e:print(e)



    def execute(self):
        data = None
        try:
            with sqlite3.connect(getPath(database)) as con:
                data = con.execute(self.command)
        except Exception as e:
            print(f"Error ->{e}")
        if self.callback is not None:
            data = self.callback(data)
        self.command = None
        self.callback = None
        return data



    def create_table(self):
        self.command = f'''
            create table {self.tables}(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid TEXT,
                name TEXT,
                juliandate INTEGER,
                juliandateEnd INTEGER,
                location TEXT,
                htmllink TEXT,
                detail TEXT
        );'''
        return self

    
    def add(self,data:Data):
        self.command = f'''
            insert into {self.tables} {tuple( x  for x in asdict(data))} values {tuple( asdict(data)[x]  for x in asdict(data))};
        '''
        # print(self.command)
        return self

    @property
    def getall(self):
        self.command = f"select * from {self.tables}"
        def callback(data):
            datalist = []
            for i in list(data):
                tmp = Data(i[2],i[1],i[4],i[3])
                datalist.append(tmp)
            return datalist
        self.callback = callback
        return self





if __name__ == "__main__":
    pass
    
