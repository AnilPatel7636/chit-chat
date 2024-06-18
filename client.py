import socket
import threading
import time

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 5066

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Flag to indicate if an error occurred
error_occurred = False

# Function to send messages
def send_message():
    global error_occurred
    
    # Prompt user to register with phone number
    phone_number = input("Enter your phone number to register: ")
    # Send phone number to server
    client_socket.send(phone_number.encode('utf-8'))

    # Receive and print verification code from server
    verification_code = client_socket.recv(1024).decode('utf-8')
    print(verification_code)
    time.sleep(1)
    # Check if the phone number is already registered
    if verification_code.startswith("Phone number already registered"):
        print("Authentication failed due to duplicate phone number. Closing connection.")
        error_occurred = True
        client_socket.close()  # Close the socket if authentication fails
        return
    
    # Prompt user to enter verification code
    client_verification_code = input("Enter the verification code: ")
    # Send verification code to server
    client_socket.send(client_verification_code.encode('utf-8'))
    time.sleep(0.5)
    time.sleep(1)
    # Check if an error occurred during authentication
    if error_occurred:
        return  # Exit function if an error occurred
    
    while True:
        recipient = input("Enter the recipient's phone number: ")
        message_content = input("Enter your message: ")
        message = f"{recipient}:{message_content}"
        client_socket.send(message.encode('utf-8'))

# Function to receive messages
def receive_message():
    global error_occurred
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break  # Break the loop if no message received
            if message.startswith("Invalid verification code"):
                print("Authentication failed due to invalid verification code. Closing connection.")
                error_occurred = True
                client_socket.close()  # Close the socket if authentication fails
                break
            print(f"\nReceived message: {message}")
        except ConnectionError:
            print("Connection closed.")
            break


# Create threads for sending and receiving messages
send_thread = threading.Thread(target=send_message)
receive_thread = threading.Thread(target=receive_message)

# Start the threads
send_thread.start()
receive_thread.start()

# Join the threads
send_thread.join()
receive_thread.join()

