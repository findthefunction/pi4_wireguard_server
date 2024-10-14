import tkinter as tk
import subprocess
import os
import threading
import time

# Function to get WireGuard status
def get_wireguard_status():
    try:
        status = subprocess.getoutput("wg show")
    except Exception as e:
        status = f"Error retrieving status: {e}"
    return status

# Function to get network traffic stats
def get_traffic_stats():
    try:
        stats = subprocess.getoutput("wg show wg0 transfer")
    except Exception as e:
        stats = f"Error retrieving traffic stats: {e}"
    return stats

# Function to check connection status via ping
def check_connection():
    response = os.system("ping -c 1 10.0.0.1")
    if response == 0:
        result_label.config(text="Connected to Server", fg="green")
        status_label.config(text=get_wireguard_status(), fg="blue")
        traffic_label.config(text=get_traffic_stats(), fg="purple")
    else:
        result_label.config(text="Disconnected", fg="red")
        status_label.config(text="No connection", fg="red")
        traffic_label.config(text="", fg="red")

# Function to restart WireGuard service
def restart_wireguard():
    try:
        os.system("sudo wg-quick down wg0 && sudo wg-quick up wg0")
        result_label.config(text="WireGuard Restarted", fg="blue")
    except Exception as e:
        result_label.config(text=f"Failed to restart: {e}", fg="red")

# Function to get WireGuard logs
def get_wireguard_logs():
    try:
        logs = subprocess.getoutput("journalctl -u wg-quick@wg0 --since today")
    except Exception as e:
        logs = f"Error retrieving logs: {e}"
    return logs

# Function to display logs in a new window
def show_logs():
    logs = get_wireguard_logs()
    log_window = tk.Toplevel(root)
    log_window.title("WireGuard Logs")
    log_text = tk.Text(log_window)
    log_text.insert(tk.END, logs)
    log_text.pack()

# Function to continuously ping the server for latency checks
def continuous_ping():
    while True:
        response = os.system("ping -c 1 10.0.0.1")
        if response == 0:
            ping_label.config(text="Ping: OK", fg="green")
        else:
            ping_label.config(text="Ping: Failed", fg="red")
        time.sleep(5)

# Function to monitor connection status and trigger alerts
def monitor_connection():
    last_status = True
    while True:
        response = os.system("ping -c 1 10.0.0.1")
        if response != 0 and last_status:
            print("Alert: Connection lost!")
            last_status = False
        elif response == 0 and not last_status:
            print("Alert: Connection restored!")
            last_status = True
        time.sleep(5)

# Create GUI window
root = tk.Tk()
root.title("WireGuard Client Monitor")

# Check connection button
connection_btn = tk.Button(root, text="Check Connection", command=check_connection)
connection_btn.pack(pady=10)

# Restart WireGuard button
restart_btn = tk.Button(root, text="Restart WireGuard", command=restart_wireguard)
restart_btn.pack(pady=10)

# Show logs button
log_btn = tk.Button(root, text="Show Logs", command=show_logs)
log_btn.pack(pady=10)

# Labels for connection status, traffic stats, and ping results
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

status_label = tk.Label(root, text="", justify="left")
status_label.pack(pady=10)

traffic_label = tk.Label(root, text="", justify="left")
traffic_label.pack(pady=10)

ping_label = tk.Label(root, text="")
ping_label.pack(pady=10)

# Start continuous ping in a separate thread
ping_thread = threading.Thread(target=continuous_ping)
ping_thread.start()

# Start connection monitoring in a separate thread
monitor_thread = threading.Thread(target=monitor_connection)
monitor_thread.start()

# Run the GUI loop
root.mainloop()
