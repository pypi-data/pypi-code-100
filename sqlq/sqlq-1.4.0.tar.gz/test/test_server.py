import sqlq


sqlqueue = sqlq.SqlQueueU(server=True, db="db.db")
input("stop? ")
sqlqueue.commit()
sqlqueue.stop()
