# Example of a client 
import socket

def start_client():
    username = input("Enter your username: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))
    client.send(username.encode('utf-8'))

    while True:
        data = client.recv(1024).decode('utf-8')
        print(f"{data}")

        print("2. To Exist")
        exit = input("Enter your choice: ")
        if exit == '2':
            client.close()
            break


if __name__ == "__main__":
    start_client()
