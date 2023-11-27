# Client
# imports
import socket
import time
import os

# other Scripts
from information import *

# Centered text print
def print_centered_text(message):
    os.system('clear' if os.name == 'posix' else 'cls')
    columns = os.get_terminal_size().columns
    print(message.center(columns))

def connect_to_server(host=SERVER_HOST, port=SERVER_PORT):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the server
    client.connect((host, port))

    # loading screen
    loading_messages = ["Loading.", "Loading..", "Loading..."]

    for message in loading_messages:
        print_centered_text(message)
        time.sleep(0.5)

    # simulate "CIRCLE" display
    print_centered_text("CIRCLE")
    time.sleep(2)

    # Wait for server response to get the initial message
    initial_message = client.recv(1024).decode('utf-8')
    print_centered_text(initial_message)

    # Check if the initial message contains "Enter your username"
    if "Enter your username" not in initial_message:
        # If not, print an error message and return
        print_centered_text("Unexpected server response. Exiting...")
        return

    # get player name from the user
    player_name = input("Select a username: ")
    client.send(player_name.encode('utf-8'))

    data = client.recv(1024).decode('utf-8')
    print_centered_text(data)
    
    # Check if the server response contains "Server Connected"
    if "Server Connected" not in data:
        # If not, username is taken, try again
        print_centered_text("Username taken. Please reconnect and try with another one...")
        return

    time.sleep(2)
    
    # simulate "Main Menu" display
    print_centered_text("CIRCLE")
    print(f'\n{player_name}, Welcome to CIRCLE. New Player? Type "--new" for instructions.')

    # Continue with the rest of your client code
    while True:
        message = input(f'{player_name}: ')
        # Check for empty message
        
        if message.strip() == "":
            print("Error: Empty messages are not allowed.")
            continue

        # Check if the message starts with '-' (ignore it)
        if message.startswith('-'):
            # Send the message to the server
            client.send(message[1:].encode('utf-8'))
        else:
            print("Error: Invalid command.")
            continue
        
        # Recive data from server and print it
        data = client.recv(1024).decode('utf-8')
        print(data)



# Function to display centered text and clear the screen
def display_centered_text(message):
    os.system('clear' if os.name == 'posix' else 'cls')
    print_centered_text(message)

# Run Code
if __name__ == "__main__":
    connect_to_server()
