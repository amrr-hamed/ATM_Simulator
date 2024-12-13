import tkinter as tk
from tkinter import messagebox
import sqlite3
from threading import Thread
import threading
import random  # For generating random account IDs, transaction amounts, and types
import time  # For measuring performance time
from concurrent.futures import ThreadPoolExecutor  # For multi-threaded execution

from ATMGUI import ATMUI  # Ensure ATMUI is correctly implemented
from Accountmanager import AccountManager  # AccountManager handles authentication


def fetch_limited_active_atms(limit, db_name="atm_simulator.db"):
    """Fetch a limited number of active ATMs from the database."""
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Query to fetch active ATMs
    query = "SELECT atm_id, location FROM atms WHERE status = 'Active' LIMIT ?"
    cursor.execute(query, (limit,))
    atms = cursor.fetchall()

    connection.close()
    return atms


class ATMApp:
    def __init__(self):
        self.manager = AccountManager()
        self.main_window()

    def main_window(self):
        """Create the main window for ATM simulation."""
        self.root = tk.Tk()
        self.root.title("ATM Simulator")
        self.root.geometry("400x300")
        self.root.configure(bg="#2c3e50")

        header_label = tk.Label(
            self.root,
            text="ATM Simulator",
            font=("Helvetica", 18, "bold"),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        header_label.pack(pady=20)

        entry_frame = tk.Frame(self.root, bg="#34495e")
        entry_frame.pack(pady=10)

        entry_label = tk.Label(
            entry_frame,
            text="Enter the number of ATMs to simulate:",
            font=("Helvetica", 12),
            bg="#34495e",
            fg="#ecf0f1"
        )
        entry_label.pack(side=tk.LEFT, padx=5)

        self.atm_count_entry = tk.Entry(entry_frame, font=("Helvetica", 12), width=10)
        self.atm_count_entry.pack(side=tk.LEFT, padx=5)

        start_button = tk.Button(
            self.root,
            text="Start Simulation",
            font=("Helvetica", 12, "bold"),
            bg="#16a085",
            fg="white",
            activebackground="#1abc9c",
            activeforeground="white",
            command=self.start_simulation
        )
        start_button.pack(pady=20)

        self.root.mainloop()

    def start_simulation(self):
        """Start the ATM simulation using threads."""
        try:
            # Get the number of ATMs to simulate
            atm_count = int(self.atm_count_entry.get())
            if atm_count <= 0:
                raise ValueError("Number of ATMs must be greater than zero.")

            # Fetch the specified number of ATMs
            atms = fetch_limited_active_atms(atm_count)

            if not atms:
                messagebox.showinfo("No ATMs Found", "No active ATMs available in the database.")
                return
            elif len(atms) < atm_count:
                messagebox.showwarning(
                    "Not Enough ATMs",
                    f"Only {len(atms)} active ATMs are available. Launching {len(atms)} simulation(s)."
                )

            # Launch a thread for each ATM
            for atm_id, location in atms:
                thread = Thread(target=self.launch_atm, args=(atm_id, location))
                thread.start()

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def launch_atm(self, atm_id, location):
        """Thread-safe method to create an ATM window."""
        self.root.after(0, self.create_atm_window, atm_id, location)

    def create_atm_window(self, atm_id, location):
        """Create a new window for the ATM."""
        atm_window = tk.Toplevel(self.root)
        atm_window.title(f"ATM {atm_id}")
        atm_window.geometry("400x400")
        atm_window.configure(bg="#2c3e50")
        ATMUI(atm_window, self.manager, location, atm_id)
        
        
        
        
    def measure_transaction_performance(self):
    
        """Compare performance of single-threaded vs multi-threaded transactions"""
    
        def single_threaded_transactions():
            for _ in range(50):  # Simulate 50 transactions
                account_id = random.randint(1, 10)  # Assuming account IDs 1-10
                amount = random.uniform(10, 500)
                transaction_type = random.choice(['deposit', 'withdraw'])
                
                if transaction_type == 'deposit':
                    self.manager.deposit(account_id, amount)
                else:
                    try:
                        # Assuming ATM ID 1 for simplicity
                        self.manager.withdraw(account_id, amount, 1)
                    except ValueError as e:
                        print(f"Withdrawal error: {e}")

        def multi_threaded_transactions():
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for _ in range(50):
                    account_id = random.randint(1, 10)
                    amount = random.uniform(10, 500)
                    transaction_type = random.choice(['deposit', 'withdraw'])
                    
                    if transaction_type == 'deposit':
                        futures.append(executor.submit(self.manager.deposit, account_id, amount))
                    else:
                        futures.append(executor.submit(self.manager.withdraw, account_id, amount, 1))
                
                # Wait for all futures to complete
                for future in futures:
                    future.result()

        # Measure single-threaded performance
        start_time = time.time()
        single_threaded_transactions()
        single_threaded_time = time.time() - start_time

        # Measure multi-threaded performance
        start_time = time.time()
        multi_threaded_transactions()
        multi_threaded_time = time.time() - start_time

        print(f"Single-threaded Transaction Time: {single_threaded_time:.4f} seconds")
        print(f"Multi-threaded Transaction Time: {multi_threaded_time:.4f} seconds")
        print(f"Performance Improvement: {(single_threaded_time / multi_threaded_time - 1) * 100:.2f}%")
        
        
    def stress_test_transactions(self):
        """
        Simulate a high-concurrency scenario with multiple threads
        """
        def simulate_random_transaction():
            try:
                # Randomly choose transaction type
                transaction_type = random.choice(['deposit', 'withdraw'])
                account_id = random.randint(1, 10)  # Assuming account IDs 1-10
                amount = random.uniform(10, 500)
                
                if transaction_type == 'deposit':
                    self.manager.deposit(account_id, amount)
                    print(f"Thread {threading.current_thread().name}: Deposited ${amount} to Account {account_id}")
                else:
                    # Assuming ATM ID 1 for simplicity
                    self.manager.withdraw(account_id, amount, 1)
                    print(f"Thread {threading.current_thread().name}: Withdrew ${amount} from Account {account_id}")
            
            except ValueError as e:
                print(f"Transaction Error in {threading.current_thread().name}: {e}")

        # Create and start multiple threads
        threads = []
        num_threads = 20  # Simulate 20 concurrent transactions
        
        for _ in range(num_threads):
            thread = threading.Thread(target=simulate_random_transaction)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        print("Stress test completed.")       


if __name__ == "__main__":
    app = ATMApp()

    print("Testing Measure Transaction Performance:")
    app.measure_transaction_performance()
    print("\n")

    print("Testing Stress Test Transactions:")
    app.stress_test_transactions()

