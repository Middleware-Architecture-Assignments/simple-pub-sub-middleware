import sys
import socket as socket_module

class SocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        try:
            # Create a TCP socket
            client_socket = socket_module.socket(socket_module.AF_INET, socket_module.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")

            while True:
                message = input("Enter a message (type 'terminate' to exit): ")

                # Send the message to the server
                client_socket.sendall(message.encode('utf-8'))

                if message == 'terminate':
                    print("Terminating client...")
                    break

        except KeyboardInterrupt:
            print("Client terminated.")

        finally:
            client_socket.close()

# Get the host and port from the command line arguments
if len(sys.argv) != 3:
    print("Incorrect usage, please use this format: python client.py <HOST> <PORT>")
    exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

# Create and start the client
socket_client = SocketClient(host, port)
socket_client.start()
