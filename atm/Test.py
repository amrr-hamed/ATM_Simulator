import time
import random
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
from statistics import mean
from datetime import datetime

class ATMPerformanceTester:
    def __init__(self, db_name="atm_simulator.db"):
        self.db_name = db_name
        # Get active ATM IDs from database
        self.active_atm_ids = self._get_active_atm_ids()
        self.account_ids = self._get_all_account_ids()
        
    def _get_active_atm_ids(self):
        """Fetch active ATM IDs from database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT atm_id FROM atms WHERE status = 'Active'")
        atm_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        return atm_ids
    
    def _get_all_account_ids(self):
        """Fetch all account IDs from database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT account_id FROM accounts")
        account_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        return account_ids

    def _generate_transaction(self):
        """Generate a random realistic transaction"""
        account_id = random.choice(self.account_ids)
        atm_id = random.choice(self.active_atm_ids)
        amount = round(random.uniform(10, 500), 2)
        transaction_type = random.choice(['deposit', 'withdraw'])
        return (account_id, atm_id, transaction_type, amount)

    def _process_transaction(self, transaction_data):
        """Process a single transaction"""
        account_id, atm_id, transaction_type, amount = transaction_data
        start_time = time.time()
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Get current balance
            cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (account_id,))
            current_balance = cursor.fetchone()[0]
            
            # Process transaction
            if transaction_type == 'withdraw' and current_balance < amount:
                raise ValueError("Insufficient funds")
            
            new_balance = current_balance + amount if transaction_type == 'deposit' else current_balance - amount
            
            # Update balance
            cursor.execute("""
                UPDATE accounts 
                SET balance = ? 
                WHERE account_id = ?
            """, (new_balance, account_id))
            
            # Log transaction
            cursor.execute("""
                INSERT INTO transactions (account_id, atm_id, transaction_type, amount)
                VALUES (?, ?, ?, ?)
            """, (account_id, atm_id, transaction_type, amount))
            
            conn.commit()
            success = True
        except Exception as e:
            success = False
        finally:
            conn.close()
            
        return {
            'execution_time': time.time() - start_time,
            'success': success,
            'type': transaction_type
        }

    def run_performance_test(self, num_transactions=100, num_threads=4):
        """Run performance comparison between sequential and parallel processing"""
        print(f"\nStarting performance test with {num_transactions} transactions...")
        
        # Generate test transactions
        transactions = [self._generate_transaction() for _ in range(num_transactions)]
        
        # Sequential Test
        print("\nRunning Sequential Test...")
        sequential_start = time.time()
        sequential_results = []
        
        for transaction in transactions:
            result = self._process_transaction(transaction)
            sequential_results.append(result)
        
        sequential_total = time.time() - sequential_start
        
        # Parallel Test
        print("Running Parallel Test...")
        parallel_start = time.time()
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            parallel_results = list(executor.map(self._process_transaction, transactions))
            
        parallel_total = time.time() - parallel_start
        
        # Calculate metrics
        self._analyze_results(sequential_results, parallel_results, 
                            sequential_total, parallel_total,
                            num_transactions, num_threads)

    def _analyze_results(self, sequential_results, parallel_results, 
                        sequential_total, parallel_total,
                        num_transactions, num_threads):
        """Analyze and display test results"""
        
        def calculate_metrics(results, total_time):
            successful = [r for r in results if r['success']]
            times = [r['execution_time'] for r in results]
            return {
                'total_time': total_time,
                'success_rate': len(successful) / len(results) * 100,
                'avg_time': mean(times) if times else 0,
                'max_time': max(times) if times else 0,
                'min_time': min(times) if times else 0
            }

        seq_metrics = calculate_metrics(sequential_results, sequential_total)
        par_metrics = calculate_metrics(parallel_results, parallel_total)

        # Print results
        print("\n=== Performance Test Results ===")
        print(f"\nConfiguration:")
        print(f"Number of Transactions: {num_transactions}")
        print(f"Number of Threads: {num_threads}")
        print(f"Active ATMs: {len(self.active_atm_ids)}")
        
        print("\nSequential Execution:")
        print(f"Total Time: {seq_metrics['total_time']:.3f} seconds")
        print(f"Success Rate: {seq_metrics['success_rate']:.1f}%")
        print(f"Average Transaction Time: {seq_metrics['avg_time']*1000:.2f} ms")
        print(f"Max Transaction Time: {seq_metrics['max_time']*1000:.2f} ms")
        print(f"Min Transaction Time: {seq_metrics['min_time']*1000:.2f} ms")
        
        print("\nParallel Execution:")
        print(f"Total Time: {par_metrics['total_time']:.3f} seconds")
        print(f"Success Rate: {par_metrics['success_rate']:.1f}%")
        print(f"Average Transaction Time: {par_metrics['avg_time']*1000:.2f} ms")
        print(f"Max Transaction Time: {par_metrics['max_time']*1000:.2f} ms")
        print(f"Min Transaction Time: {par_metrics['min_time']*1000:.2f} ms")
        
        speedup = seq_metrics['total_time'] / par_metrics['total_time']
        print(f"\nSpeedup Factor: {speedup:.2f}x")
        
        # Create visualization
        self._plot_results(seq_metrics, par_metrics)

    def _plot_results(self, seq_metrics, par_metrics):
        """Create performance visualization"""
        plt.figure(figsize=(12, 6))
        
        # Plot total times
        times = [seq_metrics['total_time'], par_metrics['total_time']]
        plt.bar(['Sequential', 'Parallel'], times)
        
        plt.title('ATM Transaction Processing Performance')
        plt.ylabel('Total Execution Time (seconds)')
        plt.grid(True, axis='y')
        
        # Add value labels on bars
        for i, v in enumerate(times):
            plt.text(i, v, f'{v:.3f}s', ha='center', va='bottom')
        
        plt.show()

if __name__ == "__main__":
    # Create and run performance test
    tester = ATMPerformanceTester()
    
    # Run test with different configurations
    print("Test 1: 1000 transactions with 50 threads")
    tester.run_performance_test(num_transactions=10000, num_threads=5000)
    
    print("\nTest 2: 200 transactions with 8 threads")
    #tester.run_performance_test(num_transactions=200, num_threads=8)