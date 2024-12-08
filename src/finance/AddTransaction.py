import sqlite3
class AddTransaction:
    
    def __init__(self, database, user_id):
        self.connect = sqlite3.connect(database)
        self.cursor = self.connect.cursor()
        self.user_id = user_id  

    def add_transaction(self, date, amount, category, description, transaction_type):
        try:
            self.cursor.execute('''
                INSERT INTO transactions (user_id, date, amount, category, description, transaction_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.user_id, date, amount, category,  description, transaction_type))
            self.connect.commit()
            print(f"Transaction added: {transaction_type} of {amount} on {date}")
        except sqlite3.Error as e:
            print(f"Error adding transaction: {e}")

    def close(self):
        if self.connect:
            self.connect.close()
