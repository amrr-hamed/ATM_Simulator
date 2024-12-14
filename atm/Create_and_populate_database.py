import sqlite3
import random
import string
import threading
from datetime import datetime

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.lock = threading.Lock()  # Replace with a threading lock if needed

    def create_and_populate_database(self):
        """Creates and populates the database with initial data."""
        with self.lock:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()

            # Drop existing tables if they exist
            cursor.execute("DROP TABLE IF EXISTS accounts")
            cursor.execute("DROP TABLE IF EXISTS atms")
            cursor.execute("DROP TABLE IF EXISTS transactions")

            # Create the accounts table
            cursor.execute("""
                CREATE TABLE accounts (
                    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_holder_name TEXT NOT NULL,
                    password TEXT NOT NULL,
                    balance REAL NOT NULL
                )
            """)

            # Create the ATMs table
            cursor.execute("""
                CREATE TABLE atms (
                    atm_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT NOT NULL,
                    cash_level REAL NOT NULL,
                    status TEXT NOT NULL
                )
            """)

            # Create the transactions table
            cursor.execute("""
                CREATE TABLE transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER NOT NULL,
                    transaction_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
                )
            """)

            # Generate and populate the accounts table with 100 random accounts
            accounts = []
            for _ in range(100):
                name = ''.join(random.choices(string.ascii_letters + " ", k=10))
                password = ''.join(random.choices(string.digits, k=4))
                balance = round(random.uniform(1000.0, 10000.0), 2)
                accounts.append((name, password, balance))

            cursor.executemany(
                "INSERT INTO accounts (account_holder_name, password, balance) VALUES (?, ?, ?)",
                accounts
            )

            # Generate and populate the ATMs table with 100 random ATMs
            atms = []
            locations = ["Downtown", "Uptown", "Airport", "Mall", "University"]
            for _ in range(100):
                location = random.choice(locations) + str(random.randint(1, 100))  # Randomize location names
                cash_level = round(random.uniform(1000.0, 20000.0), 2)
                status = random.choice(["Active", "Inactive"])
                atms.append((location, cash_level, status))

            cursor.executemany(
                "INSERT INTO atms (location, cash_level, status) VALUES (?, ?, ?)",
                atms
            )

            # Generate and populate the transactions table with 100 random transactions
            transactions = []
            for _ in range(100):
                account_id = random.randint(1, 100)  # Randomly pick an account ID
                transaction_type = random.choice(["Deposit", "Withdrawal"])
                amount = round(random.uniform(50.0, 1000.0), 2)
                transactions.append((account_id, transaction_type, amount))

            cursor.executemany(
                "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (?, ?, ?)",
                transactions
            )

            connection.commit()
            connection.close()
            print("Database created and populated successfully!")

# Example usage
if __name__ == "__main__":
    db = Database("atm_simulator.db")
    db.create_and_populate_database()
