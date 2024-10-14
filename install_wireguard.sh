#!/bin/bash

# Update the system
sudo apt update && sudo apt upgrade -y

# Install WireGuard
sudo apt install wireguard -y

# Enable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf

# Set up UFW rules
sudo ufw allow 51820/udp
sudo ufw enable

echo "WireGuard installation completed."
