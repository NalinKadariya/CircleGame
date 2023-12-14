import socket
import asyncio
import time
import os

# other Scripts
from information import *

# Centered text print
def print_centered_text(message):
    os.system('clear' if os.name == 'posix' else 'cls')
    columns = os.get_terminal_size().columns
    print(message.center(columns))

async def connect_to_server(host=SERVER_HOST_CLIENT, port=SERVER_PORT):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    loading_messages = ["Loading.", "Loading..", "Loading..."]
    for message in loading_messages:
        print_centered_text(message)
        await asyncio.sleep(0.5)

    print_centered_text("CIRCLE")
    await asyncio.sleep(2)

    initial_message = client.recv(1024).decode('utf-8')
    print_centered_text(initial_message)

    if "Enter your username" not in initial_message:
        print_centered_text("Unexpected server response. Exiting...")
        return

    player_name = input("Select a username: ")
    if player_name == am[0]:
        password = input("Enter the password: ")
        if password == am[1]:
            client.send(player_name.encode('utf-8'))
        else:
            print_centered_text("Wrong password. Please reconnect and try again...")
            return
    else:
        client.send(player_name.encode('utf-8'))

    data = client.recv(1024).decode('utf-8')
    print_centered_text(data)

    if "Server Connected" not in data:
        print_centered_text("Username taken. Please reconnect and try with another one...")
        return

    await asyncio.sleep(2)

    print_centered_text("CIRCLE")
    print(f'\n{player_name}, Welcome to CIRCLE. New Player? Type "--new" for instructions.')

    while True:
        message = input(f'{player_name}: ')
        if message.strip() == "":
            print("Error: Empty messages are not allowed.")
            continue

        if message.startswith('-'):
            client.send(message[1:].encode('utf-8'))
        else:
            print_centered_text("Error: Invalid command. \n")
            continue

        data = client.recv(1024).decode('utf-8')
        print_centered_text(data)

async def main():
    await connect_to_server()

if __name__ == "__main__":
    asyncio.run(main())
