import socket
import threading
import json

from config import Config, Protocol
from trader import Trader
from wallet import Wallet

class Server:
    connection = None
    is_running = True
    active_connections = []
    wallet = None
    trader = None
    trader_thread = None

    def init():
        print('Server is initializing...')

        Server.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Server.connection.bind(Config.SERVER_ADDR)

        Server.wallet = Wallet()
        Server.trader = Trader(Server.wallet)

    def start():
        Server.connection.listen()
        print(f'[Listening on]: {Config.SERVER}:{Config.PORT}')

        # Start the trader bot
        Server.trader_thread = threading.Thread(target=Server.trader.run)
        Server.trader_thread.start()

        # Start the server loop
        while Server.is_running:
            conn, addr = Server.connection.accept()
            thread = threading.Thread(target=Server.handle_client, args=(conn, addr))
            thread.start()
            print(f'[Active connections]: {len(Server.active_connections) + 1}')

    def handle_client(conn, addr):
        print(f'[New connection]: {addr}')
        Server.active_connections.append(conn)

        # Listen for data from the client
        connected = True
        while connected:
            data = Protocol.recv(conn, addr)

            # Check for flags in the message
            if data == Protocol.WRONG_HEADER:
                print(f'[Wrong header on send from]: {addr}')
                Server.active_connections.remove(conn)
                break
            elif data == Protocol.DISCONECT_MSG:
                print(f'[User disconnect]: {addr}')
                Server.send(conn, Protocol.DISCONNECT_OK)
                Server.active_connections.remove(conn)
                connected = False
                break
            elif data == Protocol.PING_CLIENTS:
                Server.send_to_all(Protocol.PING)
                continue
            elif data == Protocol.QUERY_INFO:
                trader_info = Server.trader.serialize()
                wallet_info = Server.wallet.serialize()

                query_info = {
                    'query_info': {}
                }

                query_info['query_info']['trader_info'] = trader_info
                query_info['query_info']['wallet_info'] = wallet_info
                query_info = json.dumps(query_info, indent=4)

                Server.send(conn, query_info)
            elif data == Protocol.STOP:
                Server.is_running = False

            print(f'[Data]: {data}')        

    def send(conn, data):
        if not Protocol.send(conn, data):
            print('[Error sending data]')

    def send_to_all(data):
        # Loop through the clients and send a message to them
        for conn in Server.active_connections:
            client_host, client_port = conn.getpeername()

            print(f'- {client_host}:{client_port}')
            Protocol.send(conn, data)


Server.init()
Server.start()