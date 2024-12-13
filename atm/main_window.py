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
        
        
if __name__ == "__main__":
    app = ATMApp()    
        
  



