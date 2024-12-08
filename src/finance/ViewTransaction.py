import sqlite3

class ViewTransaction:
    def __init__(self, database, user_id):
        self.connect = sqlite3.connect(database)
        self.connect.row_factory = sqlite3.Row  
        self.cursor = self.connect.cursor()
        self.user_id = user_id

    def view_transaction(self):
        try:
            self.cursor.execute('SELECT * FROM transactions WHERE user_id=?', (self.user_id,))
            view = self.cursor.fetchall()
            if view:
                for transaction in view:
                    print(f"Transaction ID: {transaction['transaction_id']}, Date: {transaction['date']}, "
                          f"Amount: {transaction['amount']}, Category: {transaction['category']}, "
                          f"Description: {transaction['description']}, Type: {transaction['transaction_type']}")
            else:
                print("No transaction found!")
        except sqlite3.Error as e:
            print(f'Error: view transaction error: {e}')

    def close(self):
        if self.connect:
            self.connect.close()
