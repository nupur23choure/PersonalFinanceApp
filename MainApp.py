# main_app.py
from src.auth.DataConnect import DataConnect
from src.auth.UserRegistration import UserRegistration
from src.auth.UserLogin import UserLogin
from src.finance.Transaction import Transaction
from src.finance.AddTransaction import AddTransaction
from src.finance.UpdateTransaction import UpdateTransaction
from src.finance.DeleteTransaction import DeleteTransaction
from src.finance.ViewTransaction import ViewTransaction
from src.report.MonthlyReport import MonthlyReport
from src.report.YearlyReport import YearlyReport
from src.budget.SetBudget import SetBudget
from src.persistence.BackupManager import BackupManager

class MainApp:
    def __init__(self, database_path):
        self.database_path = database_path
        self.is_logged_in = False
        self.user_id = None

    def user_authentication(self):
        while True:
            print("-----Welcome to Personal Finance App-----")
            print("1. Register")
            print("2. Login")
            print("3. Finance Menu")
            print("4. Backup")
            print("5. Exit")
            choice = input("Choose 1/2/3/4: ")

            if choice == '1':
                username = input("Enter your name: ")
                email = input("Enter your email: ")
                password1 = input("Enter your password: ")
                password2 = input("Confirm password: ")
                register = UserRegistration(database_path, username, password1, password2, email)
                register.insert_user()

            elif choice == '2':
                username = input("Enter your name: ")
                password = input("Enter your password: ")
                login = UserLogin(database_path, username, password)
                self.user_id = login.user_login()  # Assign user_id based on login
                if self.user_id:  
                    self.is_logged_in = True

            elif choice == '3':
                if not self.is_logged_in:
                    print("Please log in first to access the finance menu.")
                else:
                    self.finance_menu()

            elif choice == '4':
                backup_dir = 'backup'
                manager = BackupManager(database_path, backup_dir)
                manager.backup_database()  
                manager.restore_database()  

            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")

    def finance_menu(self):
      while True:
        print("------Finance Menu-------")
        print("1. View Transactions")
        print("2. Add Transaction")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Report")
        print("6. Budget")
        print("7. Back to Main Menu")
        choice = input("Choose an option: ")

        if choice == '1':
            print("View Transactions")
            transaction = Transaction(self.database_path)
            transaction.create_connection()
            transaction.create_table_transaction()

            view_trans = ViewTransaction(self.database_path, self.user_id)
            view_trans.view_transaction()

        elif choice == '2':
            print("Add Transactions")
            date = input("Enter the transaction date (YYYY-MM-DD): ")
            amount = float(input("Enter the transaction amount: "))
            category = input("Enter the category food/rent/shopping/travel: ")
            description = input("Enter a description: ")
            transaction_type = input("Enter transaction type (income/expense): ")

            transaction = Transaction(self.database_path)
            transaction.create_connection()
            transaction.create_table_transaction()

            add = AddTransaction(self.database_path, self.user_id)
            add.add_transaction(date, amount,category, description, transaction_type)
            add.close()
            transaction.close()

        elif choice == '3':
            print("Update Transaction")
            trans_id = input("Enter the transaction id to update: ")
            amount = float(input("Enter the new transaction amount: "))
            category = input("Enter the category food/rent/shopping/travel: ")
            description = input("Enter the description: ")
            trans_type = input("Enter transaction type (income/expense): ")

            transaction = Transaction(self.database_path)
            transaction.create_connection()
            transaction.create_table_transaction()

            update = UpdateTransaction(self.database_path, self.user_id)
            update.update_transaction(trans_id, amount, category, description, trans_type)
            update.close()
            transaction.close()
            
        elif choice == '4':
            print("Delete Transaction")
            trans_id = input("Enter the transaction id to delete: ")

            transaction = Transaction(self.database_path)
            transaction.create_connection()
            transaction.create_table_transaction()

            delete = DeleteTransaction(self.database_path, self.user_id)
            delete.delete_transaction(trans_id)
            delete.close()
            transaction.close()

        elif choice == '5':
              self.finance_report()

        elif choice == '6':
            self.budget_menu()

        elif choice == '7':
            print("Returning to Main Menu.")
            break
        else:
            print("Invalid option.")

    def finance_report(self):
     while True:
        print("------Finance Report---------")
        print("1. Monthly Report")
        print("2. Yearly Report") 
        print("3. Back to Finance Menu")
        choice = input("Choose 1/2/3: ")

        if choice == '1':
            year = input("Enter Year YYYY: ")
            month = input("Enter Month MM: ")
            month_report = MonthlyReport(self.database_path, self.user_id)
            month_report.generate_month_report(year,month)
            month_report.close()

        if choice == '2':
            year = input("Enter Year YYYY: ")
            month_report = YearlyReport(self.database_path, self.user_id)
            month_report.generate_year_report(year)
            month_report.close()    

        elif choice == '3':
            print("return to finance menu")
            break
        else:
            print("invalid choice")  

    def budget_menu(self):
      while True:
        print("----Budget Management----")
        print("1. Set Monthly Budget")
        print("2. View Budget and Spending")
        print("3. Update Budget")
        print("4. Delete Budget")
        print("5. Back to Main Menu")
        choice = input("Choose an option (1/2/3/4/5): ")

        if choice == '1':
            print("Set Monthly Budget")
            category = input("Enter the category food/rent/shopping/travel: ")
            amount = float(input("Enter the budget amount: "))
            month = input("Enter the month for the budget (YYYY-MM): ")

            set_budget = SetBudget(self.database_path, self.user_id)
            set_budget.set_budget(category, amount, month)
            set_budget.close()

        elif choice == '2':
            print("View Budget and Spending")
            
            category = input("Enter the category food/rent/shopping/travel: ")
            month = input("Enter the month to view (YYYY-MM): ")

            set_budget = SetBudget(self.database_path, self.user_id)
            budget_limit = set_budget.get_budget_limit(category, month)
            total_spent = set_budget.get_total_spent(category, month)

            print(f"Category: {category}")
            print(f"Budget for {month}: ${budget_limit:.2f}")
            print(f"Total Spent in {month}: ${total_spent:.2f}")

            # Notify user if budget exceeded or nearing limit
            set_budget.check_budget(category, month, budget_limit, total_spent)
            set_budget.close()

        elif choice == '3':
            print("Update Budget")
            
            category = input("Enter the category food/rent/shopping/travel: ")
            new_amount = float(input("Enter the budget new amount: "))
            month = input("Enter the month to view (YYYY-MM): ")
            set_budget = SetBudget(self.database_path, self.user_id)
            set_budget.update_budget(category, new_amount, month)
            set_budget.close()

        elif choice == '4':
           print("Delete Budget")

           category = input("Enter the category food/rent/shopping/travel: ")
           month = input("Enter the month to delete (YYYY-MM): ")
           set_budget = SetBudget(self.database_path, self.user_id)
           set_budget.delete_budget(category, month)
           set_budget.close()

        elif choice == '5':
            print("Returning to main menu...")
            break
        else:
            print("Invalid choice. Please try again.")                   

database_path = 'data/users.db'
db = DataConnect(database_path)
db.create_connection()
db.create_table()

app = MainApp(database_path)
app.user_authentication()
db.close()
