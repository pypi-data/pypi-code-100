''' РАБОТА С БД'''

import sqlite3

class Manager_SQL:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_table(self,  name_table):
        '''создание БД'''

        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {name_table} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        messenger NULL,
                        user_id INT,
                        name NULL,
                        city NULL,
                        url_city NULL,
                        utc INT NULL,
                        gps NULL)''')
        self.save_db()
        self.close_db()

    def insert_data(self, values, name_table):
        '''запись в БД если такая запись уже есть то обновить ее'''

        if len(self.select_row(name_table=name_table, user_id=values[1], messenger=f'"{values[0]}"', close=False)) == 0:
            self.cursor.execute(f'''INSERT INTO {name_table}(messenger, user_id, name, city, url_city, utc, gps) VALUES (?, ?, ?, ?, ?, ?, ?)''', values)
        else:
            self.update_row(self, [name_table, values[1], f'"{values[0]}"', tuple(values[2:])])
        self.save_db()
        self.close_db()

    def select_row(self, name_table, user_id, messenger, close=True):
        '''получить строку из БД с инфо о пользователе'''

        x = self.cursor.execute(f'''SELECT * FROM {name_table} WHERE user_id == {user_id} AND messenger == {messenger}''').fetchall()
        if close:
            self.save_db()
            self.close_db()
        return x

    def update_row(self, *args):
        '''обновить данные'''

        self.cursor.execute(f'''UPDATE {args[1][0]} SET name = ?, city = ?, url_city = ?, utc = ?, gps = ?  WHERE user_id == {args[1][1]} AND messenger == {args[1][2]}''', args[1][3])


    def save_db(self):
        self.connection.commit()

    def close_db(self):
        self.connection.close()
