import os
import socket
from threading import Thread
import time
import pickle

# Function to check received message against current state
def check(received_dict, recv_string_message):
    # Initialize status variable to 0
    status = 0
    # Split the received message to extract data
    data_received = recv_string_message.split(':')
    # If the data is A and this process is C, wait for 50 seconds
    if data_received[0] == 'A' and name == 'C':
        time.sleep(50)
    # Check the received data against the current state
    for value in received_dict:
        if received_dict[value] <= V_local[value] and value != data_received[0]:
            status += 1
        elif value == data_received[0] and received_dict[value] > V_local[value]:
            status += 1
        else:
            status = 0
            break
    # Update the current state if the received data is valid
    if status != 0:
        for value in received_dict:
            if received_dict[value] > V_local[value]:
                V_local[value] = received_dict[value]
    # Otherwise, buffer the request
    else:
        if process != data_received[0]:
            print("local")
            print(V_local)
            print("Received")
            print(received_dict)
            print("Buffer the request")
            waiting = []
            waiting.append(received_dict)
            time.sleep(60)
            dicti = waiting[0]
            for value in dicti:
                if dicti[value] > V_local[value]:
                    V_local[value] = dicti[value]
            # print("after some time")
            # print(V_local)
    # Print the message and current state
    print('\r%s\n' % recv_string_message, end='')
    print(V_local)

# Function to receive and process incoming messages
def MessageTransfer():
    # Declare global variables
    global process
    global broadcastSocket
    global current_online
    global V_local
    # Initialize the local state dictionary
    V_local = {}
    while True:
        # Receive the message
        recv_message = broadcastSocket.recv(1024)
        recv_string_message = str(recv_message.decode('utf-8'))
        # Check if the message contains data or is an online status message
        if recv_string_message.find(':') != -1:
            recv_message1 = broadcastSocket.recv(1024)
            received_dict = pickle.loads(recv_message1)
            # Process the received message in a separate thread
            Thread1 = Thread(target=check, args=(received_dict, recv_string_message))
            Thread1.start()
        elif recv_string_message.find('!@#') != -1 and recv_string_message.find(':') == -1 and recv_string_message[3:] in current_online:
            current_online.remove(recv_string_message[3:])
            V_local.pop(recv_string_message[3:])
        elif recv_string_message not in current_online and recv_string_message.find(':') == -1:
            current_online.append(recv_string_message)
            V_local[recv_string_message] = 0
def SendBroadcastMessageForChat():
    global V_local
    global name
    global sendSocket

    # do not block the socket from which broadcast messages are sent
    sendSocket.setblocking(False)

    while True:
        data = input()
        if data == 'Exit':
            # send an exit message to all peers and exit the program
            close_message = '!@#' + name
            sendSocket.sendto(close_message.encode('utf-8'), ('255.255.255.255', 8080))
            os._exit(1)
        elif data != '' and data != 'Exit()':
            # increment the local clock of the current process
            V_local[process] += 1
            # serialize the local clock and send it with the message to peers
            serialized_dict = pickle.dumps(V_local)
            send_message = process + ': ' + data
            sendSocket.sendto(send_message.encode('utf-8'), ('255.255.255.255', 8080))
            sendSocket.sendto(serialized_dict, ('255.255.255.255', 8080))
        else:
            # prompt user to write a message first if the message is empty or Exit() command is used
            print('Write a message first!')


def SendBroadcastOnlineStatus():
    global process
    global sendSocket

    # do not block the socket from which online status messages are sent
    sendSocket.setblocking(False)

    while True:
        # send the current process ID as an online status message every second
        time.sleep(1)
        sendSocket.sendto(process.encode('utf-8'), ('255.255.255.255', 8080))

# main function
def main():
    global broadcastSocket
    global sendSocket
    global process
    global recvThread
    global sendMsgThread
    global current_online
    # socket for receiving messages from peers
    broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcastSocket.bind(('0.0.0.0', 8080))
    # socket to implement sending
    sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sendSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print('--------------------------')
    # prompt user to enter the current process ID
    process = ''
    while True:
        if not process:
            process = input('Enter processes :')
            if not process:
                print('Enter the process and dont leave it blank')
            else:
                break
    print('-----------------------------')

    # create threads
    global recvThread
    recvThread = Thread(target=MessageTransfer)

    global sendMsgThread
    sendMsgThread = Thread(target=SendBroadcastMessageForChat)

    global current_online
    current_online = []

    global sendOnlineThread
    sendOnlineThread = Thread(target=SendBroadcastOnlineStatus)

    recvThread.start()
    sendMsgThread.start()
    sendOnlineThread.start()
    recvThread.join()
    sendMsgThread.join()
    sendOnlineThread.join()


if __name__ == '__main__':
    main()