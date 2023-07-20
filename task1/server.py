import sys
import socket as socket_module


class SocketServer:
    
    host = 'localhost'

    def __init__(self) -> None:
        if len(sys.argv) != 2:
            print("Incorrect usage, please use this format\npython server.py <PORT>")
            exit(1)
        
        try:
            self.port = int(sys.argv[1])
        except ValueError:
            print("Please provide a valid port number")
            exit(1)


    def start(self):
        # creating a ip tcp socket
        server_socket = socket_module.socket(
            socket_module.AF_INET, socket_module.SOCK_STREAM)

        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Client connected: {client_address[0]}:{client_address[1]}")

                while True:
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break
                    print(f"Received from client: {data}")

                client_socket.close()
                print("Client disconnected")

        except KeyboardInterrupt:
            print("Server terminated.")

        finally:
            server_socket.close()

socket_server = SocketServer()
socket_server.start()
