import sqlite3
class Transaction:
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

    def create_table_transaction(self):
        table = '''CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            amount REAL,
            category TEXT,
            description TEXT,
            transaction_type TEXT,
            FOREIGN KEY(user_id) REFERENCES user_data(id)
        );'''
        self.cursor.execute(table)
        
        self.connect.commit()
    
    def close(self):
        if self.connect:
           self.connect.close()
