import socket
import threading
import random

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 5066

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server socket to the host and port
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Listen for incoming connections
server_socket.listen()

# Store client connections and their phone numbers
clients = {}

# Store phone numbers and verification codes
phone_verification = {}

# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    
    # Ask user to register with phone number
    phone_number = client_socket.recv(1024).decode('utf-8')
    
    # Check if the phone number is already registered
    if phone_number in clients:
        client_socket.send("Phone number already registered with another user. Please use a different phone number.".encode('utf-8'))
        client_socket.close()
        print(f"[DISCONNECTED] {client_address} disconnected due to duplicate phone number.")
        return
    
    # Generate and send verification code
    verification_code = ''.join(random.choices('0123456789', k=4))
    phone_verification[phone_number] = verification_code
    client_socket.send(f"Verification code sent to {phone_number}: {verification_code}".encode('utf-8'))
    
    # Receive verification code from client
    client_verification_code = client_socket.recv(1024).decode('utf-8')
    
    # Check if verification code matches
    if client_verification_code == phone_verification.get(phone_number):
        client_socket.send("Registration and authentication successful. You can now start chatting.".encode('utf-8'))
        
        # Store client connection using phone number as username
        clients[phone_number] = client_socket
        
        while True:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            
            # Parse recipient phone number from message
            recipient, message_content = message.split(':')
            
            # Check if the recipient is connected
            if recipient in clients:
                # Send the message to the recipient
                recipient_socket = clients[recipient]
                recipient_socket.send(f"{phone_number}: {message_content}".encode('utf-8'))
            else:
                client_socket.send(f"Recipient '{recipient}' is not connected.".encode('utf-8'))

        # Remove client from the list and close the connection
        del clients[phone_number]
        client_socket.close()
        print(f"[DISCONNECTED] {client_address} disconnected.")
    else:
        client_socket.send("Invalid verification code. Please try again.".encode('utf-8'))
        client_socket.close()

# Main function to accept client connections
def start_server():
    print("[SERVER STARTED] Waiting for incoming connections...")
    while True:
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()
        # Create a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

start_server()

