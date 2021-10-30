try:
	import pymysql
	from prettytable import PrettyTable
	from prettytable import from_db_cursor
except ImportError:
	raise ImportError("Please install required modules. See in the GitHub - https://github.com/immadev2k21/JetORM")

try:
	import sqlite3
except ImportError:
	raise ImportError("Standard modules could not be imported!")


# TODO: Random num method
''' 148518906_smth '''

class Base:

	@staticmethod
	def _load(table: str, ids: tuple):
		ids = ', '.join(map(str, ids))
		sql = (f"SELECT * FROM `{table}` WHERE `id` IN({ids})")
		return sql

	@staticmethod
	def _load_all(table: str):
		sql = (f"SELECT * FROM `{table}`")
		return sql

	@staticmethod
	def _insert_mysql(table: str, column_values: dict):
		columns = ', '.join(column_values.keys())
		values = tuple(column_values.values())
		placeholders = ", ".join(["%s"] * len(column_values.keys()))
		sql = (f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders})")
		
		return (sql, values)

	@staticmethod
	def _insert(table: str, column_values: dict):
		columns = ', '.join(column_values.keys())
		values = tuple(column_values.values())
		placeholders = ", ".join("?" * len(column_values.keys()))
		sql = (f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders})")

		return (sql, values)

	@staticmethod
	def _add_mysql(table: str, field: str, type_: str, unsigned=True):
		type_ = type_.lower().strip().split(':')

		'''
		*** input: instance_of_the_class.add(table, field, 'varchar:255')
		***  output: type_ = ['varchar', '255']
		'''
		
		
		# null
		if (type_[0] in ('varchar', 'text')):

			sql = (f"ALTER TABLE `{table}` ADD `{field}` {type_[0].upper()}({type_[1]}) NULL DEFAULT NULL;")

		# null and unsigned
		if (type_[0] == 'int'):

			sql = (f"ALTER TABLE `{table}` ADD `{field}` {type_[0].upper()}({type_[1]}) UNSIGNED NULL DEFAULT NULL;")


		# null and not unsigned
		if (type_[0] == 'int' and not unsigned):

			sql = (f"ALTER TABLE `{table}` ADD `{field}` {type_[0].upper()}({type_[1]}) NULL DEFAULT NULL;")


		# type_[1] == 'ct'. for example: date:ct (ct - currentTimeStamp)
		if (type_[0] == 'dt' and type_[1] == 'ct'):

			sql = (f"ALTER TABLE `{table}` ADD `{field}` DATETIME NULL DEFAULT CURRENT_TIMESTAMP;")


		if (type_[0] == 'id'):
			field += '_id'
			sql = (f"ALTER TABLE `{table}` ADD `{field}` INT(11) UNSIGNED, ADD (`{field}`);")
			sql_create_index = (f"CREATE INDEX index_foreignkey_users_type ON `{field}`;")


		if (type_[0] == 'bit'):
			sql = (f"ALTER TABLE `{table}` ADD `{field}` BIT")


		if (type_[0] == 'bool') or (type_[0] == 'tint' and type_[1] == '1'):
			sql = (f"ALTER TABLE `{table}` ADD `{field}` TINYINT(1) NULL DEFAULT NULL;")


		if (type_[0] == 'tint' and type_[1] == '0'):
			sql = (f"ALTER TABLE `{table}` ADD `{field}` TINYINT NULL DEFAULT NULL;")


		if (type_[0] == 'bint'):
			sql = (f"ALTER TABLE `{table}` ADD `{field}` BIGINT NULL;")

		if 'sql_create_index' not in (locals(), globals()):
			pass 
			""" we check whether there is no sql_create_index variable in locals and globals """
		else:
			return sql_create_index

		return sql

class mysql(Base):
	"""
	 				MySQL
		dms - DataBase Management System
	"""
	def __init__(self, host, database, 
		port=3306, user="root", password=""):

		super(mysql, self).__init__()
		self.host = host 
		self.database = database
		self.port = port
		self.user = user
		self.password = password

		""" Initializing the connection to the database (MySQL) """

		try:
			self.connection = pymysql.connect(
				host=self.host,
				port=self.port,
				user=self.user,
				password=self.password,
				database=self.database,
				cursorclass=pymysql.cursors.DictCursor)

			self.cursor = self.connection.cursor()
		except Exception as ex:
			raise ex
		finally:
			self.connection.close()

	def dispense(self, table: str):
		""" Creating a table """
		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			sql = (f"CREATE TABLE IF NOT EXISTS `{table}` ( `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT , PRIMARY KEY (`id`));") 

			cursor.execute(sql)

	def add(self, table: str, field: str, type_: str, unsigned=True):
		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			try:
				cursor.execute(Base._add_mysql(table, field, type_, references_table, unsigned))
			except pymysql.err.OperationalError as ex:
				pass # catching duplication of fields

	def puts(self, table: str, column_values: dict, unsigned=True):
		for key, value in column_values.items():
			if isinstance(value, str):
				if (len(value) <= 191):
					sql_create = (f"ALTER TABLE `{table}` ADD `{key}` VARCHAR(191) NULL DEFAULT NULL")

				else:
					sql_create = (f"ALTER TABLE `{table}` ADD `{key}` TEXT NULL DEFAULT NULL")

	
			if isinstance(value, int):
				sql_create = (f"ALTER TABLE `{table}` ADD `{key}` INT(11) UNSIGNED NULL DEFAULT NULL")


			if isinstance(value, int) and not unsigned:
				sql_create = (f"ALTER TABLE `{table}` ADD `{key}` INT(11) NULL DEFAULT NULL")

			self.connection.ping()  # reconnecting mysql
			with self.connection.cursor() as cursor:
				try:
					cursor.execute(sql_create)
				except pymysql.err.OperationalError as ex:
					pass	# catching duplication of fields


		self.insert(table, column_values)

	def insert(self, table: str, column_values: dict):	
		self.connection.ping() 	# reconnecting mysql	
		with self.connection.cursor() as cursor:
			cursor.execute(Base._insert_mysql(table, column_values)[0], \
						   Base._insert_mysql(table, column_values)[1])
			self.connection.commit()

	def exec(self, query: str, *values):
		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			cursor.execute(query, values)
			rows = cursor.fetchall()
		return rows

	def load(self, table: str, ids: tuple):
		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			try:
				cursor.execute(Base._load(table, ids))
				rows = cursor.fetchall()

				return rows

			except Exception as _:
				print(_)

	def load_all(self, table: str):
		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			try:
				cursor.execute(Base._load_all(table))
				rows = cursor.fetchall()

				return rows

			except Exception as _:
				print(_)

	def store(self):
		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			self.connection.commit()
		
	def recent(self, table: str, order_by_field: str):
		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			sql = (f"SELECT * FROM `{table}` ORDER BY `{order_by_field}` DESC LIMIT 1")
			cursor.execute(sql)
			rows = cursor.fetchall()
		return rows
			
	def read(self, table: str, fields: tuple, sub_sql: str=None, *values):
		fields = "`" + "`, `".join(fields) + "`"
		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			if sub_sql is None:
				sql = (f"SELECT {fields} FROM `{table}`")
				cursor.execute(sql, values)
				rows = cursor.fetchall()
			else:
				sql = (f"SELECT {fields} FROM `{table}` WHERE {sub_sql}")
				cursor.execute(sql, values)
				rows = cursor.fetchall()
			return rows

	def read_one(self, table: str, fields: tuple, sub_sql: str=None, *values):
		fields = "`" + "`, `".join(fields) + "`"
		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			if sub_sql is None:
				sql = (f"SELECT {fields} FROM `{table}` LIMIT 1")
				cursor.execute(sql, values)
				rows = cursor.fetchall()
			else:
				sql = (f"SELECT {fields} FROM `{table}` WHERE {sub_sql} LIMIT 1")
				cursor.execute(sql, values)
				rows = cursor.fetchall()
			return rows

	def update(self, table: str, column_values: dict, sub_sql: str=None, *values):
		for key, value in column_values.items():
			if sub_sql is None:
				sql = f"UPDATE `{table}` SET `{key}` = %s"

				self.connection.ping()
				with self.connection.cursor() as cursor:
					cursor.execute(sql, (value,))
					self.store()
			else:
				sql = f"UPDATE `{table}` SET `{key}` = %s WHERE {sub_sql}"
				values = value, *values
				values = tuple(values)

				self.connection.ping()
				with self.connection.cursor() as cursor:
					cursor.execute(sql, values)	
					self.store()		

	def count(self, table: str, sub_sql=None, *values):
		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			if sub_sql is None:
				sql = (f"SELECT COUNT(*) FROM `{table}`")
				cursor.execute(sql)
				rows = cursor.fetchall()
				for row in rows:
					for v in row.values():
						return v
			else: 
				sql = f"SELECT COUNT(*) FROM `{table}` WHERE {sub_sql};"
				cursor.execute(sql, values)
				rows = cursor.fetchall()
				for row in rows:
					for v in row.values():
						return v

	def view_all(self, table: str):
		self.connection.ping() # reconnecting mysql
		with self.connection.cursor() as cursor:
			sql = (f"SELECT * FROM `{table}`")
			sql_describe = (f"DESCRIBE `{table}`")

			table = PrettyTable()

			field_names = []
			values_list = []

			cursor.execute(sql_describe)

			fields = cursor.fetchall() 
			for field in fields:
				field_names.append(field['Field'])

			table.field_names = [field_name for field_name in field_names]

			cursor.execute(sql)

			values = cursor.fetchall()

			for row in values:
				table.add_row(row.values())

			return table

	def view(self, table: str, ids: tuple):
		self.connection.ping() # reconnecting mysql
		with self.connection.cursor() as cursor:
			ids = ', '.join(map(str, ids))
			sql = (f"SELECT * FROM `{table}` WHERE `id` IN({ids})")

			sql_describe = (f"DESCRIBE `{table}`")

			table = PrettyTable()

			field_names = []
			values_list = []

			cursor.execute(sql_describe)

			fields = cursor.fetchall() 
			for field in fields:
				field_names.append(field['Field'])

			table.field_names = [field_name for field_name in field_names]

			cursor.execute(sql)

			values = cursor.fetchall()

			for row in values:
				table.add_row(row.values())

			return table

	def find(self, table: str, sql: str, *values):
		sub_sql = (f"SELECT * FROM `{table}` WHERE {sql}")

		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			cursor.execute(sql, values)
			rows = cursor.fetchall()

		return rows

	def find_one(self, table: str, sql: str, *values):
		sub_sql = (f"SELECT * FROM `{table}` WHERE {sql} LIMIT 1;")

		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			cursor.execute(sql, values)
			rows = cursor.fetchall()

		return rows

	def trash(self, table: str, field_ids: tuple):
		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			field_ids = ", ".join(map(str, field_ids))
			sql = (f"DELETE FROM `{table}` WHERE `id` IN({field_ids})")
			cursor.execute(sql)
			self.store()

	def trash_sql(self, table: str, sql: str, *values):
		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			sub_sql = (f"DELETE FROM `{table}` WHERE {sql}")
			cursor.execute(sub_sql, values)
			self.store()

	def wipe(self, table: str):
		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			sql = (f"TRUNCATE `{table}`")
			cursor.execute(sql)
			self.store()

	def nuke(self, table: str):
		self.connection.ping()  # reconnecting mysql
		with self.connection.cursor() as cursor:
			sql = (f"DROP TABLE IF EXISTS `{table}`")
			cursor.execute(sql)
			self.store()

class sqlite(Base):

	def __init__(self, database: str):
		super(sqlite, self).__init__()

		# host=None, port=None, user=None, password=None, database=None
		try:
			self.database = database
			self.connection = sqlite3.connect(self.database)
			self.cursor = self.connection.cursor()

		except Exception as ex:
			raise ex


	def load(self, table: str, ids: tuple):
		with self.connection:
			return self.cursor.execute(Base._load(table, ids)).fetchall()

	def load_all(self, table: str):
		with self.connection:
			return self.cursor.execute(Base._load_all(table)).fetchall()

	def dispense(self, table: str):
		with self.connection:
			sql = (
				f"""
					CREATE TABLE IF NOT EXISTS {table} (
	    				id INTEGER PRIMARY KEY AUTOINCREMENT
				);"""
				)
			self.cursor.execute(sql)

	def add(self, table: str, field: str, type_: str):
		type_ = type_.lower().strip().split(':')

		'''
		*** input: instance_of_the_class.add(table, field, 'varchar:255', previous_field)
		***  output: type_ = ['varchar', '255']
		'''
		
		
		# null
		if (type_[0] == 'varchar'):

			sql = (f"ALTER TABLE `{table}` ADD `{field}` VARCHAR({type_[1]}) NULL DEFAULT NULL;")

		if (type_[0] == 'text'):

			sql = (f"ALTER TABLE `{table}` ADD `{field}` TEXT NULL DEFAULT NULL;")

		if (type_[0] == 'int'):

			sql = (f"ALTER TABLE `{table}` ADD `{field}` INTEGER({type_[1]}) NULL DEFAULT NULL;")


		# type_[1] == 'ct'. for example: dt:ct (ct - currentTimeStamp)
		if (type_[0] == 'dt' and type_[1] == 'ct'):

			sql = (f"ALTER TABLE `{table}` ADD `{field}` DATETIME NOT NULL DEFAULT ((DATETIME('now')));")


		if (type_[0] == 'id'):
			field += '_id'
			sql = (f"ALTER TABLE `{table}` ADD `{field}` INTEGER(11);")
			sql_create_index = (f"CREATE UNIQUE INDEX {field} ON {table} ({field});")


		if (type_[0] == 'bool') or (type_[0] == 'tint' and type_[1] == '1'):
			sql = (f"ALTER TABLE `{table}` ADD `{field}` BOOLEAN(1) NULL DEFAULT NULL;")


		if (type_[0] == 'tint' and type_[1] == '0'):
			sql = (f"ALTER TABLE `{table}` ADD `{field}` TINYINT NULL DEFAULT NULL;")


		if (type_[0] == 'bint'):
			sql = (f"ALTER TABLE `{table}` ADD `{field}` BIGINT NULL;")


		with self.connection:
			try:
				self.cursor.execute(sql)

				if type_[0] == 'id':
					self.cursor.execute(sql_create_index)

			except sqlite3.OperationalError:
				pass # skip duplicate fields error


	def puts(self, table: str, column_values: dict):
		for key, value in column_values.items():
			if isinstance(value, str):
					if (len(value) <= 191):
						sql_create = (f"ALTER TABLE `{table}` ADD `{key}` VARCHAR(191) NULL DEFAULT NULL")

					else:
						sql_create = (f"ALTER TABLE `{table}` ADD `{key}` TEXT NULL DEFAULT NULL")
		
			if isinstance(value, int):
				sql_create = (f"ALTER TABLE `{table}` ADD `{key}` INTEGER(11) NULL DEFAULT NULL")

			with self.connection:
				try:
					self.cursor.execute(sql_create)
				except sqlite3.OperationalError:
					pass 

		self.insert(table, column_values)


	def insert(self, table: str, column_values: dict):
		with self.connection: 
			self.cursor.execute(Base._insert(table, column_values)[0], \
				Base._insert(table, column_values)[1])

	def exec(self, query: str, *values):
		with self.connection:
			return self.cursor.execute(query, values).fetchall()

	def recent(self, table: str, order_by_field: str):
		with self.connection:
			sql = (f"SELECT * FROM `{table}` ORDER BY `{order_by_field}` DESC LIMIT 1")
			return self.cursor.execute(sql).fetchone()
			
	def read(self, table: str, fields: tuple, sub_sql: str=None, *values):
		fields = "`" + "`, `".join(fields) + "`"
		with self.connection:
			if sub_sql is None:
				sql = (f"SELECT {fields} FROM `{table}`")
			else:
				sql = (f"SELECT {fields} FROM `{table}` WHERE {sub_sql}")
			return self.cursor.execute(sql, values).fetchall()

	def read_one(self, table: str, fields: tuple, sub_sql: str=None, *values):
		fields = "`" + "`, `".join(fields) + "`"
		with self.connection:
			if sub_sql is None:
				sql = (f"SELECT {fields} FROM `{table}` LIMIT 1")
			else:
				sql = (f"SELECT {fields} FROM `{table}` WHERE {sub_sql} LIMIT 1")

			return self.cursor.execute(sql, values).fetchall()


	def update(self, table: str, column_values: dict, sub_sql: str=None, *values):
		with self.connection:
			for key, value in column_values.items():
				if sub_sql is None:
					sql = f"UPDATE `{table}` SET `{key}` = ?"
					self.execute(sql, (value,))
				else:
					sql = f"UPDATE `{table}` SET `{key}` = ? WHERE {sub_sql}"
					values = value, *values
					values = tuple(values)
					self.cursor.execute(sql, values)				

	def count(self, table: str, sub_sql=None, *values):
		with self.connection:
			items = []
			if sub_sql is None:
				sql = (f"SELECT COUNT(*) FROM `{table}`")
				for row in self.cursor.execute(sql).fetchall():
					items.append(f"{row[0]}")
			else: 
				sql = f"SELECT COUNT(*) FROM `{table}` WHERE {sub_sql};"
				for row in self.cursor.execute(sql, values).fetchall():
					items.append(f"{row[0]}")
		return "".join(items)

	def find(self, table: str, sql: str, *values):
		sub_sql = (f"SELECT * FROM `{table}` WHERE {sql};")
		with self.connection:
			return self.cursor.execute(sub_sql, values).fetchall()

	def find_one(self, table: str, sql: str, *values):
		sub_sql = (f"SELECT * FROM `{table}` WHERE {sql} LIMIT 1;")

		with self.connection:
			return self.cursor.execute(sub_sql, values).fetchall()

	def view(self, table: str, ids: tuple, *values):
		field_ids = ", ".join(map(str, ids))
		with self.connection:
			sql = (f"SELECT * FROM `{table}` WHERE `id` IN({field_ids})")
			self.cursor.execute(sql, values)
			table = from_db_cursor(self.cursor)
			return table

	def view_all(self, table: str):
		with self.connection:
			sql = (f"SELECT * FROM `{table}`")
			self.cursor.execute(sql)
			table = from_db_cursor(self.cursor)
			return table
			 
	def trash(self, table: str, field_ids: tuple):
		field_ids = ", ".join(map(str, field_ids))
		with self.connection:
			sql = (f"DELETE FROM `{table}` WHERE `id` IN({field_ids})")
			self.cursor.execute(sql)

	def trash_sql(self, table: str, sub_sql: str, *values):
		with self.connection:
			sql = (f"DELETE FROM `{table}` WHERE {sub_sql};")
			self.cursor.execute(sql, values)

	def wipe(self, table):
		with self.connection:
			sql = (f"DELETE FROM `{table}`")
			self.cursor.execute(sql)

	def nuke(self, table: str):
		with self.connection:
			sql = (f"DROP TABLE IF EXISTS `{table}`")
			self.cursor.execute(sql)
			