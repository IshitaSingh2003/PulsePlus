import pandas as pd
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('latency.db')
c = conn.cursor()

# Load the latency data from the SQL table into a DataFrame.
c.execute("SELECT * FROM latency")
latency_data = pd.DataFrame(c.fetchall(), columns=['timestamp', 'target', 'latency'])
# Print the first few rows of the DataFrame to inspect the data.
print("Sample latency data:")
print(latency_data.head())

# Calculate and print basic statistics for each target address.
for target_address in latency_data['target'].unique():
    target_data = latency_data[latency_data['target'] == target_address]
    print(f"\nStatistics for {target_address}:")
    print("Average Latency:", target_data['latency'].mean())
    print("Maximum Latency:", target_data['latency'].max())
    print("Minimum Latency:", target_data['latency'].min())
    print("Standard Deviation:", target_data['latency'].std())

# Calculate the average latency for each target address over time.
average_latency = latency_data.groupby('target')['latency'].mean()

# Calculate the standard deviation of latency for each target address over time.
std_deviation = latency_data.groupby('target')['latency'].std()

# Assuming the initial average latency and standard deviation are known (before your tool's implementation):
initial_average_latency = 0.1  # Initial average latency in seconds
initial_std_deviation = 0.02  # Initial standard deviation in seconds

# Calculate the reduction in waiting time for users and the performance improvement.
waiting_time_reduction = (initial_average_latency - average_latency).sum() * len(latency_data) / 3600  # Hours
performance_improvement = (initial_std_deviation - std_deviation).sum() / initial_std_deviation * 100  # Percentage

# Print the estimated improvements.
print(f"Estimated Waiting Time Reduction: {waiting_time_reduction:.2f} hours")
print(f"Estimated Performance Improvement: {performance_improvement:.2f}%")

# Close the database connection
conn.close()
