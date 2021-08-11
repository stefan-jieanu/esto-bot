import socket
import threading
from config import Config, Protocol

class ClientConnection:
    connection = None
    is_connected_to_server = True

    client_data_callback = None

    # SERVER_ADDR = ('134.122.95.110', 5050)

    def init():
        print('Client is initializing...')
        ClientConnection.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ClientConnection.connection.connect(Config.SERVER_ADDR)

        thread = threading.Thread(target=ClientConnection.handle_server, 
            args=(ClientConnection.connection, Config.SERVER_ADDR))
        thread.start()

    def set_client_data_callback(callback):
        ClientConnection.client_data_callback = callback

    def send(data):
        if not Protocol.send(ClientConnection.connection, data):
            print('[Error sending data]')

    def handle_server(conn, addr):
        print(f'[Connected to server]: {addr}')

        while ClientConnection.is_connected_to_server:
            data = Protocol.recv(conn, addr)

            # Check for flags in the message
            if data == Protocol.WRONG_HEADER:
                print(f'[Wrong header on send from]: {addr}')
                ClientConnection.send(Protocol.DISCONECT_MSG)
                break
            if data == Protocol.DISCONNECT_OK:
                print(f'[Disconnectig from server]')
                ClientConnection.is_connected_to_server = False
                ClientConnection.close_socket_conn()
                break
            if data == Protocol.PING:
                print(f'[Data]: {data}')
                ClientConnection.client_data_callback(data)
                continue
            
            ClientConnection.client_data_callback(data)

    def close_socket_conn():
        # Close the socket connection
        ClientConnection.connection.shutdown(socket.SHUT_RDWR)
        ClientConnection.connection.close()

    def disconnect():
        ClientConnection.send(Protocol.DISCONECT_MSG)
