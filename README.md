# Multithreaded Communication System

This project implements a multithreaded client-server communication system using Python sockets. It supports both unicast and broadcast communication, along with logical vector clocks for synchronizing events.

## Features
- **Client-Server Model**: A server to handle multiple clients concurrently using threads.
- **Vector Clock Synchronization**: Tracks the order of events across clients.
- **Broadcast and Unicast Messaging**: Clients can send messages to the server or broadcast them to other clients.
- **Interactive CLI**: Command-line-based communication between clients and server.

---

## Project Structure
- **`Server.py`**:
  - A multithreaded server that handles connections from multiple clients and synchronizes clocks.
- **`Client.py`**:
  - A CLI-based client that connects to the server and sends/receives messages.
- **`Threaded_Client.py`**:
  - `Readme.txt`: Execution steps and prerequisite information.

---

## Prerequisites
- Python 3.x installed on your system.
- A text editor or IDE such as PyCharm for development.

---

## How to Run
### Step 1: Start the Server
Run the server script:
python3 Server.py

### Step 2: Start Clients
In separate terminals, run the client scripts:
python3 Client.py

### Step 3: Send Messages
Use the CLI to send messages.
Observe the vector clock synchronization and message broadcasts.

