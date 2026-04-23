from socket import *
import threading

# Algorithm 4: High-level Client Logic for One-to-One Chat

# Create a TCP client socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to the server using the provided IP address and port
serverName = input("Enter server IP address: ").strip()
if not serverName:
    serverName = "127.0.0.1"
clientSocket.connect((serverName, 12000))

# Wait for the server to request a username
print(clientSocket.recv(1024).decode(), end="")

# Input the username from the user and send it to the server
username = input()
clientSocket.send(username.encode())

# Start a background thread to continuously receive and display messages
def receive_messages():
    while True:
        try:
            # Receive incoming messages from the server
            message = clientSocket.recv(1024).decode()

            if not message:
                break

            # Display received messages to the user
            print(message)
        except:
            # If server disconnects or error occurs, close the connection
            print("Disconnected from server.")
            clientSocket.close()
            break

recv_thread = threading.Thread(target=receive_messages)
recv_thread.daemon = True
recv_thread.start()

# In the main thread, repeatedly accept and send user input
print("To send a private message type: (@username message)")
while True:
    try:
        # Accept user input from the keyboard
        message = input()

        # To send a private message, type in the format @username message
        # Send the message to the server for delivery to the target user
        clientSocket.send(message.encode())

    except:
        # If error occurs, close the socket connection
        clientSocket.close()
        break