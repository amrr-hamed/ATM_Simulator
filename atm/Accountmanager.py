import threading
import sqlite3

from transaction import Transaction
      
import sqlite3
import threading


class AccountManager:
    def __init__(self, db_name="atm_simulator.db"):
        self.db_name = db_name
        self.lock = threading.Lock()  # Ensures thread safety for database operations

    def execute_query(self, query, params=(), fetch_one=False, fetch_all=False):
        """Executes a query with thread-safe database access."""
        with self.lock:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()

            result = None
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()

            connection.close()
            return result

    def authenticate_user(self, account_id, password):
        """Validates user credentials."""
        query = "SELECT * FROM accounts WHERE account_id = ? AND password = ?"
        result = self.execute_query(query, (account_id, password), fetch_one=True)
        return result is not None

    def get_balance(self, account_id):
        """Retrieves the current balance of an account."""
        try:
            query = "SELECT balance FROM accounts WHERE account_id = ?"
            result = self.execute_query(query, (account_id,), fetch_one=True)
            
            if result is None:
                print(f"No account found with ID {account_id}")
                return None
            
            return result[0]
        except Exception as e:
            print(f"Error retrieving balance for account {account_id}: {e}")
            return None

    def deposit(self, account_id, amount):
        """Deposits an amount into an account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")

        # Update the balance
        update_query = "UPDATE accounts SET balance = balance + ? WHERE account_id = ?"
        self.execute_query(update_query, (amount, account_id))

        # Log the transaction
        log_query = "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (?, 'Deposit', ?)"
        self.execute_query(log_query, (account_id, amount))

    def withdraw(self, account_id, amount, atm_id):
        """Withdraws an amount from an account, considering ATM cash levels."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")

        # Check account balance
        current_balance = self.get_balance(account_id)
        if current_balance is None:
            raise ValueError("Account does not exist.")
        if current_balance < amount:
            raise ValueError("Insufficient balance in the account.")

        # Check ATM cash level
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        cursor.execute("SELECT cash_level FROM atms WHERE atm_id = ?", (atm_id,))
        result = cursor.fetchone()

        if not result:
            connection.close()
            raise ValueError("ATM not found.")

        atm_cash_level = result[0]

        if atm_cash_level < amount:
            connection.close()
            raise ValueError(
                f"ATM does not have enough cash. Available: {atm_cash_level}. Try a smaller amount."
            )

        # Update account balance
        update_balance_query = "UPDATE accounts SET balance = balance - ? WHERE account_id = ?"
        cursor.execute(update_balance_query, (amount, account_id))

        # Update ATM cash level
        update_atm_query = "UPDATE atms SET cash_level = cash_level - ? WHERE atm_id = ?"
        cursor.execute(update_atm_query, (amount, atm_id))

        # Log the transaction
        log_query = """
            INSERT INTO transactions (account_id, transaction_type, amount) 
            VALUES (?, 'Withdrawal', ?)
        """
        cursor.execute(log_query, (account_id, amount))

        connection.commit()
        connection.close()


    def log_transaction(self, account_id, transaction_type, amount):
        """Logs a transaction."""
        query = "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (?, ?, ?)"
        self.execute_query(query, (account_id, transaction_type, amount))

    def get_transaction_history(self, account_id):
        """Retrieves the transaction history for an account and formats it."""
        query = "SELECT * FROM transactions WHERE account_id = ? ORDER BY timestamp DESC LIMIT 3"
        transactions = self.execute_query(query, (account_id,), fetch_all=True)
        
        # Format each transaction tuple into a user-friendly string
        formatted_transactions = [
            f"Type: {transaction[2]}\n, Amount: ${float(transaction[3]):.2f}\n, Time: {transaction[4]}\n --------\n"
            for transaction in transactions
        ]
        return formatted_transactions
    
    def get_account_name(self, account_id):
        """Retrieves the transaction history for an account."""
        query = "SELECT account_holder_name FROM accounts WHERE account_id = ? "
        result=self.execute_query(query, (account_id,), fetch_one=True)
        return result[0]
    


# if __name__ == "__main__":
#     manager = AccountManager()

#     # Create test accounts
#     manager.execute_query(
#         "INSERT INTO accounts (account_holder_name, password, balance) VALUES (?, ?, ?)",
#         ("John Doe", "1234", 5000.0),
#     )
#     manager.execute_query(
#         "INSERT INTO accounts (account_holder_name, password, balance) VALUES (?, ?, ?)",
#         ("Jane Smith", "5678", 3000.0),
#     )

#     # Authenticate user
#     print("Authentication:", manager.authenticate_user(1, "1234"))

#     # Deposit money
#     manager.deposit(1, 1000)
#     print("Balance after deposit:", manager.get_balance(1))

#     # Withdraw money
#     manager.withdraw(1, 500)
#     print("Balance after withdrawal:", manager.get_balance(1))

#     # Get transaction history
#     print("Transaction History:")
#     for transaction in manager.get_transaction_history(1):
#         print(transaction)