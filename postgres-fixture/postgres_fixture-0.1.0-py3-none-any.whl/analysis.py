from sqlalchemy import select,func

get_count = lambda tbl: select(func.count(["*"])).select_from(tbl)

def counts(connection, metadata):
    return {name: connection.execute(get_count(tbl)).fetchone()[0] for name,tbl in metadata.tables.items()}
