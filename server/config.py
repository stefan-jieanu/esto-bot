import socket

class Config:
    PORT = 5050
    SERVER = '192.168.8.109'
    SERVER_ADDR = (SERVER, PORT)


class Protocol:
    HEADER_SIZE = 64
    DISCONECT_MSG = '!DISCONECT'
    DISCONNECT_OK = '!DISCONNECT_OK'
    WRONG_HEADER = '!WRONG HEADER'
    PING_CLIENTS = '!PING_CLIENTS'
    QUERY_INFO = '!QUERY_INFO'
    STOP = '!PING_CLIENTS'
    PING = '!PING'
    FORMAT = 'utf-8'

    def recv(conn, addr):
        # Check that the header is set right
        header = conn.recv(Protocol.HEADER_SIZE).decode(Protocol.FORMAT)

        if not header:
            return Protocol.WRONG_HEADER

        data = conn.recv(int(header)).decode(Protocol.FORMAT)
        return data

    def send(conn, data):
        encoded_data = data.encode(Protocol.FORMAT)

        # Getting the length of the message and padding it up to the protocol HEADER_SIZE
        data_length = str(len(encoded_data)).encode(Protocol.FORMAT)
        data_length += b' ' * (Protocol.HEADER_SIZE - len(data_length))

        conn.send(data_length)
        conn.send(encoded_data)

        return True