from socket import *
import threading
import time
import random

# 1: Create a TCP server socket and bind it to an IP address and port
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))

# 2: Start listening for incoming client connections
serverSocket.listen(5)
print("The server is ready to receive")

# 3: Initialize an empty list to store connected clients
clients = []

# Feature 3 metrics for simulated delay/jitter
total_delayed_messages = 0
total_delay_seconds = 0.0
min_delay = None
max_delay = None
metrics_lock = threading.Lock()


def updateAndPrintDelayMetrics(delay):
    # Keep metric updates thread-safe because each client runs in its own thread.
    global total_delayed_messages, total_delay_seconds, min_delay, max_delay
    with metrics_lock:
        total_delayed_messages += 1
        total_delay_seconds += delay
        if min_delay is None or delay < min_delay:
            min_delay = delay
        if max_delay is None or delay > max_delay:
            max_delay = delay
        avg_delay = total_delay_seconds / total_delayed_messages
        print(
            f"[Delay Metrics] total={total_delayed_messages}, "
            f"avg={avg_delay:.3f}s, min={min_delay:.3f}s, max={max_delay:.3f}s"
        )


# 9: Client Handler (in each thread):
def handleClient(connectionSocket, addr):
    # 10: Continuously receive messages from the assigned client
    while True:
        try:
            message = connectionSocket.recv(1024)

            if not message:
                break

            # 11: For each received message, forward it to all other connected clients
            for client in clients:
                if client != connectionSocket:
                    # Feature 3: simulate server-side latency/jitter before forwarding
                    delay = random.uniform(0.2, 1.0)
                    time.sleep(delay)
                    client.send(message)
                    updateAndPrintDelayMetrics(delay)
        except:
            break

    # 12: If the client disconnects, close the connection and remove it from the list
    if connectionSocket in clients:
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