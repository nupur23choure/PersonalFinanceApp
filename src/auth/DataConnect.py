import sqlite3

class DataConnect():
    def __init__(self, database):
        self.database = database
        self.connect = None
        self.cursor = None
    def create_connection(self):
        try:
            self.connect = sqlite3.connect(self.database)
            self.cursor = self.connect.cursor()
        except sqlite3.Error as e:
            print(f'Error connecting to database: {e}')    

    def create_table(self):
        table = '''
           CREATE TABLE IF NOT EXISTS user_data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT, 
            email TEXT UNIQUE,
            password TEXT UNIQUE                                                 
        );'''
        self.cursor.execute(table)
        self.connect.commit()

    def close(self):
        if self.connect:
           self.connect.close()
           