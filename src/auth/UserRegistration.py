# UserRegistration.py
import sqlite3

class UserRegistration:
    def __init__(self, database, username, password1, password2, email):
        self.connect = sqlite3.connect(database)
        self.cursor = self.connect.cursor()  
        self.password1 = password1
        self.password2 = password2
        self.email = email
        self.username = username

    def check_password(self):
        if self.password1 == self.password2:
            print("Passwords match.")
            return True
        else:
            print("Passwords do not match!")
            return False

    def insert_user(self):
        if self.check_password():
            try:
                self.cursor.execute("""
                    INSERT INTO user_data (username, email, password)
                    VALUES (?, ?, ?)
                """, (self.username, self.email, self.password2))
                self.connect.commit()
                print("You have successfully created an account.")
            except sqlite3.IntegrityError as e:
                print("Error: This email is already registered.")
                raise e
    