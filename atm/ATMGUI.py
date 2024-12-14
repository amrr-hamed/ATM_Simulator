import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import os

class ATMUI:
    def __init__(self, root, account_manager, location, atm_id):
        self.root = root
        self.account_manager = account_manager
        self.location = location
        self.atm_id = atm_id
        
        # Window Setup
        self.root.title("ATM Interface")
        self.root.geometry("500x600")  # Increased height for message area
        self.root.configure(bg='#2c3e50')

        # Create main container
        self.main_container = tk.Frame(root, bg='#2c3e50')
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Background image setup
        # self.setup_background()

        # Message label for displaying transaction messages
        self.message_label = None

        # Initial login screen
        self.create_login_screen()

    # def setup_background(self):
    #     """Set up a background image with overlay."""
    #     self.canvas = tk.Canvas(self.main_container, highlightthickness=0)
    #     self.canvas.pack(fill=tk.BOTH, expand=True)

    #     try:
    #         bg_image = Image.open("E:\\ATM\\black.jpg")
    #         self.bg_photo = ImageTk.PhotoImage(bg_image)
    #         self.canvas.create_image(0, 0, image=self.bg_photo, anchor=tk.NW)
    #         self.canvas.create_rectangle(0, 0, 1000, 700, fill='black', stipple='gray50')
    #     except Exception as e:
    #         print(f"Background image error: {e}")
    def authenticate(self):
        """Authenticate user and move to main menu."""
        try:
            card_number = int(self.card_entry.get())
            password = self.pass_entry.get()

            if self.account_manager.authenticate_user(card_number, password):
                account_name = self.account_manager.get_account_name(card_number)
                self.create_main_menu(account_name, card_number)
            else:
                messagebox.showerror("Login Failed", "Invalid Card Number or PIN")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid card number and PIN")        

    def show_message(self, message, parent, color='black'):
        """Display a message dynamically under the relevant section."""
        # Destroy any previous message labels in the parent
        for widget in parent.winfo_children():
            if isinstance(widget, tk.Label) and getattr(widget, "is_message_label", False):
                widget.destroy()

        # Create and display a new message label
        message_label = tk.Label(
            parent,
            text=message,
            font=('Arial', 12),
            bg='white',
            fg=color,
            wraplength=600,
            pady=10
        )
        message_label.is_message_label = True  # Mark this as a message label
        message_label.pack(pady=(10, 0))  # Place it dynamically within the parent



    def create_login_screen(self):
        """Create a modern login screen."""
        for widget in self.main_container.winfo_children():
            widget.destroy()

        login_frame = tk.Frame(self.main_container, 
                             bg='white', 
                             highlightbackground='#e0e0e0', 
                             highlightthickness=1)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=500)

        # Rest of the login screen code remains the same
        title_label = tk.Label(login_frame, text=f"ALAhly Bank \n Branch:{self.location}", 
                             font=('Arial', 24, 'bold'), 
                             bg='white', fg='#2c3e50')
        title_label.pack(pady=(50, 30))

        card_label = tk.Label(login_frame, text="Card Number", 
                            font=('Arial', 12), 
                            bg='white', fg='#34495e')
        card_label.pack(pady=(10, 5))
        self.card_entry = tk.Entry(login_frame, font=('Arial', 14), 
                                 justify='center', bd=1, relief=tk.SOLID)
        self.card_entry.pack(pady=(0, 20), padx=50, fill=tk.X)

        pass_label = tk.Label(login_frame, text="PIN", 
                            font=('Arial', 12), 
                            bg='white', fg='#34495e')
        pass_label.pack(pady=(10, 5))
        self.pass_entry = tk.Entry(login_frame, show='*', 
                                 font=('Arial', 14), 
                                 justify='center', bd=1, relief=tk.SOLID)
        self.pass_entry.pack(pady=(0, 30), padx=50, fill=tk.X)

        login_button = tk.Button(login_frame, text="Login", 
                               font=('Arial', 14, 'bold'), 
                               bg='#3498db', fg='white', 
                               activebackground='#2980b9',
                               relief=tk.FLAT,
                               command=self.authenticate)
        login_button.pack(pady=(10, 20), padx=50, fill=tk.X)

    def create_main_menu(self, account_name, card_number):
        """Create the main menu with modern, colorful buttons."""
        self.account_name = account_name  # Store account name for cancel button
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Rest of the main menu code remains the same with existing buttons
        menu_frame = tk.Frame(self.main_container, bg='white')
        menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=700, height=500)

        welcome_label = tk.Label(menu_frame, 
                               text=f"Welcome, {account_name}", 
                               font=('Arial', 24, 'bold'), 
                               bg='white', fg='#2c3e50')
        welcome_label.pack(pady=(30, 30))

        button_frame = tk.Frame(menu_frame, bg='white')
        button_frame.pack(expand=True)

        button_style = {
            'font': ('Arial', 16, 'bold'),
            'bd': 0,
            'relief': tk.FLAT,
            'width': 20,
            'pady': 15
        }

        withdraw_btn = tk.Button(button_frame, 
                               text="Withdraw", 
                               bg='#2c3e50', fg='white',
                               command=lambda: self.show_transaction_screen('withdraw', card_number),
                               **button_style)
        withdraw_btn.pack(pady=10)

        deposit_btn = tk.Button(button_frame, 
                              text="Deposit", 
                              bg='#2c3e50', fg='white',
                              command=lambda: self.show_transaction_screen('deposit', card_number),
                              **button_style)
        deposit_btn.pack(pady=10)

        balance_btn = tk.Button(button_frame, 
                              text="Check Balance", 
                              bg='#2c3e50', fg='white',
                              command=lambda: self.show_check_balance_screen(card_number),
                              **button_style)
        balance_btn.pack(pady=10)

        transactions_btn = tk.Button(button_frame, 
                                   text="Recent Transactions", 
                                   bg='#2c3e50', fg='white',
                                   command=lambda: self.show_transaction_log_screen(card_number),
                                   **button_style)
        transactions_btn.pack(pady=10)
        
    def show_message(self, message, parent, color='black'):
        """Display a message dynamically under the relevant section."""
        # Destroy any previous message labels in the parent
        for widget in parent.winfo_children():
            if isinstance(widget, tk.Label) and getattr(widget, "is_message_label", False):
                widget.destroy()

        # Create and display a new message label
        message_label = tk.Label(
            parent,
            text=message,
            font=('Arial', 12),
            bg='white',
            fg=color,
            wraplength=600,
            pady=10
        )
        message_label.is_message_label = True  # Mark this as a message label
        message_label.pack(pady=(10, 0))  # Place it dynamically within the parent
        
    def show_transaction_screen(self, transaction_type, card_number):
        """Show transaction screen with amount input."""
        for widget in self.main_container.winfo_children():
            widget.destroy()

        trans_frame = tk.Frame(self.main_container, bg='white')
        trans_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER, width=700, height=500)

        title_label = tk.Label(trans_frame, 
                            text=f"{transaction_type.capitalize()} Money", 
                            font=('Arial', 24, 'bold'), 
                            bg='white', fg='#2c3e50')
        title_label.pack(pady=(30, 20))

        amount_label = tk.Label(trans_frame, 
                                text="Enter Amount", 
                                font=('Arial', 16), 
                                bg='white', fg='#34495e')
        amount_label.pack(pady=(10, 5))

        amount_entry = tk.Entry(trans_frame, 
                                font=('Arial', 20), 
                                justify='center', 
                                bd=1, relief=tk.SOLID)
        amount_entry.pack(pady=(0, 20), padx=100, fill=tk.X)

        btn_frame = tk.Frame(trans_frame, bg='white')
        btn_frame.pack(pady=20)

        confirm_btn = tk.Button(btn_frame, 
                                text="Confirm", 
                                font=('Arial', 16, 'bold'),
                                bg='#2ecc71', fg='white',
                                width=15,
                                command=lambda: self.process_transaction(transaction_type, 
                                                                        card_number, 
                                                                        amount_entry.get(),
                                                                        trans_frame))
        confirm_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(btn_frame, 
                            text="Cancel", 
                            font=('Arial', 16, 'bold'),
                            bg='#e74c3c', fg='white',
                            width=15,
                            command=lambda: self.create_main_menu(self.account_name, card_number))
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    

    def process_transaction(self, transaction_type, card_number, amount, parent):
        """Process withdrawal or deposit."""
        try:
            amount = float(amount)
            if transaction_type == 'withdraw':
                self.account_manager.withdraw(card_number, amount, self.atm_id)
                self.show_message(f"Withdrawal of ${amount:.2f} successful!", parent, 'green')
            else:  # deposit
                self.account_manager.deposit(card_number, amount,self.atm_id)
                self.show_message(f"Deposit of ${amount:.2f} successful!", parent, 'green')

            # Optionally return to the main menu after a delay
            self.root.after(2000, lambda: self.create_main_menu(
                self.account_manager.get_account_name(card_number), card_number))
        except Exception as e:
            self.show_message(str(e), parent, 'red')




    def show_check_balance_screen(self, card_number):
        """Show the screen to check the balance."""
        for widget in self.main_container.winfo_children():
            widget.destroy()

        balance_frame = tk.Frame(self.main_container, bg='white')
        balance_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER, width=700, height=500)

        title_label = tk.Label(balance_frame, 
                            text="Account Balance", 
                            font=('Arial', 24, 'bold'), 
                            bg='white', fg='#2c3e50')
        title_label.pack(pady=(30, 20))

        try:
            # Fetch and display the account balance
            balance = self.account_manager.get_balance(card_number)
            self.show_message(f"Your balance is: ${balance:.2f}", balance_frame, 'green')
        except Exception as e:
            self.show_message(str(e), balance_frame, 'red')

        # Add a back button to return to the main menu
        back_button = tk.Button(balance_frame, 
                                text="Back", 
                                font=('Arial', 16, 'bold'),
                                bg='#3498db', fg='white',
                                command=lambda: self.create_main_menu(self.account_name, card_number))
        back_button.pack(pady=20)




    def show_transaction_log_screen(self, card_number):
        """Show the screen to view the transaction log."""
        for widget in self.main_container.winfo_children():
            widget.destroy()

        log_frame = tk.Frame(self.main_container, bg='white')
        log_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER, width=700, height=500)

        title_label = tk.Label(log_frame, 
                            text="Transaction Log", 
                            font=('Arial', 24, 'bold'), 
                            bg='white', fg='#2c3e50')
        title_label.pack(pady=(30, 20))

        log_text = tk.Text(log_frame, 
                        font=('Arial', 12), 
                        bg='#ecf0f1', fg='#2c3e50', 
                        wrap=tk.WORD, height=15, width=80, 
                        state=tk.DISABLED)
        log_text.pack(pady=(10, 20), padx=20)

        try:
            # Fetch the transaction log
            transactions = self.account_manager.get_transaction_history(card_number)
            if transactions:
                log_text.config(state=tk.NORMAL)
                log_text.insert(tk.END, "\n".join(transactions))
                log_text.config(state=tk.DISABLED)
            else:
                self.show_message("No transactions found.", log_frame, 'orange')
        except Exception as e:
            self.show_message(str(e), log_frame, 'red')

        # Add a back button to return to the main menu
        back_button = tk.Button(log_frame, 
                                text="Back", 
                                font=('Arial', 16, 'bold'),
                                bg='#3498db', fg='white',
                                command=lambda: self.create_main_menu(self.account_name, card_number))
        back_button.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    dummy_account_manager = None
    app = ATMUI(root, dummy_account_manager, "ALF MASKAN", 2)