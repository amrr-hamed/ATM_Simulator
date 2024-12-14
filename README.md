# ATM Simulator Project

## Overview
This ATM Simulator is a comprehensive Python application that simulates a multi-threaded ATM banking system using Tkinter for the graphical interface and SQLite for data management.

## Features
- Multi-threaded ATM simulation
- Secure user authentication
- Real-time balance management
- Transaction logging
- Concurrent ATM operations

## Prerequisites
- Python 3.8+
- Tkinter
- SQLite3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ATM-Simulator.git
cd ATM-Simulator
```

2. Install dependencies:
```bash
pip install sqlite3
```

## Configuration

### Database Setup
Before running the application, initialize the database:
```python
from Database import Database

db = Database("atm_simulator.db")
db.create_and_populate_database()
```

## Running the Application
```bash
python main.py
```
## Key Components

### Authentication
- Secure PIN-based login
- Thread-safe credential verification

### Transaction Types
- Withdrawal
- Deposit
- Balance Inquiry
- Transaction History

### Multi-Threading
- Concurrent ATM simulations
- Thread-safe database access
- Distributed transaction processing

## Security Features
- Locked database transactions
- Restricted account access
- Secure password management

## Performance Considerations
- Uses threading for parallel processing
- Implements database locks to prevent race conditions
- Efficient transaction logging

## Limitations
- Simulated environment
- Fixed number of pre-generated accounts
- No network or real-world banking integration

## Potential Improvements
- Implement more robust error handling
- Add advanced security features
- Create more complex transaction scenarios
- Develop a more sophisticated UI

## Troubleshooting
- Ensure SQLite3 is properly installed
- Check Python version compatibility
- Verify database initialization

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
