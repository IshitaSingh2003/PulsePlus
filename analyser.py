import pandas as pd

# Load the latency data from the Excel sheet into a DataFrame.
latency_data = pd.read_excel("latency_data.xlsx")

# Print the first few rows of the DataFrame to inspect the data.
print("Sample latency data:")
print(latency_data.head())

# Calculate and print basic statistics for each target address.
for target_address in latency_data.columns[1:]:
    print(f"\nStatistics for {target_address}:")
    print("Average Latency:", latency_data[target_address].mean())
    print("Maximum Latency:", latency_data[target_address].max())
    print("Minimum Latency:", latency_data[target_address].min())
    print("Standard Deviation:", latency_data[target_address].std())


# Calculate the average latency for each target address.
average_latency = latency_data.mean()

# Calculate the standard deviation of latency for each target address.
std_deviation = latency_data.std()

# Assuming the initial average latency and standard deviation are known (before your tool's implementation):
initial_average_latency = 0.1  # Initial average latency in seconds
initial_std_deviation = 0.02  # Initial standard deviation in seconds

# Calculate the reduction in waiting time for users and the performance improvement.
waiting_time_reduction = (initial_average_latency - average_latency)[0] * len(latency_data) / 3600  # Hours
performance_improvement = (initial_std_deviation - std_deviation)[0] / initial_std_deviation * 100  # Percentage

# Print the estimated improvements.
print(f"Estimated Waiting Time Reduction: {float(waiting_time_reduction):.2f} hours")
print(f"Estimated Performance Improvement: {performance_improvement:.2f}%")