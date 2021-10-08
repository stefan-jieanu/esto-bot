import asyncio
import datetime
import random
import websockets
import json

from log import Log
from trader import Trader

class Command:
    START = '!START'
    STOP = '!STOP'
    SEND_TRADER_INFO = '!SEND_TRADER_INFO'
    SEND_WALLET_INFO = '!SEND_WALLET_INFO'
    SET_TRADER_INFO = '!SET_TRADER_INFO'
    SET_WALLET_INFO = '!SET_WALLET_INFO'
    BROADCAST = '!BROADCAST'
    PING = '!PING' 
    NONE = '!NONE'
    GET_ALL = '!GET_ALL'

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.connected = set()

    async def consumer_handler(self, websocket, path):
        async for message in websocket:
            await self.consume(websocket, message)

    async def handle_conn(self, websocket, path):
        # Register new connections
        self.connected.add(websocket)

        await self.send(websocket, self.trader.serialize())        

        try:
            while True:
                await self.consumer_handler(websocket, path)
        finally:
            self.connected.remove(websocket)

    async def consume(self, websocket, message):
        try:
            message = json.loads(message)
            if 'command' in message:
                # Check the command
                if message['command'] == Command.STOP:
                    self.trader.stop()
                    return 
                elif message['command'] == Command.START:
                    self.trader.start()
                    return
                elif message['command'] == Command.SEND_TRADER_INFO:
                    await self.send(websocket, self.trader.serialize())
                    return
                elif message['command'] == Command.SEND_WALLET_INFO:
                    await self.send(websocket, self.wallet.serialize())
                    return
                elif message['command'] == Command.SET_TRADER_INFO:
                    self.trader.set_info(message['trader_info'])
                    return
                elif message['command'] == Command.SET_WALLET_INFO:
                    self.wallet.set_info(message['wallet_info'])
                    return
                elif message['command'] == Command.BROADCAST:
                    return 
                elif message['command'] == Command.PING:
                    return 
                elif message['command'] == Command.NONE:
                    Log.info(message['data'])
                    return

                Log.warn('Unrecognized command')
            else:
                Log.warn('Invalid json format message from client')
        except:
            Log.warn('Could not convert client message to json')

    async def send(self, websocket, message):
        await websocket.send(message)

    async def send_to_all(self, message):
        async for socket in self.connected:
            await self.send(socket, message)
    
    def assign_trader(self, trader):
        self.trader = trader

    def run(self):
        socket_server = websockets.serve(self.handle_conn, self.host, self.port)
        Log.info(f'Started server on {self.host}:{self.port}')

        asyncio.get_event_loop().run_until_complete(socket_server)
        asyncio.get_event_loop().run_forever()


