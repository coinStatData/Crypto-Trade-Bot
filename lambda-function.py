import cbpro
import os
import json

print('Loading function')

api_secret = os.environ['API_SECRET']
api_key = os.environ['API_KEY']
api_pass = os.environ['API_PASS']
url= os.environ['URL']

client = cbpro.AuthenticatedClient(
    api_key,
    api_secret,
    api_pass,
    api_url=url
)

def lambda_handler(event, context):
    balance = getBalance()
    if(balance > .000001):
        b = client.place_market_order(product_id='BTC-USD', side='sell', size=balance)
        print(b);

def getBalance():
    accounts = client.get_accounts();
    for acc in accounts:
        currency = acc.get('currency')
        if currency=='BTC':
            acc_id = acc.get('id')
    acc_history = client.get_account_history(acc_id)
    for hist in acc_history:
        balance = json.dumps(hist,indent=1)
        break;
    print('Balance is -> ', balance)
    balance = json.loads(balance)
    balance = round(float(balance['balance']), 7) - .000001
    return balance

