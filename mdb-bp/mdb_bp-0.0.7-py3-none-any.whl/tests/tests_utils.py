# import unittest
#
# from mdb_bp import driver
# from mdb_bp.bitmap import bitmap
#
# class MyTestCase(unittest.TestCase):
#     def test_basic_bitmap_set_and_retrieve(self):
#         bm = bitmap(bytearray(2))
#
#         self.assertEqual(bm.get(0), 0)
#         bm.set(0, 1)
#         self.assertEqual(bm.get(0), 1)
#
#     # def test_convert_column_to_value(self):
#     #     col = bytearray()
#
#     def test_basic_odbc_objects(self):
#         conn = driver.connect(
#             username="system",
#             password="biglove",
#             connection_protocol="tcp",
#             server_address="localhost",
#             server_port=8080,
#             database_name="master",
#             parameters={"interpolateParams": True},
#         )
#
#         stmt_use = conn.prepare("USE main")
#         result = stmt_use.exec()
#
#         print(result)
#
#     def test_basic_odbc_query(self):
#         conn = driver.connect(
#             username="system",
#             password="biglove",
#             connection_protocol="tcp",
#             server_address="localhost",
#             server_port=8080,
#             database_name="master",
#             parameters={"interpolateParams": True},
#         )
#
#         errored = False
#         try:
#             conn.query("SELECT * FROM skrt_skrt")
#
#         except Exception as err:
#             # Expect an error
#             errored = True
#
#         if not errored:
#             raise Exception("skrt_skrt didn't fail")
#
#         rows = conn.query("SELECT * FROM sys_sessions")
#
#         itr = iter(rows)
#
#         for row in itr:
#             print(row)
#
#     def test_basic_odbc_begin(self):
#         conn = driver.connect(
#             username="system",
#             password="biglove",
#             connection_protocol="tcp",
#             server_address="localhost",
#             server_port=8080,
#             database_name="master",
#             parameters={"interpolateParams": True},
#         )
#
#         class user:
#             def __init__(self, id, first, last, age, username):
#                 self.id = id
#                 self.first = first
#                 self.last = last
#                 self.age = age
#                 self.username = username
#
#         stmt = conn.prepare("CREATE DATABASE users")
#         result = stmt.exec()
#         print(result)
#
#         stmt = conn.prepare("USE users")
#         result = stmt.exec()
#         print(result)
#
#         stmt = conn.prepare(
#             "CREATE BLOCKCHAIN user TRADITIONAL ("
#             + "id uint64 PRIMARY KEY AUTO INCREMENT,"
#             + " first_name string size = 25 PACKED,"
#             + " last_name string size = 50 PACKED,"
#             + " age uint8,"
#             + " username string size=30 PACKED UNIQUE)")
#
#         result = stmt.exec()
#         print(result)
#
#         # Start a transaction
#         xact = conn.begin()
#
#         # Insert a value atomically
#         # stmt = conn.prepare(
#         #     "INSERT user (whipper_snapper, last_name, age, username)"
#         #     + " VALUES (\"Paul\", \"Smith\", 20, \"pdawgy\")")
#         errored = False
#         try:
#             result = xact.exec(
#                 "INSERT user (whipper_snapper, last_name, age, username)"
#                 + " VALUES (\"Paul\", \"Smith\", 20, \"pdawgy\")")
#             print(result)
#
#         except Exception:
#             errored = True
#             xact.rollback()
#
#         if not errored:
#             raise Exception("first insert didn't fail")
#
#         # Start another transaction
#         xact = conn.begin()
#
#         xact.exec(
#             "INSERT user (first_name, last_name, age, username) "
#             + "VALUES (\"it's NOT CHABOY\", \"Smith\", 45, \"NOT CHABOY\")")
#
#         # Rollback
#         xact.rollback()
#
#         # Start another transaction
#         xact = conn.begin()
#
#         # Query from that connection.
#         try:
#             rows = xact.query("SELECT * FROM user")
#         except Exception as err:
#             print(err)
#
#         itr = iter(rows)
#
#         for row in itr:
#             user = user(row[0], row[1], row[2], row[3], row[4])
#             print(user)
#             if user.username == "it's CHABOY":
#                 # Check for the rolled back record
#                 raise Exception("rollback unsuccessful")
#
#     def test_demo_setup(self):
#         conn = driver.connect(
#             username="system",
#             password="biglove",
#             connection_protocol="tcp",
#             server_address="localhost",
#             server_port=8080,
#             database_name="master",
#             parameters={"interpolateParams": True},
#         )
#
#         stmt = conn.prepare("CREATE DATABASE financial")
#         result = stmt.exec()
#         print(result)
#
#         stmt = conn.prepare("USE financial")
#         result = stmt.exec()
#         print(result)
#
#         stmt = conn.prepare(
#             "CREATE BLOCKCHAIN temp TRADITIONAL"
#             + " (symbol string primary = true packed,"
#             + " name string packed,"
#             + " sector string packed,"
#             + " price float32,"
#             + " dividend_yield float32,"
#             + " price_earning float32,"
#             + " earning_share float32,"
#             + " book_value float32,"
#             + " 52_week_low float32,"
#             + " 52_week_high float32,"
#             + " market_cap float64,"
#             + " EBITDA float64,"
#             + " sales float64,"
#             + " price_book_value float32,"
#             + " SEC_filings string packed)")
#
#         result = stmt.exec()
#         print(result)
#
#         stmt = conn.prepare(
#             "CREATE BLOCKCHAIN companies HISTORICAL PLUS ("
#             + "symbol string primary = true packed,"
#             + " name string packed unique nullable,"
#             + " sector string packed default = \"Undefined\")")
#         result = stmt.exec()
#         print(result)
#
#         stmt = conn.prepare(
#             "CREATE BLOCKCHAIN pricing SPARSE ("
#             + "symbol string primary = true packed,"
#             + " price float32, dividend_yield float32,"
#             + " price_earning float32,"
#             + " earning_share float32,"
#             + " book_value float32,"
#             + " 52_week_low float32 CHECK [52_week_high > 52_week_low],"
#             + " 52_week_high float32)")
#
#         result = stmt.exec()
#         print(result)
#
#         # Load the csv into temp
#         stmt = conn.prepare(
#             "INSERT INTO temp SELECT * FROM IMPORT = \"test_files/constituents-financials.csv\" (symbol string primary = true packed, name string packed, sector string packed, price float32, price_earning float32, dividend_yield float32, earning_share float32,  book_value float32, 52_week_low float32, 52_week_high float32, market_cap float64, EBITDA float64, sales float64, price_book_value float32, SEC_filings string packed)")
#         result = stmt.exec()
#         print(result)
#
#         stmt = conn.prepare("INSERT INTO companies SELECT symbol, name, sector FROM temp")
#         result = stmt.exec()
#         print(result)
#
#         stmt = conn.prepare("INSERT INTO pricing SELECT symbol, price, dividend_yield, price_earning, earning_share, book_value, 52_week_low, 52_week_high FROM temp")
#         result = stmt.exec()
#         print(result)
#
#         rows = conn.query("SELECT * FROM (SELECT pricing.symbol FROM pricing WHERE symbol = \"AAPL\") AS s JOIN (SELECT * FROM companies) AS c ON c.symbol = s.symbol")
#
#         itr = iter(rows)
#
#         for row in itr:
#             print(row)
#
#
#
# if __name__ == '__main__':
#     unittest.main()
