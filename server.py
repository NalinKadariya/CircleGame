# Server
# Imports
import socket
import threading
import random

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

        self.subservers = {} #Keep track of subservers

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
                    response = self.execute_function(function_name, player_name,client)
                    client.send(response.encode('utf-8'))
                else:
                    client.send('Invalid suffix. Type --new or --help'.encode('utf-8'))
    

        except ConnectionAbortedError:
            print(f'{address[0]}:{address[1]} disconnected abruptly.')
        except Exception as e:
            with self.lock:  # Locking
                (f'An error occurred for {address[0]}:{address[1]}: Exception Type: {type(e).__name__}, Exception: {str(e)}')
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
        try:
            print(f'{player_name} executed {function_name}')
            if function_name == "create":
                return self.create_and_join_subserver(player_name, client) # Create a Server
            elif function_name.split()[0] == "join":
                return self.join_subserver(function_name.split()[1], player_name, client)  # Join a Server
            else:
                function_inject = getattr(server_functions, function_name)
                result = function_inject()
                if result is not None:
                    return result
                else:
                    return f'Success {function_name}, No RETURN.'
        except AttributeError:
            return f'Invalid function or command: {function_name} \n'
    
    # Creating and handling subservers
    def create_and_join_subserver(self, player_name, client):
        subserver_code = self.generate_subserver_code()
        response = self.create_subserver(subserver_code)
        join_response = self.join_subserver(subserver_code, player_name, client)
        return f'{response}\n{join_response}'

    def join_subserver(self, subserver_code, player_name, client):
        if subserver_code in self.subservers:
            subserv = self.subservers[subserver_code]
            subserv.add_player(player_name, client)
            return f'{player_name} joined subserver {subserver_code}'
        else:
            return 'Invalid server code.\n'

    def generate_subserver_code(self):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        numbers = '0123456789'
        uniqueCode = ""
        for i in range(joinCodeLength):
            if i % 2 == 0:
                uniqueCode += random.choice(numbers)
            else:
                uniqueCode += random.choice(alphabet)
        return uniqueCode


# Subsever Class
class SubServer:    
    def __init__(self, code, lock):
        self.code = code
        self.players = {}
        self.lock = lock

    def add_player(self, player_name, client):
        with self.lock:
            if player_name not in self.players:
                self.players[player_name] = client
                print(f'{player_name} joined subserver {self.code}.')
                client.send(f'Joined subserver {self.code}'.encode('utf-8'))
            else:
                client.send('Username taken. Please choose another one.'.encode('utf-8'))
                client.close()


# Run Code
if __name__ == "__main__":
    Game_server = GameServer()
    Game_server.start_server()