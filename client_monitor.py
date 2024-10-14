import tkinter as tk
import subprocess
import os

def check_connection():
    response = os.system("ping -c 1 10.0.0.1")
    if response == 0:
        result_label.config(text="Connected to Server", fg="green")
    else:
        result_label.config(text="Disconnected", fg="red")

def restart_wireguard():
    os.system("sudo wg-quick down wg0 && sudo wg-quick up wg0")
    result_label.config(text="WireGuard Restarted", fg="blue")

root = tk.Tk()
root.title("WireGuard Client Monitor")

connection_btn = tk.Button(root, text="Check Connection", command=check_connection)
connection_btn.pack(pady=10)

restart_btn = tk.Button(root, text="Restart WireGuard", command=restart_wireguard)
restart_btn.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()
