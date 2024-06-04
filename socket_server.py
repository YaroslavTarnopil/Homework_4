import socket
import json
from datetime import datetime
import os

STORAGE_DIR = 'storage'
DATA_FILE = os.path.join(STORAGE_DIR, 'data.json')

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

def save_message(data):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            messages = json.load(file)
    else:
        messages = {}

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    messages[timestamp] = data['message']
    
    with open(DATA_FILE, 'w') as file:
        json.dump(messages, file, indent=4)

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 5000)
    sock.bind(server_address)
    
    while True:
        data, address = sock.recvfrom(4096)
        if data:
            message = json.loads(data.decode())
            save_message(message)

if __name__ == '__main__':
    start_server()
