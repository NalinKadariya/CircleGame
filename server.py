# Server
# Imports
import socket
import threading

# Other Scripts
from information import *
import Server_Functions as server_functions

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
                if data.startswith("-"):
                    function_name = data[1:]
                    response = self.execute_function(function_name)
                    client.send(response.encode('utf-8'))
                else:
                    client.send('Invalid suffix. Type --new or --help'.encode('utf-8'))
    

        except ConnectionAbortedError:
            print(f'{address[0]}:{address[1]} disconnected abruptly.')
        except Exception as e:
            with self.lock:  # Locking
                print(f'An error occurred for {address[0]}:{address[1]}: Exception Type: {type(e).__name__}, Exception: {str(e)}')
                self.players.remove(player_name)

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
    
    def execute_function(self, function_name):
        try:
            function_inject = getattr(server_functions, function_name)
            result = function_inject()
            if result is not None:
                return result
            else:
                return f'Sucess {function_name}, No RETURN.'
        except AttributeError:
            return f'Invalid function name: {function_name}'

# Run Code
if __name__ == "__main__":
    Game_server = GameServer()
    Game_server.start_server()
