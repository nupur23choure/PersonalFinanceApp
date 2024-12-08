import sqlite3

class MonthlyReport:
    def __init__(self, database, user_id):
        self.connect = sqlite3.connect(database)
        self.cursor = self.connect.cursor()
        self.user_id = user_id

    def get_total(self, trans_type, year, month):
        try:
            self.cursor.execute('''
                SELECT SUM(amount) FROM transactions 
                WHERE user_id=? AND transaction_type=?  
                AND substr(date, 1, 4) = ? AND substr(date, 6, 2) = ?
            ''', (self.user_id, trans_type, year, month))    
            r = self.cursor.fetchone()
            return r[0] if r[0] is not None else 0  
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def total_income(self, trans_type, year, month):
        return self.get_total(trans_type, year, month)

    def total_expense(self, trans_type, year, month):
        return self.get_total(trans_type, year, month)

    def monthly_saving(self, year, month):
        income = self.total_income('income', year, month)  
        expense = self.total_expense('expense', year, month)  
        saving = income - expense 
        return saving    

    def generate_month_report(self, year, month):
        income = self.total_income('income', year, month)
        expense = self.total_expense('expense', year, month)
        saving = self.monthly_saving(year, month)

        report = {
            "Total Income": income,
            "Total Expense": expense,
            "Total Saving": saving
        }
        
        print("----Monthly Report-----")
        for key, value in report.items():
            print(f"{key}: {value:.2f}")
        return report

    def close(self):
        if self.connect:
            self.connect.close()
