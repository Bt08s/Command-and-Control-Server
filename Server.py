import dearpygui.dearpygui as dpg
import threading
import platform
import socket
import os

dpg.create_context()


def clear():
    os.system("cls" if os.name == "nt" else "clear")


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
        try:
            client, address = server.accept()
            clients.append(client)
            print(f"New connection from {address[0]}:{address[1]}")

            t = threading.Thread(target=handle_data, args=(client, address))
            t.start()
        except:
            pass


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
    dpg.add_button(label="Listen", callback=listen, width=75)
    dpg.add_spacer(parent=3)
    dpg.add_input_text(label="Data", tag="server data", multiline=True,
                       default_value=':: Windows\necho "Hello World"\n\nor\n\n# Linux\necho "Hello World"')
    dpg.add_button(label="Send", callback=send_data, width=75)
    with dpg.tooltip(dpg.last_item()):
        dpg.add_text("Send data to all clients in connection")

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
        dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 5)
        dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 5)
        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 5)
        dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 5)
        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 5)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 5, 5)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 5, 5)

        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (21, 22, 23))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (32, 50, 77))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (39, 73, 114))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (32, 50, 77))

clear()
set_console_title("Server")

dpg.bind_theme(global_theme)
dpg.create_viewport(title='Command and control server by Bt08s', width=600, height=287)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Server window", True)
dpg.start_dearpygui()
dpg.destroy_context()
