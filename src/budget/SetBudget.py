import sqlite3
import logging
class SetBudget:
    
    def __init__(self, database, user_id):
        self.connect = sqlite3.connect(database)
        self.cursor = self.connect.cursor()
        self.user_id = user_id

    def set_budget(self,category, amount, month):
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO budget (user_id, category, month, amount)
                VALUES (?, ?, ?, ?)
            ''', (self.user_id, category, month, amount))
            self.connect.commit()
            print(f"Budget set for user {self.user_id}: {category} - ${amount:.2f} in {month}")
        except sqlite3.Error as e:
            print(f"Error: Could not set budget: {e}")
        
    def get_budget_limit(self, category, month): 
        try:
            self.cursor.execute('''
                SELECT amount FROM budget
                WHERE user_id = ? AND category = ? AND month = ?
            ''', (self.user_id, category, month))
            
            result = self.cursor.fetchone()
            return result[0] if result else 0.0  
        except sqlite3.Error as e:
            print(f"Error: Could not retrieve budget limit: {e}")
            return 0.0
        
    def get_total_spent(self, category, month):
        try:
            year, month_part = month.split("-")
            self.cursor.execute('''
                SELECT SUM(amount) FROM transactions
                WHERE user_id = ? AND category = ? AND substr(date, 1, 4) = ? AND substr(date, 6, 2) = ?
                AND transaction_type = 'expense'
            ''', (self.user_id, category, year, month_part))
            
            result = self.cursor.fetchone()
            return result[0] if result[0] is not None else 0.0
        except sqlite3.Error as e:
            print(f"Error: Could not calculate total spent: {e}")
            return 0.0

    def check_budget(self, category, month, budget_limit, total_spent):
        try: 
            if budget_limit == 0: 
                logging.info(f"No budget set for {category} in {month}.") 
                return 
            if total_spent > budget_limit: 
                logging.warning(f"Alert: You have exceeded your budget for {category} in {month}!") 
                logging.warning(f"Budget Limit: ${budget_limit:.2f}, Total Spent: ${total_spent:.2f}") 
            elif total_spent > 0.8 * budget_limit: 
                logging.warning(f"Warning: You are close to exceeding your budget for {category} in {month}.") 
                logging.warning(f"Budget Limit: ${budget_limit:.2f}, Total Spent: ${total_spent:.2f}") 
            else: 
                logging.info(f"Good job! You are within your budget for {category} in {month}.") 
                logging.info(f"Budget Limit: ${budget_limit:.2f}, Total Spent: ${total_spent:.2f}") 
        except Exception as e: 
                logging.error(f"Error checking budget: {e}")

    def delete_budget(self, category, month):
        try:
            self.cursor.execute('''
                DELETE FROM budget
                WHERE user_id = ? AND category = ? AND month = ?
            ''', (self.user_id, category, month))
            self.connect.commit()

            if self.cursor.rowcount > 0:
                print(f"Budget deleted: {category} for {month}.")
            else:
                print(f"No budget found to delete for {category} in {month}.")
        except sqlite3.Error as e:
            print(f"Error: Could not delete budget: {e}")

    def update_budget(self, category, new_amount, month):     
        try:
            self.cursor.execute('''
                UPDATE budget
                SET amount = ?
                WHERE user_id = ? AND category = ? AND month = ?
            ''', (new_amount, self.user_id, category, month))
            self.connect.commit()

            if self.cursor.rowcount > 0:
                print(f"Budget updated: {category} - ${new_amount:.2f} for {month}.")
            else:
                print(f"No budget found to update for {category} in {month}.")
        except sqlite3.Error as e:
            print(f"Error: Could not update budget: {e}")       

    def close(self):
        if self.connect:
            self.connect.close()
                    