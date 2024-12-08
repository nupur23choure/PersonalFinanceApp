import unittest
import sqlite3
from src.finance.AddTransaction import AddTransaction
from src.finance.DeleteTransaction import DeleteTransaction
from src.finance.UpdateTransaction import UpdateTransaction
from src.finance.ViewTransaction import ViewTransaction

class TestFinance(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row 
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                amount REAL,
                category TEXT,
                description TEXT,
                transaction_type TEXT
            )
        ''')
        self.conn.commit()
        self.user_id = 1
        self.transaction = AddTransaction(':memory:', self.user_id)
        self.transaction.connect = self.conn
        self.transaction.cursor = self.cursor
        self.delete_transaction = DeleteTransaction(':memory:', self.user_id)
        self.delete_transaction.connect = self.conn
        self.delete_transaction.cursor = self.cursor
        self.update_transaction = UpdateTransaction(':memory:', self.user_id)
        self.update_transaction.connect = self.conn
        self.update_transaction.cursor  = self.cursor
        self.view_transaction = ViewTransaction(':memory:', self.user_id)
        self.view_transaction.connect = self.conn
        self.view_transaction.cursor = self.cursor

    def tearDown(self):
        self.transaction.close()
        self.delete_transaction.close()
        self.update_transaction.close()
        self.view_transaction.close()
        self.conn.close()

    def test_add_transaction_success(self):
        self.transaction.add_transaction('2024-11-10', 100.0, 'food', 'groceries', 'expense')
        self.cursor.execute('SELECT user_id, date, amount, category, description, transaction_type FROM transactions WHERE user_id = ?', (self.user_id,))
        result = self.cursor.fetchone()
        expected = (self.user_id, '2024-11-10', 100.0, 'food', 'groceries', 'expense')
        self.assertEqual(tuple(result), expected)

    def test_delete_transaction(self):
        self.transaction.add_transaction('2024-11-10', 100.0, 'food', 'groceries', 'expense')
        self.cursor.execute('SELECT transaction_id FROM transactions WHERE user_id = ?', (self.user_id,))
        transaction = self.cursor.fetchone()
        if transaction:
            trans_id = transaction['transaction_id']
            print(f"Fetched Transaction ID: {trans_id}")
        else:
            self.fail("Transaction not found after adding.")
        self.delete_transaction.delete_transaction(trans_id)
        self.cursor.execute('SELECT * FROM transactions WHERE transaction_id = ?', (trans_id,))
        result = self.cursor.fetchone()
        print(f"Database state after deletion: {result}")
        self.assertIsNone(result, "Transaction was not deleted")

    def test_update_transaction(self):
        self.transaction.add_transaction('2024-11-10', 100.0, 'food', 'groceries', 'expense')
        self.cursor.execute('SELECT transaction_id FROM transactions WHERE user_id = ?', (self.user_id,))
        transaction = self.cursor.fetchone()
        if transaction:
            trans_id = transaction['transaction_id']
            print(f"Fetched Transaction ID for update: {trans_id}")
        else:
            self.fail("Transaction not found for update test.")
        self.update_transaction.update_transaction(
            trans_id, 150.0, 'utilities', 'electricity bill', 'expense'
        )
        self.cursor.execute('SELECT amount, category, description, transaction_type FROM transactions WHERE transaction_id = ?', (trans_id,))
        updated_transaction = self.cursor.fetchone()
        expected = (150.0, 'utilities', 'electricity bill', 'expense')
        self.assertEqual(tuple(updated_transaction), expected, "Transaction update did not match the expected values.")

    def test_view_transaction(self):
        transactions = [
            ('2024-11-10', 100.0, 'food', 'groceries', 'expense'),
            ('2024-11-11', 200.0, 'utilities', 'electricity bill', 'expense'),
        ]
        for date, amount, category, description, transaction_type in transactions:
            self.transaction.add_transaction(date, amount, category, description, transaction_type)

        self.cursor.execute('SELECT * FROM transactions WHERE user_id = ?', (self.user_id,))
        expected_results = self.cursor.fetchall()
        print(f"Expected Results: {expected_results}")

        self.view_transaction.view_transaction()

        self.assertEqual(len(transactions), len(expected_results), "Transaction count mismatch.")


if __name__ == '__main__':
    unittest.main()
