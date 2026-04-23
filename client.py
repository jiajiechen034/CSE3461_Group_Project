from socket import *
import threading

# 1: Create a TCP client socket
serverName = input("Enter server IP address: ").strip()
if not serverName:
    serverName = "127.0.0.1"
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)

# 2: Connect to the server using the server’s IP address and port
clientSocket.connect((serverName, serverPort))

# 3: Display the client’s local address and port information
print("Connected to server")
print("Local address:", clientSocket.getsockname())


# 4: Background thread to receive messages
def receiveMessages():
    while True:
        try:
            message = clientSocket.recv(1024)

            if not message:
                print("Server disconnected")
                break

            print("Received:", message.decode())
        except:
            print("Disconnected from server")
            break


thread = threading.Thread(target=receiveMessages)
thread.daemon = True
thread.start()


# 5: Send messages
while True:
    sentence = input()

    if sentence.lower() == "exit":
        break

    clientSocket.send(sentence.encode())

# 6: Close connection
clientSocket.close()
print("Client closed")