import tkinter as tk
import subprocess
import os
import threading
import time
import smtplib
import requests
import matplotlib.pyplot as plt
from collections import deque
from email.mime.text import MIMEText

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"
RECEIVER_EMAIL = "receiver-email@gmail.com"

# History to track latency and traffic stats over time
ping_history = deque(maxlen=100)
traffic_history = deque(maxlen=100)

# Function to send email alerts
def send_email_alert(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print(f"Email alert sent: {subject}")
    except Exception as e:
        print(f"Error sending email: {e}")

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
        sent, received = map(int, stats.split())
        traffic_history.append((sent + received) / 1024)  # Convert to KB
    except Exception as e:
        print(f"Error parsing traffic stats: {e}")

# Function to check connection status via ping
def check_connection():
    response = os.system("ping -c 1 10.0.0.1")
    if response == 0:
        result_label.config(text="Connected to Server", fg="green")
        status_label.config(text=get_wireguard_status(), fg="blue")
        get_traffic_stats()
    else:
        result_label.config(text="Disconnected", fg="red")
        status_label.config(text="No connection", fg="red")

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
        start_time = time.time()
        response = os.system("ping -c 1 10.0.0.1")
        end_time = time.time()

        if response == 0:
            latency = (end_time - start_time) * 1000  # Convert to ms
            ping_history.append(latency)
            ping_label.config(text=f"Ping: {latency:.2f} ms", fg="green")
        else:
            ping_label.config(text="Ping: Failed", fg="red")

        time.sleep(5)
        plot_graphs()

# Function to get public IP and verify routing through VPN
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            return "Failed to get public IP"
    except Exception as e:
        return f"Error: {e}"

# Function to monitor DNS queries
def monitor_dns():
    dns_query = subprocess.getoutput("cat /var/log/syslog | grep 'named'")
    dns_window = tk.Toplevel(root)
    dns_window.title("DNS Query Monitor")
    dns_text = tk.Text(dns_window)
    dns_text.insert(tk.END, dns_query)
    dns_text.pack()

# Function to monitor connection status and trigger alerts
def monitor_connection():
    last_status = True
    vpn_ip_range = "your-VPN-IP-range"

    while True:
        response = os.system("ping -c 1 10.0.0.1")
        public_ip = get_public_ip()

        if response != 0 and last_status:
            send_email_alert("Connection Lost", "The WireGuard VPN connection was lost.")
            last_status = False
        elif response == 0 and not last_status:
            if vpn_ip_range in public_ip:
                send_email_alert("Connection Restored", f"VPN connection restored. Public IP: {public_ip}")
            else:
                send_email_alert("Warning", "VPN connection restored, but traffic may not be routed correctly.")
            last_status = True

        time.sleep(5)

# Function to plot latency and traffic data using matplotlib
def plot_graphs():
    plt.clf()  # Clear the previous plot
    plt.subplot(2, 1, 1)
    plt.plot(ping_history, label="Ping Latency (ms)")
    plt.legend(loc="upper left")

    plt.subplot(2, 1, 2)
    plt.plot(traffic_history, label="Traffic Sent/Received (KB)")
    plt.legend(loc="upper left")

    plt.pause(0.05)  # Pause to allow for live updating

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

# Monitor DNS button
dns_btn = tk.Button(root, text="Monitor DNS Queries", command=monitor_dns)
dns_btn.pack(pady=10)

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

# Start matplotlib in interactive mode
plt.ion()
plot_thread = threading.Thread(target=plot_graphs)
plot_thread.start()

# Run the GUI loop
root.mainloop()
