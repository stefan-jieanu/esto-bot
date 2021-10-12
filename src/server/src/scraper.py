from bs4 import BeautifulSoup
import requests

# def get_curent_lusd():
#     html = requests.get('https://etherscan.io/token/0x5f98805A4E8be255a32880FDeC7F6728C6568bA0').content

#     soup = BeautifulSoup(html, 'html.parser')
#     lusd_price = soup.find_all('h2')
    
#     return lusd_price

import requests
import json

def get_curent_lusd():

    data = requests.get('https://api.ethplorer.io/getTokenInfo/0x5f98805a4e8be255a32880fdec7f6728c6568ba0?apiKey=EK-2EtBp-P4bJq3y-ummYA')
    data = data.content.decode('utf8').replace("'", '"')

    return json.loads(data)['price']['rate']


def get_current_usd():
    html = requests.get('https://coinmarketcap.com/currencies/ethereum/').content

    soup = BeautifulSoup(html, 'html.parser')
    usd_price = soup.find_all('div', {'class': 'priceValue'})[0].string

    return float(usd_price.replace('$', '').replace(',', ''))

def get_gas_fees(exchange):
    html = requests.get('https://crypto.com/defi/dashboard/gas-fees').content

    soup = BeautifulSoup(html, 'html.parser')
    row = soup.find_all('tr', {'class': 'DefiTableRow__TableRow-aqcgpn-2 keNjLW'})

    fees = 0
    for r in row:
        if exchange == r.find_all_next('td')[2].string:
            fees = r.find_all_next('td')[6].string[1:]
            break

    return float(fees)
