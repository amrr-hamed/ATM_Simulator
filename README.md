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
