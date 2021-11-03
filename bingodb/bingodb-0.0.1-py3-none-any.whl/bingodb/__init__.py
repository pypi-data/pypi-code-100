
import psycopg2

class BingoDB:
    
    connection = {}
    
    def __connect_to_postgres(self, database, credentials, host='localhost'):
        con = psycopg2.connect(host=host, database=database,
                               user=credentials['USER'], password=credentials['PASSWORD'])
        return con

    def db_connect(self, database, credentials, host='localhost'):
        con = self.__connect_to_postgres(
            database=database, credentials=credentials)
        self.connection["postgres"] = con
        
    def db_operation(self, operationName=None, **kwargs):
        
        if not operationName is None and not operationName in ["insert", "retrieve", "update", "pluck"]:
            print(
                f'Invalid operation name \"{operationName}\" provided, expected {" (or) ".join(["insert", "retrieve", "update", "pluck"])}....')
            return

        if "postgres" in self.connection:
            cursor = self.connection[list(self.connection.keys())[0]].cursor()
            if not "command" in kwargs:
            	if "tablename" not in kwargs:
            		print("Expecting tablename....")
            		return
            	elif "columns" not in kwargs:
            		print("Expecting Columns info....")
            		return
            	elif not type(kwargs["tablename"]) == type(str()):
            		print(
        				"Invalid datatype provided for param tablename, expecting str type....")
            		return
            	elif not type(kwargs["columns"]) == type(list()):
            		print(
        				"Invalid datatype provided for param columns, expecting list type...")
            		return

            	if operationName == "insert":
            		if not "values" in kwargs:
            			print(
            				"Expecting \"values\" param....")
            			return
            		elif not type(kwargs["values"]) is type(list()):
            			print(
            				"Invalid datatype provided for param values, expecting list type....")
            			return
            		try:
            			cursor.execute(
            				"insert into {} ({}) values ({})".format(kwargs["tablename"],
            				','.join(kwargs["columns"]),
            				','.join(["%s" for value in kwargs["values"]])), tuple(kwargs["values"]))
            			self.connection["postgres"].commit()
            		except Exception as e:
            			print(e)
            	elif operationName == "retrieve":
	                try:
	                	cursor.execute("select {} from {}".format(','.join(kwargs["columns"]), kwargs["tablename"]))
	                	rows = cursor.fetchall()
	                	return rows
	                except Exception as e:
	                	print(e)
	                	return
            else:
            	try:
            		cursor.execute(kwargs["command"])
            		self.connection["postgres"].commit()
            	except Exception as e:
            		print(e)
            		return

        else:
            print("Connection to database has not been established")
            return
