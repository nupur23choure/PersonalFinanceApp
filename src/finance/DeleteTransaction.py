import sqlite3
class DeleteTransaction:
    
    def __init__(self, database, user_id):
        self.connect = sqlite3.connect(database)
        self.cursor = self.connect.cursor()
        self.user_id = user_id

    def delete_transaction(self, trans_id):
        try:
            print(f"Attempting to update transaction {trans_id} for user {self.user_id}")
            self.cursor.execute(
                 '''
                DELETE  FROM transactions 
                WHERE (user_id = ? OR user_id IS NULL) AND transaction_id = ?

                ''',(self.user_id, trans_id)
            )
            if self.user_id:
             print("Transaction has been deleted successfully")
            self.connect.commit()
        
        except sqlite3.Error as e:
            print(f'Error: deleting transaction {e}')
   
    def close(self):
        if self.connect:
            self.connect.close()
            