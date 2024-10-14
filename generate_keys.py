import os

def generate_key_pair():
    private_key = os.popen("wg genkey").read().strip()
    public_key = os.popen(f"echo {private_key} | wg pubkey").read().strip()
    return private_key, public_key

# Generate server keys
server_private_key, server_public_key = generate_key_pair()
print(f"Server Private Key: {server_private_key}")
print(f"Server Public Key: {server_public_key}")

# Generate client keys
client_private_key, client_public_key = generate_key_pair()
print(f"Client Private Key: {client_private_key}")
print(f"Client Public Key: {client_public_key}")
