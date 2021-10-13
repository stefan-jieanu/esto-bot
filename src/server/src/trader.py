import json
import threading
import time
import scraper
import wallet
from datetime import datetime

from scipy import stats
from cryptocmd import CmcScraper
from datetime import datetime, timedelta
from log import Log
from emailer import Emailer

# DEFAULT PARAMETERS
# self.high_coefficient = 1.2
# self.low_coefficient = 0.4
# self.buy_point = 0
# self.sell_point = 0
# self.current_traded_coin_price = 0
# self.moving_average_high = 0
# self.moving_average_low = 0
# self.new_buy_point =  0.9988
# self.new_sell_point = 1.02
# self.discard_buy_point = 0.98
# self.discard_sell_point = 1.03
# self.buy_coefficient = 0.996
# self.sell_coefficient = 1.004
# self.max_buy_point = 1
# self.ten_day_moving_average_high = 0
# self.ten_day_moving_average_low = 0
# self.manual_buy_point = 0
# self.manual_sell_point = 0
# self.max_gas_fees = 0.01

class Trader:
    def __init__(self):
        self.running = False
        self.run_thread = threading.Thread(target=self.run)

        self.wallet = wallet.Wallet()

        # Init the variables with the default values
        self.high_coefficient = 1.2
        self.low_coefficient = 0.4
        self.buy_point = 0
        self.sell_point = 0
        # TODO: Change the name lusd to a more generic name
        self.current_traded_coin_price = 0
        self.moving_average_high = 0
        self.moving_average_low = 0
        self.new_buy_point =  0.9988
        self.new_sell_point = 1.02
        self.discard_buy_point = 0.98
        self.discard_sell_point = 1.03
        self.buy_coefficient = 0.996
        self.sell_coefficient = 1.004
        self.max_buy_point = 1
        self.ten_day_moving_average_high = 0
        self.ten_day_moving_average_low = 0
        self.manual_buy_point = 0
        self.manual_sell_point = 0
        self.max_gas_fees = 0.01

        self.emailer = Emailer()

    def assign_server(self, server):
        # Assign the server which will be used to send messages
        self.server = server

    def get_crypto_data(self, dates):
        # initialise scraper 
        scraper = CmcScraper('lusd', dates[1], dates[0])

        # Pandas dataFrame for the same data
        try: 
            return scraper.get_dataframe()
        except:
            return None

    def get_dates(self, start_date, dt):
        dates = []
        d1 = datetime.now() - timedelta(days=start_date)
        d2 = datetime.now() - timedelta(days=(start_date + dt))

        dates.append(d1.strftime("%d-%m-%Y"))
        dates.append(d2.strftime("%d-%m-%Y"))
        return dates


    def swap(self, opts, price):
        if opts == 'buy':
            if price > 0.9999999:
                self.wallet.balance['LUSD'] = self.wallet.balance['USDT'] * price
            elif price <= 0.9999999:
                self.wallet.balance['LUSD'] = self.wallet.balance['USDT'] / price
            self.wallet.balance['USDT'] = 0
        elif opts == 'sell':
            if price > 0.9999999:
                self.wallet.balance['USDT'] = self.wallet.balance['LUSD'] * price
            elif price <= 0.9999999:
                self.wallet.balance['USDT'] = self.wallet.balance['LUSD'] / price
            self.wallet.balance['LUSD'] = 0

        # print(f'Traded! LUSD price: {price}; \nCurrent USDT balance: {self.wallet.balance["USDT"]}; \n Current LUSD balance: {self.wallet.balance["LUSD"]}')\

        # Send a notification to the client of the trade
        # self.server.send('{trade}')

        # Send email that a trade is available
        self.email_trade()
        
        # Log the trade to the file
        self.log_trade()

    def trade_model(self, open_val, high_val, low_val):
        self.current_traded_coin_price = float(scraper.get_curent_lusd())
        Log.debug(self.current_traded_coin_price)

        # This will be without outliers
        # TODO: We need to get this data from 10 days in the past, so do that later
        self.ten_day_moving_average_high = stats.trim_mean(high_val, 0.1)
        self.ten_day_moving_average_low = stats.trim_mean(low_val, 0.1)

        # Convert pandas data frame to numpy array so that it can be manupulated
        high_val_arr = high_val.to_numpy()
        low_val_arr = low_val.to_numpy()

        # high from yesterday
        if high_val_arr[0] > 1.04:
            high_val_arr[0] = self.ten_day_moving_average_high

        # high from two days ago
        if high_val_arr[1] > 1.04:
            high_val_arr[1] = self.ten_day_moving_average_high

        # high from three days ago
        if high_val_arr[2] > 1.04:
            high_val_arr[2] = self.ten_day_moving_average_high

        # low from yesterday
        if low_val_arr[0] < 0.97:
            low_val_arr[0] = self.ten_day_moving_average_low

        # low from two days ago
        if low_val_arr[1] < 0.97:
            low_val_arr[1] = self.ten_day_moving_average_low

        # low from three days ago
        if low_val_arr[2] < 0.97:
            low_val_arr[2] = self.ten_day_moving_average_low

        # Use data from 3 days ago, 2 days ago, 1 day ago
        self.moving_average_high = sum(high_val_arr[:3]) / 3
        self.moving_average_low = sum(low_val_arr[:3]) / 3
        self.moving_average_open = sum(open_val[:3]) / 3

        # Calculate the buying point
        buy_point = self.moving_average_low * self.buy_coefficient
        selling_point = self.moving_average_high * self.sell_coefficient

        #TODO Get the gas fees in here somewhere do to something

        # clamp buy point
        if buy_point <= self.discard_buy_point or buy_point > self.max_buy_point:
            buy_point = self.new_buy_point

        # clamp sell point
        if selling_point > self.discard_sell_point:
            selling_point = self.new_sell_point

        self.buy_point = buy_point
        self.sell_point = selling_point

        # Change the buy_point and sell_point if they are set manually
        if self.manual_buy_point != 0:
            self.buy_point = self.manual_buy_point
        if self.manual_sell_point != 0:
            self.sell_point = self.manual_sell_point

        # Safeguard for gas fees 
        self.gas_fees_fast = scraper.get_gas_fees('Curve')
        if self.gas_fees_fast <= self.max_gas_fees * (self.wallet.balance['LUSD'] + self.wallet.balance['USDT']):
            return
        
        # Buy condition
        if buy_point > self.moving_average_low and self.wallet.balance['USDT'] > self.wallet.balance['LUSD']:
            if self.current_traded_coin_price <= buy_point:
                # Buy LUSD with USDT
                self.swap('buy', self.current_traded_coin_price)

        # Sell condition
        if selling_point < self.moving_average_high and self.wallet.balance['LUSD'] > self.wallet.balance['USDT']:
            if self.current_traded_coin_price >= selling_point:
                # Sell LUSD for USDT
                self.swap('sell', self.current_traded_coin_price)

    def serialize(self):
        data = {
            'trader_info': {
                'discard_buy_point': self.discard_buy_point,
                'discard_sell_point': self.discard_sell_point,
                'new_buy_point': self.new_buy_point,
                'new_sell_point': self.new_sell_point,
                'max_buy_point': self.max_buy_point,
                'buy_coefficient': self.buy_coefficient,
                'sell_coefficient': self.sell_coefficient,
                'manual_buy_point': self.manual_buy_point,
                'manual_sell_point': self.manual_sell_point,
                'max_gas_fees': self.max_gas_fees,
                'current_traded_coint_price': self.current_traded_coin_price,
                'moving_average_high': self.moving_average_high,
                'moving_average_low': self.moving_average_low,
                'ten_day_moving_average_high': self.ten_day_moving_average_high,
                'ten_day_moving_average_low': self.ten_day_moving_average_low,
                'high_coefficient': self.high_coefficient,
                'low_coefficient': self.low_coefficient,
                'buy_point': self.buy_point,
                'sell_point': self.sell_point
            }
        }

        return json.dumps(data, indent=4)

    def set_info(self, data):
        self.discard_buy_point = float(data['discard_buy_point'])
        self.discard_sell_point = float(data['discard_sell_point'])
        self.new_buy_point = float(data['new_buy_point'])
        self.new_sell_point = float(data['new_sell_point'])
        self.max_buy_point = float(data['max_buy_point'])
        self.buy_coefficient = float(data['buy_coefficient'])
        self.sell_coefficient = data['sell_coefficient']
        self.manual_buy_point = data['manual_buy_point']
        self.manual_sell_point = data['manual_sell_point']
        self.max_gas_fees = data['max_gas_fees']

        # Save the new settings to the config file
        self.save_settings_to_file()

    def email_trade(self):
        date_time_now = str(datetime.now())
        date_now = date_time_now.split(' ')[0]
        time_now = date_time_now.split(' ')[1].split('.')[0]
        content = f'{date_now},{time_now},usdt: {self.wallet.balance["USDT"]}, lusd: {self.wallet.balance["LUSD"]}, gas fees fast: {self.gas}'

        self.emailer.send('Bot trade found!', content)
    
    def log_trade(self):
        date_time_now = str(datetime.now())
        date_now = date_time_now.split(' ')[0]
        time_now = date_time_now.split(' ')[1].split('.')[0]
        
        with open('../logs/trade_log.csv', 'a') as f:
            line = f'{date_now},{time_now},{self.wallet.balance["USDT"]},{self.wallet.balance["LUSD"]},gas_fee,total_transaction_fee'
            pass

    def save_settings_to_file(self):
        settings = self.serialize()

        with open('trader_config.txt', 'w') as f:
            f.write(settings)

    def start(self):
        if self.running:
            Log.warn('Bot is already running')
            return

        self.running = True
        self.run_thread.start()
    
    def run(self):
        if not self.running:
            Log.error(f'Bot run method not started on new thread')
            return

        self.current_traded_coin_price = float(scraper.get_curent_lusd())

        Log.info(f'Trader started')
        while self.running:
            # Get the dates from which to get the data
            data = self.get_crypto_data(self.get_dates(start_date=0, dt=10))

            if data != None:
                if not data.empty:
                    # Process the data 
                    self.trade_model(data.get('Open'), data.get('High'), data.get('Low'))
                else:
                    Log.debug('error getting data')
            else:
                Log.debug('error getting data')

            time.sleep(60)

    def stop(self):
        self.run_thread.join()
        self.running = False
        Log.debug(f'Bot gracefully closed')


def get_traded_coin_price():
    pass

def get_eth_price():
    pass