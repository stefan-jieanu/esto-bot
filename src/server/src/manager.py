class BotManager:
    def __init__(self, trader, server, wallet, eventEmitter):
        self.trader = trader
        self.server = server
        self.wallet = wallet
        self.eventEmitter = eventEmitter

        self.eventEmitter.on('starttrader', self.start_trader)
        self.eventEmitter.on('stoptrader', self.stop_trader)
        self.eventEmitter.on('newconnection', self.send_trader_info)

    def start_trader(self):
        self.trader.start()
    
    def stop_trader(self):
        self.trader.stop()

    def send_trader_info(self, websocket):
        self.server.send(websocket, self.trader.serialize())

    def send_trader_status(self):
        # Send a message telling the status of the trader thread: running, on hold, crashed(god forbid)
        pass

    def send_wallet_info(self):
        # self.server.send(self.wallet.serialize())
        pass
    
    def run(self):
        while True:
            pass