import unittest
import sqlite3
from src.budget.SetBudget import SetBudget

class TestSetBudget(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT,
                amount REAL,
                month TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        self.budget = SetBudget(':memory:', self.user_id)
        self.budget.connect = self.conn
        self.budget.cursor = self.cursor

    def tearDown(self):
        self.budget.close()
        self.conn.close()

    def test_set_budget(self):
        self.budget.set_budget('food', 500, '2024-11')
        self.cursor.execute('SELECT * FROM budget WHERE user_id = ? AND category = ? AND month = ?', (self.user_id, 'food', '2024-11'))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[3], 500)

    def test_get_budget_limit(self):
        self.budget.set_budget('food', 500, '2024-11')
        limit = self.budget.get_budget_limit('food', '2024-11')
        self.assertEqual(limit, 500)

    def test_get_total_spent(self):
        self.cursor.execute('''
            INSERT INTO transactions (user_id, date, amount, category, description, transaction_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.user_id, '2024-11-10', 100, 'food', 'groceries', 'expense'))
        self.conn.commit()
        total_spent = self.budget.get_total_spent('food', '2024-11')
        self.assertEqual(total_spent, 100)

    def test_check_budget(self):
        self.budget.set_budget('food', 500, '2024-11') 
        self.cursor.execute(''' INSERT INTO transactions (user_id, date, amount, category, description, transaction_type) 
         VALUES (?, ?, ?, ?, ?, ?) ''', (self.user_id, '2024-11-10', 100, 'food', 'groceries', 'expense')) 
        self.conn.commit() 

        limit = self.budget.get_budget_limit('food', '2024-11') 
        total_spent = self.budget.get_total_spent('food', '2024-11') 
        with self.assertLogs(level='INFO') as log: self.budget.check_budget('food', '2024-11', limit, total_spent) 
        self.assertIn('INFO:root:Good job! You are within your budget for food in 2024-11.', log.output) 
        self.assertIn('INFO:root:Budget Limit: $500.00, Total Spent: $100.00', log.output)

    def test_delete_budget(self):
        self.budget.set_budget('food', 500, '2024-11')
        self.budget.delete_budget('food', '2024-11')
        self.cursor.execute('SELECT * FROM budget WHERE user_id = ? AND category = ? AND month = ?', (self.user_id, 'food', '2024-11'))
        result = self.cursor.fetchone()
        self.assertIsNone(result)

    def test_update_budget(self):
        self.budget.set_budget('food', 500, '2024-11')
        self.budget.update_budget('food', 600, '2024-11')
        self.cursor.execute('SELECT amount FROM budget WHERE user_id = ? AND category = ? AND month = ?', (self.user_id, 'food', '2024-11'))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 600)

if __name__ == '__main__':
    unittest.main()
