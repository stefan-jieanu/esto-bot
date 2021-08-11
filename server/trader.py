from ast import Index
import builtins
import sys
import time
import json
from scipy import stats

import coinmarketscraper

from datetime import datetime, timedelta
from cryptocmd import CmcScraper

class Trader:
    def __init__(self, wallet):
        self.running = False
        self.wallet = wallet

        self.high_coefficient = 1.2
        self.low_coefficient = 0.4
        self.buy_point = 0
        self.sell_point = 0
        self.current_lusd_price = 0
        self.moving_average_high = 0
        self.moving_average_low = 0
        self.new_buy_point =  0.9988
        self.new_sell_point = 1.02
        self.discard_buy_point = 0.98
        self.discard_sell_point = 1.03
        self.percentage_of_moving_average_high = 0.996
        self.percentage_of_moving_average_low = 1.004
        self.max_buy_point = 1
        self.ten_day_moving_average_high = 0
        self.ten_day_moving_average_low = 0
        pass

    def get_crypto_data(self, dates):
        # initialise scraper 
        scraper = CmcScraper('lusd', dates[1], dates[0])

        # Pandas dataFrame for the same data
        print(scraper.get_dataframe())
        return scraper.get_dataframe()

    def get_dates(self, days_ago, dt):
        dates = []
        d1 = datetime.now() - timedelta(days=days_ago)
        d2 = datetime.now() - timedelta(days=(days_ago + dt))

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

        print(f'Traded! LUSD price: {price}; \nCurrent USDT balance: {self.wallet.balance["USDT"]}; \n Current LUSD balance: {self.wallet.balance["LUSD"]}')
        

    def calculate_moving_average(self, open_val, high_val, low_val):
        self.current_lusd_price = float(coinmarketscraper.get_curent_lusd())

        # This will be without outliers
        # TODO: We need to get this data from 10 days in the past, so do that later
        self.ten_day_moving_average_high = stats.trim_mean(high_val, 0.1)
        self.ten_day_moving_average_low = stats.trim_mean(low_val, 0.1)

        # high from yesterday
        if high_val[0] > 1.04:
            high_val[0] = self.ten_day_moving_average_high

        # high from two days ago
        if high_val[1] > 1.04:
            high_val[1] = self.ten_day_moving_average_high

        # high from three days ago
        if high_val[2] > 1.04:
            high_val[2] = self.ten_day_moving_average_high

        # low from yesterday
        if low_val[0] < 0.97:
            low_val[0] = self.ten_day_moving_average_low

        # low from two days ago
        if low_val[1] < 0.97:
            low_val[1] = self.ten_day_moving_average_low

        # low from three days ago
        if low_val[2] < 0.97:
            low_val[2] = self.ten_day_moving_average_low

        # Use data from 3 days ago, 2 days ago, 1 day ago
        self.moving_average_high = sum(high_val) / 3
        self.moving_average_low = sum(low_val) / 3
        self.moving_average_open = sum(open_val) / 3

        # Calculate the buying point
        buy_point = self.moving_average_low * self.percentage_of_moving_average_low
        selling_point = self.moving_average_high * self.percentage_of_moving_average_high

        # clamp buy point
        if buy_point <= self.discard_buy_point or buy_point > self.max_buy_point:
            buy_point = self.new_buy_point

        # clamp sell point
        if selling_point > self.discard_sell_point:
            selling_point = self.new_sell_point

        self.buy_point = buy_point
        self.sell_point = selling_point

        # Buy condition
        if buy_point > self.moving_average_low and self.wallet.balance['USDT'] > self.wallet.balance['LUSD']:
            if self.current_lusd_price <= buy_point:
                # Buy LUSD with USDT
                self.swap('buy', self.current_lusd_price)

        # Sell condition
        if selling_point < self.moving_average_high and self.wallet.balance['LUSD'] > self.wallet.balance['USDT']:
            if self.current_lusd_price >= selling_point:
                # Sell LUSD for USDT
                self.swap('sell', self.current_lusd_price)

    def run(self):
        self.running = True
        print('Bot started...')
        self.current_lusd_price = float(coinmarketscraper.get_curent_lusd())

        while self.running:
            # Get the dates from which to get the data
            data = self.get_crypto_data(self.get_dates(days_ago=0, dt=3))

            # Process the data 
            self.calculate_moving_average(data.get('Open'), data.get('High'), data.get('Low'))

            time.sleep(60)

    def serialize(self):
        trader_info = {
            'high_coefficient': self.high_coefficient,
            'low_coefficient': self.low_coefficient,
            'buy_point': self.buy_point,
            'sell_point': self.sell_point,
            'lusd_price': self.current_lusd_price,
            'moving_average_high': self.moving_average_high,
            'moving_average_low': self.moving_average_low,
            'ten_day_moving_average_high': self.ten_day_moving_average_high,
            'ten_day_moving_average_low': self.ten_day_moving_average_low,
            'new_buy_point': self.new_buy_point,
            'new_sell_point': self.new_sell_point,
            'discard_buy_point': self.discard_buy_point,
            'discard_sell_point': self.discard_sell_point,
            'percentage_of_moving_average_high': self.percentage_of_moving_average_high,
            'percentage_of_moving_average_low': self.percentage_of_moving_average_low,
            'max_buy_point': self.max_buy_point
        }

        return trader_info

    # Setters
    def set_high_coefficient(self, value):
        self.high_coefficient = value
    
    def set_low_coefficient(self, value):
        self.low_coefficient = value
