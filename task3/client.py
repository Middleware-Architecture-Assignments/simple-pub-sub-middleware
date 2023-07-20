import sys
import socket as socket_module

class SocketClient:
    def __init__(self, host : str, port: int, client_type: str, topic: str):
        self.host = host
        self.port = port
        self.client_type = client_type
        self.topic = topic

    def start(self):
        try:
            # Create a TCP socket
            client_socket = socket_module.socket(socket_module.AF_INET, socket_module.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            print(f"Connected to middleware at {self.host}:{self.port}")
            
            # Send the initial message establish the client type and topic
            if self.client_type == "PUBLISHER":
                client_socket.sendall(f"PUBLISH TO %%%%%{self.topic}".encode('utf-8'))
            elif self.client_type == "SUBSCRIBER":
                client_socket.sendall(f"SUBSCRIBE TO %%%%%{self.topic}".encode('utf-8'))
                
            
            while True:
                if(self.client_type == "SUBSCRIBER"):
                    try:
                        while True:
                            data = client_socket.recv(1024).decode('utf-8')
                            if not data:
                                break
                            print(f"Received from middleware: {data}")

                        client_socket.close()
                        print(f"Middleware disconnected")

                    except Exception as e:
                        print(f"Error handling middleware", e)
                        exit(1)
                else:
                    message = input("Enter a message (type 'terminate' to exit): ")
                    if message == "terminate":
                        raise KeyboardInterrupt()
                    # Send the message to the server
                    client_socket.sendall(message.encode('utf-8'))

        except KeyboardInterrupt:
            print("Client terminated.")

        finally:
            client_socket.close()

# Get the host and port from the command line arguments
if len(sys.argv) != 5:
    print("Incorrect usage, please use this format: python client.py <HOST> <PORT> <CLIENT_TYPE(either publisher or subscriber)> <TOPIC>")
    exit(1)

host = sys.argv[1]
port = int(sys.argv[2])
client_type = sys.argv[3]
topic = sys.argv[4]

if (client_type != "PUBLISHER") and (client_type != "SUBSCRIBER"):
    print("Client type is not valid.Please use PUBLISHER or SUBSCRIBER to indicate type")
    exit(1)

if topic.startswith("%"):
    print("Topics shouldn't start with %")
    exit(1)

# Create and start the client
socket_client = SocketClient(host, port, client_type, topic)
socket_client.start()
