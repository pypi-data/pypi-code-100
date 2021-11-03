from sqlitedict import SqliteDict

def open(fp, flag='n'):
    return SqliteDict(fp, flag=flag, autocommit=False)
