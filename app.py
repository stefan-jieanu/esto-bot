import requests
import json

data = requests.get('https://api.ethplorer.io/getTokenInfo/0x5f98805a4e8be255a32880fdec7f6728c6568ba0?apiKey=EK-2EtBp-P4bJq3y-ummYA')
data = data.content.decode('utf8').replace("'", '"')

json.dumps(data)
print(json.loads(data)['price']['rate'])
