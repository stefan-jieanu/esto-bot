import json
import coinmarketscraper

class Wallet:
    def __init__(self):
        self.address = ''
        self.balance = {
            'USDT': 1000,
            'LUSD': 0,
            'ETH': 0.3,
            'ETH_IN_USD': 0
        }

        self.update_usd_balance()

    def update_usd_balance(self):
        price_eth = coinmarketscraper.get_current_usd()
        self.balance['ETH_IN_USD'] = self.balance['ETH'] * price_eth

    def serialize(self):
        wallet_info =  {}

        for key, value in self.balance.items():
            wallet_info[key] = value

        return wallet_info
