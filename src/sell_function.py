import os
import json
import math
from typing import Final, Union, List

import cbpro
from aws_lambda_powertools.logging import Logger

logging = Logger()

API_SECRET: Final[str] = os.environ['API_SECRET']
API_KEY: Final[str] = os.environ['API_KEY']
API_PASS: Final[str] = os.environ['API_PASS']
URL: Final[str] = os.environ['URL']

client = cbpro.AuthenticatedClient(
    key=API_KEY,
    b64secret=API_SECRET,
    passphrase=API_PASS,
    api_url=URL
)


def lambda_handler(event, context):
    logging.info({
        'event': event,
        'context': context,
    })

    balance = get_balance()
    order_details = None

    if balance > 0.000001:
        order_details = client.place_market_order(
            product_id='BTC-USD',
            side='sell',
            size=balance
        )
        print(f'{order_details=}')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'order_details': order_details,
        })
    }


def get_balance(target_currency: str = 'BTC') -> float:
    accounts: List[dict] = client.get_accounts()

    acc_id: Union[str, None] = None
    balance: float = math.nan
    for acc in accounts:
        currency = acc.get('currency')
        if currency == target_currency:
            acc_id = acc.get('id')

    if acc_id is None:
        return math.nan

    acc_history: List[dict] = client.get_account_history(acc_id)
    for hist in acc_history:
        balance = hist.get('balance', math.nan)
        balance = round(
            number=float(balance) - .000001,
            ndigits=7,
        )
        break
    return balance
