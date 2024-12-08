import sqlite3

class UpdateTransaction:
    
    def __init__(self, database, user_id):
        self.connect = sqlite3.connect(database)
        self.cursor = self.connect.cursor()
        self.user_id = user_id

    def update_transaction(self, trans_id, amount, category, description, trans_type):
        try:
            print(f"Attempting to update transaction {trans_id} for user {self.user_id}")
            self.cursor.execute(
                '''
                UPDATE transactions 
                SET amount = ?, category = ?, description = ?, transaction_type = ? 
                WHERE (user_id = ? OR user_id IS NULL) AND transaction_id = ?
                ''',
                (amount, category, description, trans_type, self.user_id, trans_id)
            )
            print("Transaction updated successfully!")
            self.cursor.execute('SELECT * FROM transactions WHERE transaction_id = ?', (trans_id,))
            updated_row = self.cursor.fetchone()
            print("Updated transaction:", updated_row)
            self.connect.commit()

        except sqlite3.Error as e:    
            print(f'Error: updating transaction: {e}')  

    def close(self):
        if self.connect:
            self.connect.close()
