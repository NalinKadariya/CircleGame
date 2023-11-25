# Server
# Imports
import socket

# Other Scripts
from information import *

# GameServer Class
class GameServer:
    # Initialize
    def __init__(self):
        print("Initializing Server...")
        self.players = set()

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
            try:
                player_name = client.recv(1024).decode('utf-8')

                # Trying to Connect
                print(f'{address[0]}:{address[1]} is trying to connect to the server.')  # 0 = IP, 1 = Port
               
                # Get Username & Connect, and repeat if username is invalid
                while not player_name or not self.is_valid_player(player_name):
                    client.send("Username taken. Please reconnect and try with another one...".encode('utf-8'))
                    player_name = client.recv(1024).decode('utf-8')

                self.players.add(player_name)
                print(f'{player_name} connected to the server. IP: {address[0]}:{address[1]}\n')    
                
                # Sending Data
                client.send('Server Connected.'.encode('utf-8'))


                # Game Logic
                while True:
                    data = client.recv(1024).decode('utf-8')
                    if not data:
                        print(f'{player_name} disconnected from the server. IP: {address[0]}:{address[1]}\n')
                        self.players.remove(player_name)
                        break

            # Error handling 
            except ConnectionAbortedError:
                print(f'{address[0]}:{address[1]} disconnected abruptly.')
            except Exception as e:
                print(f'An error occurred for {address[0]}:{address[1]}: Exception: {e}')
                client.close()

    # Check Player Set
    def is_valid_player(self, player_name):
        return player_name not in self.players

# Run Code
if __name__ == "__main__":
    Game_server = GameServer()
    Game_server.start_server()
