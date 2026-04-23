from socket import *
import threading

# Algorithm 3: High-level Server Logic for One-to-One Chat

# Create a TCP server socket and bind it to an IP address and port
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', 12000))

# Start listening for incoming client connections
serverSocket.listen(5)
print("The server is ready...")

# Initialize an empty dictionary to store each client's username and socket
clients_dict = {}

# Client Handler
def handle_client(clientSocket, user_addr, username):
    while True:
        try:
            # Wait to receive a message from the client
            message = clientSocket.recv(1024).decode().strip()

            # Check if client disconnected
            if not message:
                break

            # if message starts with @target then
            if message.startswith("@"):
                # Extract the target username and message text
                pts = message.split(" ", 1)
                target = pts[0][1:].strip()  # remove '@'

                # Check format first
                if len(pts[0]) <= 1:
                    clientSocket.send("Invalid format! Use (@username message)\n".encode())
                    continue

                # Check if username exist
                if target not in clients_dict:
                    clientSocket.send("Error! User not found\n".encode())
                    continue

                # Prevent self-messaging
                if target == username:
                    clientSocket.send("Error! You cannot message yourself\n".encode())
                    continue

                # Check message is blank
                if len(pts) < 2 or not pts[1].strip():
                    clientSocket.send("Message was blank!\n".encode())
                    continue

                # Get actual message
                msg = pts[1].strip()

                # if target username exists in the client dictionary then
                # Send the message only to that specific target client
                clients_dict[target].send(f"[Private message from {username}]: {msg}\n".encode())

            else:
                # Inform the sender to use the correct format (@username message)
                clientSocket.send("Invalid! Use format: (@username message) to send messages\n".encode())

        except:
            break

    # Remove client when disconnected
    if username in clients_dict:
        del clients_dict[username]
    clientSocket.close()
    print(f"{username} disconnected")

# While server is running do
while True:
    # Accept a new client connection
    clientSocket, user_addr = serverSocket.accept()

    # Request and receive the client's username
    clientSocket.send("Enter your username: ".encode())
    username = clientSocket.recv(1024).decode().strip()

    # Add the username-socket pair to the dictionary
    clients_dict[username] = clientSocket
    clientSocket.send(f"Welcome {username}! Please use @username message to chat privately.\n".encode())

    print(f"{username} joined")

    # Start a new thread to handle communication with that client
    thread = threading.Thread(target=handle_client, args=(clientSocket, user_addr, username))
    thread.start()