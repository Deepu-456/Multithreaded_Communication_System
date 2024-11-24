import socket
import threading
import random

# Define the host and port for the server
SERVER_HOST = "localhost"
SERVER_PORT = 9000

# Initialize a clock variable with a random integer between 1 and 10
clock = random.randint(1, 10)

# Create a dictionary to store client addresses and their clock values
client_clocks = {}

# Initialize a counter to keep track of the number of connected clients
client_counter = 0

# Create a list to store the client connections
client_connections = []

# Define a function to calculate the average of all client clocks and broadcast it to all clients
def broadcast_avg(conn):
    global client_clocks

    # Calculate the total time and number of clients
    total_time = float(clock) + sum(client_clocks.values())
    num_clients = len(client_clocks) + 1

    # Calculate the average and format it to 2 decimal places
    avg_time = total_time / num_clients
    avg_time = "{:.2f}".format(avg_time)
    avg_time = str(avg_time)

    # Send the average to all clients in the list
    for client_conn in client_connections:
        client_conn.send(avg_time.encode())

    # Print the average on the server side
    print("Average at Server: ", avg_time)

    return avg_time

# Define a function to handle a client connection
def handle_client(conn, addr):
    global client_counter
    global clock
    client_counter += 1
    print(f"New client connected: {addr}")

    connected = True
    while connected:
        # Receive the client's clock value
        msg = conn.recv(1024).decode()

        # Store the client's clock value in the dictionary
        with threading.Lock():
            client_clocks[addr] = float(msg)

        # Send a confirmation message to the client
        msg = f"Clock received: {msg}."
        conn.send(msg.encode())

        # If there are at least 2 clients connected, calculate and broadcast the average clock
        if client_counter >= 2:
            avg_time = broadcast_avg(conn)
            print("Updated clock: ", avg_time)
            clock = float(avg_time)

# Define the main function to start the server
def main():
    # Print the initial clock value on the server side
    print(f"Initial clock value at server: {clock}")

    # Create a socket object and bind it to the host and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()

    # Accept client connections and start a thread for each client
    while True:
        conn, addr = server_socket.accept()
        client_connections.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
