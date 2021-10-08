from server import Server
from trader import Trader
from wallet import Wallet

def main():    
    # Init the trader
    trader = Trader()

    # TODO: Grab these params from env variables
    HOST = '127.0.0.1'
    PORT = 5050
    # Start the server and assign events
    server = Server(HOST, PORT)
    server.assign_trader(trader)
    trader.assign_server(server)

    trader.start()

    # Run the server
    server.run()

if __name__ == "__main__":
    main();
