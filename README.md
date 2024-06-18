# Chat Server and Client Application

This repository contains a simple chat server and client application implemented in Python using the `socket` and `threading` modules. The application allows multiple clients to connect to a server, register with a phone number, authenticate via a verification code, and send messages to each other.

## Features

- Multi-threaded server to handle multiple client connections simultaneously.
- Client registration with unique phone numbers.
- Verification system using 4-digit codes.
- Real-time messaging between clients.
- Error handling for duplicate phone numbers and invalid verification codes.

## Getting Started

### Prerequisites

- Python 3.x

### Running the Server

1. Clone the repository.
    

2. Run the server.
    

### Running the Client

1. In a new terminal, navigate to the project directory.

2. Run the client.
   

3. Follow the prompts to register, authenticate, and start sending messages.

## Code Overview

### Server (`server.py`)

- Sets up a server socket to listen for incoming connections.
- Handles client registration and authentication.
- Manages connected clients and facilitates message broadcasting.

### Client (`client.py`)

- Connects to the server.
- Handles user registration and authentication.
- Allows users to send and receive messages.



## License

This project is licensed under the MIT License.
