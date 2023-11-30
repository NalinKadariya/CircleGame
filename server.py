# Server
# Imports
import socket
import threading
from information import *
import Server_Functions as server_functions
import time

# Global Variables
gameStarted = False

# GameServer Class
class GameServer:
    # Initialize
    def __init__(self):
        print("Initializing Server...")
        self.players = set()
        self.lock = threading.Lock()  # safety

    # Handle Client Connection
    def handle_client(self, client, address):
        try:
            # Get Username & Connect, and repeat if username is invalid
            while True:
                client.send("Enter your username.".encode('utf-8'))
                player_name = client.recv(1024).decode('utf-8')
        
                with self.lock:  # Locking
                    if player_name not in self.players:
                        self.players.add(player_name)
                        print(f'{player_name} connected to the server. IP: {address[0]}:{address[1]}\n')
                        client.send('Server Connected.'.encode('utf-8'))
                        break
                    else:
                        client.send('Username taken. Please choose another one.'.encode('utf-8'))
                        client.close()

            # Receive Data from Client
            while True:
                data = client.recv(1024).decode('utf-8')

                if not data:
                    print(f'{player_name}: {address[0]}:{address[1]} disconnected.')
                    self.players.remove(player_name)
                    break

                # Functionality
                if data.startswith("-") and not gameStarted:
                    function_name = data[1:]
                    response = self.execute_function(function_name, player_name, client)
                    client.send(response.encode('utf-8'))
                elif gameStarted:
                    print("GAME HAS STARTED!")
                else:
                    client.send('Invalid suffix. Type --new or --help\n'.encode('utf-8'))

        except ConnectionAbortedError:
            print(f'{address[0]}:{address[1]} disconnected abruptly.')
        except Exception as e:
            with self.lock:  # Locking
                print(f'An error {address[0]}:{address[1]}: Exception Type: {type(e).__name__}, Exception: {str(e)}')
                client.send('An error occurred.\n'.encode('utf-8'))
                self.players.remove(player_name)
                client.close()

    # Start Server
    def start_server(self, host=SERVER_HOST, port=SERVER_PORT):
        # Define Server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))

        # Listen & Max Connections
        server.listen(MAX_CONNECTIONS)
        print(f"Server is listening on {host}:{port}...")

        # Accept Connections
        while True:
            client, address = server.accept()
            # Create a new thread for each client
            client_thread = threading.Thread(target=self.handle_client, args=(client, address))
            client_thread.start()

    def execute_function(self, function_name, player_name, client):
        global gameStarted  # Declare the global variable
        if not gameStarted:
            try:
                print(f'{player_name} executed {function_name}')
                if player_name == am[0] and function_name == "start" and not gameStarted:
                    # Handle start command
                    return self.start_game()
                elif function_name == "playerlist":
                    # Handle playerlist command (pass the function for now)
                    return self.get_player_list(player_name)
                else:
                    # Allow other commands for players not in a subserver
                    function_inject = getattr(server_functions, function_name)
                    result = function_inject()
                    if result is not None:
                        return result
                    else:
                        return f'Success {function_name}, No RETURN.'
            except AttributeError:
                return f'Invalid function or command: {function_name} \n'
        else:
            return f'Game has already started. Commands are no longer allowed. \n'

    def start_game(self):
        global gameStarted  # Declare the global variable
        with self.lock:
            gameStarted = True
            print("GAME STARTED\n")

            # Notify clients about the game start
            for player in self.players:
                player.send('GAME STARTED\n'.encode('utf-8'))

            # Clear the screen for all clients
            for player in self.players:
                player.send('\033c'.encode('utf-8'))

            # Display welcome messages
            welcome_messages = [
                "WELCOME TO THE CIRCLE! IT HAS NOW BEGUN!",
                "RULES ARE SIMPLE: THERE ARE NO RULES.",
                "LET THE GAME BEGIN!",
                "THERE IS 45 SECONDS BETWEEN EACH VOTE-OFF",
                "3",
                "2",
                "1",
                "START!"
            ]

            for message in welcome_messages:
                time.sleep(1)
                for player in self.players:
                    player.send((message + '\n').encode('utf-8'))
        
    def get_player_list(self, player_name):
        # Implement the logic for getting the player list
        with self.lock:
            players = ", ".join(self.players)
            return f'Player list: [ {players} ]\n'

# Run Code
if __name__ == "__main__":
    Game_server = GameServer()
    Game_server.start_server()
