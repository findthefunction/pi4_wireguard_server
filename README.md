# WireGuard Monitoring Tool

This tool provides real-time monitoring for a WireGuard VPN setup, including graphical statistics, email alerts, robust connection monitoring, and DNS request tracking.

## Features
- Real-time latency and traffic statistics (using `matplotlib`).
- Connection status and WireGuard service logs.
- Email alerts when the connection is lost or restored.
- DNS query monitoring.
- Automatic restart of WireGuard on failure.
- Public IP checking to verify if the traffic is routed through the VPN.

## Installation

### Dependencies

Install the following dependencies:

```bash
sudo apt update
sudo apt install python3-tk python3-matplotlib python3-requests
```

2. Clone the Repository
Clone the project repository from GitHub:
git clone https://github.com/your-username/wireguard-pi4-setup.git
cd wireguard-pi4-setup
3. Configure the .env File
Create a .env file in the root of the project to securely store secrets like email credentials. The file
should look like this:
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
RECEIVER_EMAIL=receiver-email@gmail.com
Make sure to install python-dotenv to handle the .env file:
pip install python-dotenv
4. Run the Monitoring Tool
After setting up the .env file, you can run the monitoring tool:
python3 client_monitor_gui.py
This will start the GUI to monitor your WireGuard setup in real-time with graphical statistics, logs,
and DNS monitoring.
5. Running Tests
To run tests to validate the setup, use the following command:
python3 -m unittest test_monitoring.py
This will run a series of tests for monitoring features, including checking connection status, DNS
query logging, and email alert functionality.
License
This project is licensed under the MIT License.