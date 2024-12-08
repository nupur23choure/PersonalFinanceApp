import sqlite3
class Budget:
    def __init__(self, database):
        self.database = database
        self.connect = None
        self.cursor = None

    def create_connection(self):
        try:
            self.connect = sqlite3.connect(self.database)
            self.cursor = self.connect.cursor()
            print("Connection established")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_table_budget(self):
        try:
            self.cursor.execute('DROP TABLE IF EXISTS budget')
            print("Table 'budget' dropped successfully")

            table = '''
               CREATE TABLE IF NOT EXISTS budget(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER, 
                category TEXT,
                amount REAL,
                month TEXT,
                FOREIGN KEY(user_id) REFERENCES user_data(id)                                                   
            );'''
            self.cursor.execute(table)
            print("Table 'budget' created successfully")

            self.connect.commit()
        except sqlite3.Error as e:
            print(f"Error during table operation: {e}")

    def close(self):
        if self.connect:
            self.connect.close()
            