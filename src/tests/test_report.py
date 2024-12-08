import unittest
import sqlite3
from src.report.MonthlyReport import MonthlyReport
from src.report.YearlyReport import YearlyReport

class TestReport(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
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

        self.monthly_report = MonthlyReport(':memory:', self.user_id)
        self.monthly_report.connect = self.conn
        self.monthly_report.cursor = self.cursor

        self.yearly_report = YearlyReport(':memory:', self.user_id)
        self.yearly_report.connect = self.conn
        self.yearly_report.cursor = self.cursor

        self.transactions = [
            (self.user_id, '2024-01-15', 1000.0, 'salary', 'monthly income', 'income'),
            (self.user_id, '2024-01-20', 200.0, 'food', 'grocery shopping', 'expense'),
            (self.user_id, '2024-02-10', 1500.0, 'freelancing', 'side job', 'income'),
            (self.user_id, '2024-02-18', 500.0, 'rent', 'monthly rent', 'expense'),
        ]
        self.cursor.executemany('''
            INSERT INTO transactions (user_id, date, amount, category, description, transaction_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', self.transactions)
        self.conn.commit()

    def tearDown(self):
        self.monthly_report.close()
        self.yearly_report.close()
        self.conn.close()

    def test_monthly_report(self):
        report = self.monthly_report.generate_month_report('2024', '01')
        expected_report = {
            "Total Income": 1000.0,
            "Total Expense": 200.0,
            "Total Saving": 800.0,
        }
        self.assertEqual(report, expected_report)

        report = self.monthly_report.generate_month_report('2024', '02')
        expected_report = {
            "Total Income": 1500.0,
            "Total Expense": 500.0,
            "Total Saving": 1000.0,
        }
        self.assertEqual(report, expected_report)

    def test_yearly_report(self):
        report = self.yearly_report.generate_year_report('2024')
        expected_report = {
            "Total Income": 2500.0,
            "Total Expense": 700.0,
            "Total Saving": 1800.0,
        }
        self.assertEqual(report, expected_report)

    def test_monthly_saving(self):
        saving = self.monthly_report.monthly_saving('2024', '01')
        self.assertEqual(saving, 800.0)
        saving = self.monthly_report.monthly_saving('2024', '02')
        self.assertEqual(saving, 1000.0)

    def test_yearly_saving(self):
        saving = self.yearly_report.yearly_saving('2024')
        self.assertEqual(saving, 1800.0)

if __name__ == '__main__':
    unittest.main()
