from datetime import datetime
class Transaction:
    def __init__(self, transaction_id,account_id, transaction_type, amount):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.transaction_type = transaction_type  # Correct the attribute name here
        self.amount = amount
        self.timestamp = datetime.now()

    def __str__(self):
        return f"Transaction(ID: {self.transaction_id}, Account ID: {self.account_id}, Type: {self.transaction_type}, Amount: {self.amount}, Timestamp: {self.timestamp})"
