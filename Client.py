import socket
import random

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9000


def client():
    # Initialize a clock variable with a random integer between 1 and 10
    clock = random.randint(1, 10)
    print(f"Local clock value: {clock}")

    # Connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to server {SERVER_HOST}:{SERVER_PORT}")

        # Send the local clock value to the server
        s.send(str(clock).encode())

        # Receive the updated clock value from the server
        data = s.recv(1024).decode()
        print(f"Received updated clock value: {data}")


if __name__ == "__main__":
    client()
