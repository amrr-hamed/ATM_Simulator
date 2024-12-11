import sqlite3
import threading
class Database:
    def __init__(self, db_name="atm_simulator.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_holder_name TEXT NOT NULL,
            password TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0.0
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            transaction_type TEXT CHECK(transaction_type IN ('Deposit', 'Withdrawal', 'Balance Inquiry')) NOT NULL,
            amount REAL NOT NULL CHECK(amount >= 0),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(account_id)
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS atms (
            atm_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            status TEXT CHECK(status IN ('Active', 'Inactive')) NOT NULL DEFAULT 'Active',
            cash_level REAL NOT NULL DEFAULT 0.0
        )
        ''')

        self.connection.commit()

    def close(self):
        self.connection.close()

  
