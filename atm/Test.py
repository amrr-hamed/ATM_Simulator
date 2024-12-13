import time
import random
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
from statistics import mean

def simulate_transaction_time():
    """Simulate a transaction without database interaction"""
    # Simulate some processing time
    time.sleep(random.uniform(0.1, 0.3))
    return True

def test_atm_performance(num_transactions=100, num_threads=4):
    """
    Test ATM performance comparing sequential vs parallel execution
    without actual database operations
    """
    print(f"\nTesting with {num_transactions} transactions...")
    
    # Sequential Test
    print("\nRunning Sequential Test...")
    sequential_times = []
    sequential_start = time.time()
    
    for _ in range(num_transactions):
        trans_start = time.time()
        simulate_transaction_time()
        sequential_times.append(time.time() - trans_start)
    
    sequential_total = time.time() - sequential_start
    
    # Parallel Test
    print("Running Parallel Test...")
    parallel_times = []
    parallel_start = time.time()
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit all tasks at once
        futures = [executor.submit(simulate_transaction_time) 
                  for _ in range(num_transactions)]
        
        # Wait for completion and record times
        for future in futures:
            start_time = time.time()
            future.result()
            parallel_times.append(time.time() - start_time)
    
    parallel_total = time.time() - parallel_start
    
    # Calculate and display results
    results = {
        'Sequential': {
            'total_time': sequential_total,
            'avg_time': mean(sequential_times),
            'max_time': max(sequential_times),
            'min_time': min(sequential_times)
        },
        'Parallel': {
            'total_time': parallel_total,
            'avg_time': mean(parallel_times),
            'max_time': max(parallel_times),
            'min_time': min(parallel_times)
        }
    }
    
    # Print results
    print("\n=== Performance Results ===")
    print(f"\nNumber of Transactions: {num_transactions}")
    print(f"Number of Threads: {num_threads}")
    
    print("\nSequential Execution:")
    print(f"Total Time: {results['Sequential']['total_time']:.3f} seconds")
    print(f"Average Transaction Time: {results['Sequential']['avg_time']*1000:.2f} ms")
    print(f"Max Transaction Time: {results['Sequential']['max_time']*1000:.2f} ms")
    print(f"Min Transaction Time: {results['Sequential']['min_time']*1000:.2f} ms")
    
    print("\nParallel Execution:")
    print(f"Total Time: {results['Parallel']['total_time']:.3f} seconds")
    print(f"Average Transaction Time: {results['Parallel']['avg_time']*1000:.2f} ms")
    print(f"Max Transaction Time: {results['Parallel']['max_time']*1000:.2f} ms")
    print(f"Min Transaction Time: {results['Parallel']['min_time']*1000:.2f} ms")
    
    speedup = results['Sequential']['total_time'] / results['Parallel']['total_time']
    print(f"\nSpeedup Factor: {speedup:.2f}x")
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    plt.bar(['Sequential', 'Parallel'], 
            [results['Sequential']['total_time'], results['Parallel']['total_time']])
    plt.title('Transaction Processing Time Comparison')
    plt.ylabel('Total Time (seconds)')
    plt.grid(True, axis='y')
    
    # Add time labels on top of bars
    for i, v in enumerate([results['Sequential']['total_time'], 
                          results['Parallel']['total_time']]):
        plt.text(i, v, f'{v:.3f}s', ha='center', va='bottom')
    
    plt.show()
    
    return results

if __name__ == "__main__":
    # Test with different scenarios
    print("Testing with 300 transactions and 30 threads")
    results1 = test_atm_performance(num_transactions=200, num_threads=5)
    
    print("\nTesting with 500 transactions and 50 threads")
    #results2 = test_atm_performance(num_transactions=500, num_threads=50)