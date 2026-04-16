from socket import *
import threading

# 1: Create a TCP server socket and bind it to an IP address and port
serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))

# 2: Start listening for incoming client connections
serverSocket.listen(5)
print("The server is ready to receive")

# 3: Initialize an empty list to store connected clients
clients = []


# 9: Client Handler (in each thread):
def handleClient(connectionSocket, addr):

    # 10: Continuously receive messages from the assigned client
    while True:
        message = connectionSocket.recv(1024)

        if not message:
            break

        # 11: For each received message, forward it to all other connected clients
        for client in clients:
            if client != connectionSocket:
                client.send(message)

    # 12: If the client disconnects, close the connection and remove it from the list
    clients.remove(connectionSocket)
    connectionSocket.close()
    print("Disconnected:", addr)


# 4: while server is running do
while True:
    # 5: Accept a new client connection
    connectionSocket, addr = serverSocket.accept()
    print("Connected by", addr)

    # 6: Add the client to the list of active clients
    clients.append(connectionSocket)

    # 7: Start a new thread to handle communication with that client
    thread = threading.Thread(target=handleClient, args=(connectionSocket, addr))
    thread.start()

# 8: end while