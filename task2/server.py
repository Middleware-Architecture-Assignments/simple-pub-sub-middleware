import sys
import socket as socket_module
import threading

class SocketServer:
    
    host = 'localhost'
    publishers : list[socket_module.socket] = []
    subscribers: list[socket_module.socket] = []

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
                client_handler = ClientHandler(client_socket, client_address, self)
                client_handler.start()

        except KeyboardInterrupt:
            print("Server terminated.")

        finally:
            server_socket.close()


class ClientHandler(threading.Thread):
    def __init__(self, client_socket : socket_module.socket, client_address, socket_server: SocketServer):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        self.server = socket_server

    def run(self):
        try:
            client_type_message = self.client_socket.recv(1024).decode('utf-8')
            if (client_type_message.find("__ESTABLISH_CLIENT_TYPE__ : 'SUBSCRIBER'") != -1):
                
                self.server.subscribers.append(self.client_socket)
                
                print(f"Subscriber connected: {self.client_address[0]}:{self.client_address[1]}")
            elif (client_type_message.find("__ESTABLISH_CLIENT_TYPE__ : 'PUBLISHER'") != -1):
                
                self.server.publishers.append(self.client_socket)
                
                print(f"Publisher connected: {self.client_address[0]}:{self.client_address[1]}")
                while True:
                    data = self.client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break
                    for subscriber in self.server.subscribers:
                        subscriber.sendall(data.encode('utf-8'))
                    print(f"Publisher ({self.client_address[0]}:{self.client_address[1]}): {data}")

                self.client_socket.close()
                print(f"Publisher disconnected: {self.client_address[0]}:{self.client_address[1]}")

        except Exception as e:
            print(f"Error handling client: {self.client_address[0]}:{self.client_address[1]} - {str(e)}")



socket_server = SocketServer()
socket_server.start()
