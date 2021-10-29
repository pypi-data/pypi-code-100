import marvmiloTools as mmt

mmt.sql.connect("database.db")
mmt.sql.execute("CREATE TABLE IF NOT EXISTS test (a INTEGER, b INTEGER)")
mmt.sql.execute("INSERT INTO test (a,b) VALUES (0,1)")
mmt.sql.disconnect()
