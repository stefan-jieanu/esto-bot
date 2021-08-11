import sys
# import client
from datetime import datetime, timedelta
from cryptocmd import CmcScraper

fake_wallet_balance_LUSD = 0
fake_wallet_balance_USDT = 1000
fake_current_price = 1

def calculate_moving_average(open_cost, high, low):
    # This is temporary
    global fake_wallet_balance_LUSD
    global fake_wallet_balance_USDT
    ###################

    average = 0

    # print("Open: " + str(open_cost[0]) + ", " + str(open_cost[1]) + ", " + str(open_cost[2]))
    # print("High:" + str(high[0]) + ", " + str(high[1]) + ", " + str(high[2]))
    # print("Low:" + str(low[0]) + ", " + str(low[1]) + ", " + str(low[2]))

    # Use data from 3 days ago, 2 days ago, 1 day ago
    moving_average_high = sum(high[:1]) / 3
    moving_average_low = sum(low[:1]) / 3
    moving_average_open = sum(open_cost[:1]) / 3

    # Use data from 3 days ago, 2 days ago, 1 day ago
    moving_average_low_to_one = ((low[3] - 1) + (low[2] - 1) + (low[1] - 1)) / 3
    moving_average_one_to_high = ((high[3] - 1) + (high[2] - 1) + (high[1] - 1)) / 3

    # Calculate the buying point
    buy_point = moving_average_open + (moving_average_low_to_one * 1.2)
    selling_point = moving_average_open + (moving_average_one_to_high * 0.4)

    # Buy condition
    if buy_point > moving_average_low and fake_wallet_balance_USDT > fake_wallet_balance_LUSD:
        # if current
        swap('buy')

    # Sell condition
    if buy_point > moving_average_low and selling_point < moving_average_high:
        if (fake_wallet_balance_LUSD > fake_wallet_balance_USDT):
            swap('sell')

    return average

def swap(opts):
    # This is temporary
    global fake_wallet_balance_LUSD
    global fake_wallet_balance_USDT
    ###################

    if opts == 'buy':
        # TODO: Get this data from the cms scrapper I think
        exchange_rate = 0.99
        fake_wallet_balance_LUSD = fake_wallet_balance_USDT * exchange_rate
    elif opts == 'sell':
        # TODO: Get this data from the cms scrapper I think
        exchange_rate = 0.99
        fake_wallet_balance_USDT = fake_wallet_balance_LUSD * exchange_rate

def get_crypto_data(dates):
    coin_name = input("Enter coint symbol(eg. BTC, XRP): ")
    coin_name = coin_name.upper()

    # initialise scraper 
    scraper = CmcScraper(coin_name)

    # export the data as csv file, you can also pass optional name parameter
    # scraper.export_csv(coin_name + '_all_time.csv')

    # Pandas dataFrame for the same data
    return scraper.get_dataframe()


# days_ago - how many days to go in the past to get data
# dt - the time period for which to get the data
def get_dates(days_ago, dt):
    dates = []
    d1 = datetime.now() - timedelta(days=days_ago)
    d2 = datetime.now() - timedelta(days=(days_ago + dt))

    dates.append(d1.strftime("%d-%m-%Y"))
    dates.append(d2.strftime("%d-%m-%Y"))
    return dates

def main(argv, argc):
    data = get_crypto_data(get_dates(days_ago=0, dt=3))
    print(data[:10])
    # average = calculate_moving_average(data.get("Open"), data.get("High"), data.get("Low"))

    #print(average)

if __name__ == "__main__":
    # client.send_notification("Hello notification")

    main(sys.argv, len(sys.argv))
