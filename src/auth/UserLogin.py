import sqlite3

class UserLogin():
    def __init__(self, database, username, password):
        self.connect = sqlite3.connect(database)
        self.cursor = self.connect.cursor()
        self.username = username
        self.password = password    
    def user_login(self):
        try:
            self.cursor.execute('SELECT id FROM user_data WHERE username=? AND password=?', (self.username, self.password))
            result = self.cursor.fetchone()
            if result:
                print("Login successful!")
                return result[0]   
            else:
                print("Invalid username or password.")
                return None   
        except sqlite3.Error as e:
            print(f'Error during login {e}')
            return None
