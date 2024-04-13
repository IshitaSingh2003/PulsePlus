import tkinter as tk
import socket
import time
import statistics
import pandas as pd
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('latency.db')
c = conn.cursor()

# Create the latency table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS latency (timestamp TEXT, target TEXT, latency REAL)''')

# Define the target IP addresses or domain names to monitor.
target_addresses = ["google.com", "facebook.com", 
                    "whatsapp.com", "github.com",  "chat.openai.com",
                    "huggingface.co", "youtube.com", "vitbhopal.ac.in"]

# Define the port you want to monitor (e.g., HTTP on port 80).
port = 80

# Define the average latency threshold in seconds.
average_threshold = 0.5  # Adjust this value as needed.

# Create an empty DataFrame to store the latency data.
columns = ["Timestamp"] + target_addresses
latency_data = pd.DataFrame(columns=columns)

# Initialize a dictionary to store previous latency measurements.
previous_latency = {target: None for target in target_addresses}

def measure_latency(target_ip, port):
    start_time = time.time()
    try:
        # Create a socket connection to the target IP and port.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_ip, port))
    except (socket.timeout, ConnectionRefusedError, OSError):
        # Handle connection errors.
        return None
    end_time = time.time()
    return end_time - start_time

def show_popup_alert(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    popup = tk.Toplevel(root)
    popup.title("Network Latency Alert")
    popup.geometry("500x300")

    label = tk.Label(popup, text=message)
    label.pack(padx=20, pady=20)

    popup.mainloop()

# Main monitoring loop
while True:
    latency_values = {}  # Store latency values for all target addresses.

    for target_address in target_addresses:
        target_ip = socket.gethostbyname(target_address)
        latency = measure_latency(target_ip, port)
        
        if latency is not None:
            print(f"Latency to {target_address} ({target_ip}) is {latency} seconds")
            latency_values[target_address] = latency
        else:
            print(f"Unable to connect to {target_address} ({target_ip})")

    if latency_values:
        average_latency = statistics.mean(latency_values.values())
        print(f"Average latency: {average_latency} seconds")

        for target, current_latency in latency_values.items():
            previous_latency_value = previous_latency[target]
            if previous_latency_value is not None and current_latency < previous_latency_value:
                alert_message = f"Latency to {target} is decreasing. Switch network connection!"
                show_popup_alert(alert_message)

        # Record the timestamp and latency data in the DataFrame and the SQL table.
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        row_data = [timestamp] + list(latency_values.values())
        latency_data.loc[len(latency_data)] = row_data

        # Insert the data into the SQL table
        for target, latency in latency_values.items():
            c.execute("INSERT INTO latency (timestamp, target, latency) VALUES (?, ?, ?)", (timestamp, target, latency))

        conn.commit()

        previous_latency = latency_values

    # Adjust the sleep interval based on your monitoring frequency (e.g., every 5 minutes).
    time.sleep(30)  # Sleep for 5 minutes before the next round of monitoring.
