import tkinter as tk
from tkinter import ttk
import plyer.platforms.win.notification
import json

from config import Protocol
from tkinter import Canvas, Text
from tkinter.constants import END, LEFT, RADIOBUTTON, RIGHT
from plyer import notification


from client_connection import ClientConnection


class Colors:
    primary = '#00bcd4'
    dark = '#008ba3'
    light = '#62efff'
    text = '#000000'

class Client:
    def init():
        # Initializing Tk window
        Client.root = tk.Tk()
        Client.root.protocol('WM_DELETE_WINDOW', Client.close)

        # Initializing the UI for the trader bot info
        Client.trader_info = ttk.LabelFrame(Client.root, text='Trader info')
        Client.trader_info.grid(column=0, row=0, padx=20, pady=20, sticky='n')

        Client.trader_info_buy_point_label = tk.Label(Client.trader_info, text="Buy point: ")
        Client.trader_info_buy_point_label.grid(row=0, column=0, sticky='w')
        Client.trader_info_buy_point = tk.Label(Client.trader_info)
        Client.trader_info_buy_point.grid(row=0, column=1, sticky='w',
            pady=5)

        Client.trader_info_sell_point_label = tk.Label(Client.trader_info, text="Sell point: ")
        Client.trader_info_sell_point_label.grid(row=1, column=0, sticky='w')
        Client.trader_info_sell_point = tk.Label(Client.trader_info)
        Client.trader_info_sell_point.grid(row=1, column=1, sticky='w',
            pady=5)

        Client.trader_info_lusd_price_label = tk.Label(Client.trader_info, text="Current LUSD price: ")
        Client.trader_info_lusd_price_label.grid(row=2, column=0, sticky='w')
        Client.trader_info_lusd_price = tk.Label(Client.trader_info)
        Client.trader_info_lusd_price.grid(row=2, column=1, sticky='w',
            pady=5)

        Client.trader_info_mah_label = tk.Label(Client.trader_info, text="Moving average high: ")
        Client.trader_info_mah_label.grid(row=3, column=0, sticky='w')
        Client.trader_info_mah = tk.Label(Client.trader_info)
        Client.trader_info_mah.grid(row=3, column=1, sticky='w',
            pady=5)

        Client.trader_info_mal_label = tk.Label(Client.trader_info, text="Moving average low: ")
        Client.trader_info_mal_label.grid(row=4, column=0, sticky='w')
        Client.trader_info_mal = tk.Label(Client.trader_info)
        Client.trader_info_mal.grid(row=4, column=1, sticky='w',
            pady=5)

        Client.trader_info_ten_mah_label = tk.Label(Client.trader_info, text="10d moving average high: ")
        Client.trader_info_ten_mah_label.grid(row=5, column=0, sticky='w')
        Client.trader_info_ten_mah = tk.Label(Client.trader_info)
        Client.trader_info_ten_mah.grid(row=5, column=1, sticky='w',
            pady=5)

        Client.trader_info_ten_mal_label = tk.Label(Client.trader_info, text="10d moving average low: ")
        Client.trader_info_ten_mal_label.grid(row=6, column=0, sticky='w')
        Client.trader_info_ten_mal = tk.Label(Client.trader_info)
        Client.trader_info_ten_mal.grid(row=6, column=1, sticky='w',
            pady=5)

        Client.trader_info_newbuy_label = tk.Label(Client.trader_info, text="New but point: ")
        Client.trader_info_newbuy_label.grid(row=7, column=0, sticky='w')
        Client.trader_info_newbuy = tk.Label(Client.trader_info)
        Client.trader_info_newbuy.grid(row=7, column=1, sticky='w',
            pady=5)

        Client.trader_info_newsell_label = tk.Label(Client.trader_info, text="New sell point: ")
        Client.trader_info_newsell_label.grid(row=8, column=0, sticky='w')
        Client.trader_info_newsell = tk.Label(Client.trader_info)
        Client.trader_info_newsell.grid(row=8, column=1, sticky='w',
            pady=5)

        Client.trader_info_discardbuy_label = tk.Label(Client.trader_info, text="Discard buy point: ")
        Client.trader_info_discardbuy_label.grid(row=9, column=0, sticky='w')
        Client.trader_info_discardbuy = tk.Label(Client.trader_info)
        Client.trader_info_discardbuy.grid(row=9, column=1, sticky='w',
            pady=5)

        Client.trader_info_discardsell_label = tk.Label(Client.trader_info, text="Discard sell point: ")
        Client.trader_info_discardsell_label.grid(row=10, column=0, sticky='w')
        Client.trader_info_discardsell = tk.Label(Client.trader_info)
        Client.trader_info_discardsell.grid(row=10, column=1, sticky='w',
            pady=5)

        Client.trader_info_percent_mah_label = tk.Label(Client.trader_info, text="Percent of moving avg high: ")
        Client.trader_info_percent_mah_label.grid(row=11, column=0, sticky='w')
        Client.trader_info_percent_mah = tk.Label(Client.trader_info)
        Client.trader_info_percent_mah.grid(row=11, column=1, sticky='w',
            pady=5)

        Client.trader_info_percent_mal_label = tk.Label(Client.trader_info, text="Percent of moving avg low: ")
        Client.trader_info_percent_mal_label.grid(row=12, column=0, sticky='w')
        Client.trader_info_percent_mal = tk.Label(Client.trader_info)
        Client.trader_info_percent_mal.grid(row=12, column=1, sticky='w',
            pady=5)

        Client.trader_info_max_buypoint_label = tk.Label(Client.trader_info, text="Max buy point: ")
        Client.trader_info_max_buypoint_label.grid(row=13, column=0, sticky='w')
        Client.trader_info_max_buypoint = tk.Label(Client.trader_info)
        Client.trader_info_max_buypoint.grid(row=13, column=1, sticky='w',
            pady=5)

        # Initializing the UI for the wallet info
        Client.wallet_info = ttk.LabelFrame(Client.root, text='Wallet info')
        Client.wallet_info.grid(column=1, row=0, padx=20, pady=20, sticky='n')

        Client.wallet_info_usdt_label = tk.Label(Client.wallet_info, text="USDT: ")
        Client.wallet_info_usdt_label.grid(row=0, column=0, sticky='w')
        Client.wallet_info_usdt = tk.Label(Client.wallet_info)
        Client.wallet_info_usdt.grid(row=0, column=1, sticky='w',
            pady=5)

        Client.wallet_info_lusd_label = tk.Label(Client.wallet_info, text="LUSD: ")
        Client.wallet_info_lusd_label.grid(row=1, column=0, sticky='w')
        Client.wallet_info_lusd = tk.Label(Client.wallet_info)
        Client.wallet_info_lusd.grid(row=1, column=1, sticky='w',
            pady=5)

        Client.wallet_info_eth_label = tk.Label(Client.wallet_info, text="ETH: ")
        Client.wallet_info_eth_label.grid(row=2, column=0, sticky='w')
        Client.wallet_info_eth = tk.Label(Client.wallet_info)
        Client.wallet_info_eth.grid(row=2, column=1, sticky='w',
            pady=5)

        Client.wallet_info_eth_usd_label = tk.Label(Client.wallet_info, text="ETH(dollar): ")
        Client.wallet_info_eth_usd_label.grid(row=3, column=0, sticky='w')
        Client.wallet_info_eth_usd = tk.Label(Client.wallet_info)
        Client.wallet_info_eth_usd.grid(row=3, column=1, sticky='w',
            pady=5)

        # sendMessage = tk.Button(Client.root, text='Send', padx=10,
        #                 pady=10,command=Client.sendData)
        # sendMessage.grid(row=3, column=1)

        # Client.msg = tk.Entry(Client.root)
        # Client.msg.grid(row=3, column=0)

        # Initializing connection to the server
        ClientConnection.init()
        ClientConnection.set_client_data_callback(Client.on_data_from_server)

        ClientConnection.send(Protocol.QUERY_INFO)

    def on_data_from_server(data):
        if data == Protocol.PING:
            notification.notify("with love", data)
            return

        if data.find('query_info'):
            query_info = json.loads(data)['query_info']
            Client.set_ui_info(query_info)
            return

    def set_ui_info(data):
        Client.trader_info_buy_point.config(text=data['trader_info']['buy_point'])
        Client.trader_info_sell_point.config(text=data['trader_info']['sell_point'])
        Client.trader_info_lusd_price.config(text=data['trader_info']['lusd_price'])
        Client.trader_info_mah.config(text=data['trader_info']['moving_average_high'])
        Client.trader_info_mal.config(text=data['trader_info']['moving_average_low'])
        Client.trader_info_ten_mah.config(text=data['trader_info']['ten_day_moving_average_high'])
        Client.trader_info_ten_mal.config(text=data['trader_info']['ten_day_moving_average_low'])
        Client.trader_info_newbuy.config(text=data['trader_info']['new_buy_point'])
        Client.trader_info_newsell.config(text=data['trader_info']['new_sell_point'])
        Client.trader_info_discardbuy.config(text=data['trader_info']['discard_buy_point'])
        Client.trader_info_discardsell.config(text=data['trader_info']['discard_sell_point'])
        Client.trader_info_percent_mah.config(text=data['trader_info']['percentage_of_moving_average_high'])
        Client.trader_info_percent_mal.config(text=data['trader_info']['percentage_of_moving_average_low'])
        Client.trader_info_max_buypoint.config(text=data['trader_info']['max_buy_point'])
        

        Client.wallet_info_usdt.config(text=data['wallet_info']['USDT'])
        Client.wallet_info_lusd.config(text=data['wallet_info']['LUSD'])
        Client.wallet_info_eth.config(text=data['wallet_info']['ETH'])
        Client.wallet_info_eth_usd.config(text=str(data['wallet_info']['ETH_IN_USD'])[:6])

    def run():
        Client.root.mainloop()

    def sendData():
        data = Client.msg.get()

        ClientConnection.send('!PING_CLIENTS')

    def close():
        ClientConnection.disconnect()
        Client.root.destroy()

