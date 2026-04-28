## CSE-3461_Group_Project
This project was completed as a group assignment for CSE 3461 (Computer Networking and Internet Technologies). 

The work was developed collaboratively, with each team member contributing to the project.

The goal of this project is to build a simple chat system that allows multiple clients to communicate through a central server. The implementation uses Python sockets and threading to support concurrent communication between users.

## Features
### 1. Broadcast Messaging
Clients can send messages to all other connected clients through the server. The server receives a message from one client and forwards it to every other active client.
This follows the standard client-server communication model described in the assignment.

### 2. Private Messaging (One-to-One Chat)
Clients can send direct messages to a specific user using the format:

    @username message

The server routes the message only to the intended recipient using a username-to-socket mapping.

### 3. Delay/Jitter Simulation
An additional networking feature was implemented to simulate real-world conditions:
- Random delay is added before forwarding messages
- Metrics are tracked, including:
    -  Total delayed messages
    -  Average delay
    -  Minimum and maximum delay

This helps analyze how latency affects communication performance.
[View Assignment PDF](./Project_assignment_SP26.pdf)
