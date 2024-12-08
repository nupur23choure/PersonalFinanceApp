import unittest
import sqlite3
from src.auth.UserRegistration import UserRegistration
from src.auth.UserLogin import UserLogin  

class TestAuthentication(unittest.TestCase):
    def setUp(self): 
        self.database = sqlite3.connect(":memory:")
        self.cursor = self.database.cursor()
        self.cursor.execute('''
            CREATE TABLE user_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        self.database.commit()
        self.reg = UserRegistration(
            database=":memory:",  
            username="testuser",
            password1="password123",
            password2="password123",
            email="testuser@example.com"
        )
        self.reg.connect = self.database
        self.reg.cursor = self.cursor

    def tearDown(self):
        self.cursor.close()
        self.database.close()

    def test_user_registration(self):
        self.reg.insert_user()
        self.cursor.execute("SELECT * FROM user_data WHERE username = ?", ("testuser",))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "testuser")
        self.assertEqual(user[2], "testuser@example.com")

    def test_user_registration_duplicate(self):
        self.reg.insert_user()
        with self.assertRaises(sqlite3.IntegrityError):
            self.reg.insert_user()    

    def test_user_login_success(self):
        self.reg.insert_user()
        login = UserLogin(
            database=":memory:", 
            username="testuser",
            password="password123"
        )
        login.connect = self.database
        login.cursor = self.cursor

        user_id = login.user_login()   
        self.assertIsNotNone(user_id) 
        self.assertEqual(user_id, 1)  

    def test_user_login_fail(self):
        self.reg.insert_user()
        login = UserLogin(
            database=":memory:", 
            username="testfail", 
            password="password123"
        )
        login.connect = self.database
        login.cursor = self.cursor

        user_id = login.user_login()  
        self.assertIsNone(user_id) 

if __name__ == "__main__":
    unittest.main()
