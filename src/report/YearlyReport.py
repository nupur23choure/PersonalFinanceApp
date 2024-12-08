import sqlite3

class YearlyReport:
    def __init__(self, database, user_id):
        self.connect = sqlite3.connect(database)
        self.cursor = self.connect.cursor()
        self.user_id = user_id

    def get_total(self, trans_type, year):
        try:
            self.cursor.execute('''
                SELECT SUM(amount) 
                FROM transactions 
                WHERE user_id = ? 
                AND transaction_type = ?  
                AND substr(date, 1, 4) = ? 
            ''', (self.user_id, trans_type, year))
            result = self.cursor.fetchone()
            return result[0] if result[0] is not None else 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0

    def yearly_saving(self, year):
        income = self.get_total('income', year)
        expense = self.get_total('expense', year)
        return income - expense

    def generate_year_report(self, year):
        income = self.get_total('income', year)
        expense = self.get_total('expense', year)
        saving = income - expense

        report = {
            "Total Income": income,
            "Total Expense": expense,
            "Total Saving": saving
        }

        print("----Yearly Report-----")
        for key, value in report.items():
            print(f"{key}: {value:.2f}")
        return report

    def close(self):
        if self.connect:
            self.connect.close()
