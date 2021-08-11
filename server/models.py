# The standard one (the first one we ran)
def model_v1(open_val, low_val, high_val, current):
    # self.current_lusd_price = float(coinmarketscraper.get_curent_lusd())

    # # Use data from 3 days ago, 2 days ago, 1 day ago
    # moving_average_high = sum(high_val) / 3
    # moving_average_low = sum(low_val) / 3
    # moving_average_open = sum(open_val) / 3

    # # Use data from 3 days ago, 2 days ago, 1 day ago
    # moving_average_low_to_one = ((low_val[2] - 1) + (low_val[1] - 1) + (low_val[0] - 1)) / 3
    # moving_average_one_to_high = ((high_val[2] - 1) + (high_val[1] - 1) + (high_val[0] - 1)) / 3

    # # Calculate the buying point
    # buy_point = moving_average_open + (moving_average_low_to_one * self.high_coefficient)
    # selling_point = moving_average_open + (moving_average_one_to_high * self.low_coefficient)

    # self.buy_point = buy_point
    # self.sell_point = selling_point

    # # Buy condition
    # # if 1.2 > 0.99 and self.wallet.balance['USDT'] > self.wallet.balance['LUSD']:
    # if buy_point > moving_average_low and self.wallet.balance['USDT'] > self.wallet.balance['LUSD']:
    #     # if current_lusd_price <= 1.2:
    #     if self.current_lusd_price <= buy_point:
    #         # Buy LUSD with USDT
    #         self.swap('buy', self.current_lusd_price)

    # # Sell condition
    # if selling_point < moving_average_high and self.wallet.balance['LUSD'] > self.wallet.balance['USDT']:
    #     if self.current_lusd_price >= selling_point:
    #         # Sell LUSD for USDT
    #         self.swap('sell', self.current_lusd_price)
    pass

def model_v2(open_val, low_val, high_val, current):
    pass