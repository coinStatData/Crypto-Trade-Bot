import os
import json
from typing import Final

from cbpro import AuthenticatedClient
from aws_lambda_powertools.logging import Logger

from commons import get_balance, InsufficientFundsException

logging = Logger()

API_SECRET: Final[str] = os.environ['API_SECRET']
API_KEY: Final[str] = os.environ['API_KEY']
API_PASS: Final[str] = os.environ['API_PASS']
URL: Final[str] = os.environ['URL']

client = AuthenticatedClient(
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

    account_id, balance = get_balance(
        client=client,
        target_currency='BTC'
    )

    logging.info({
        'account_id': account_id,
        'balance': balance,
    })

    if balance > 5:
        order_details = client.place_market_order(
            product_id='BTC-USD',
            side='buy',
            funds=balance
        )
        result = {
            'order_details': order_details,
        }

        logging.info(result)
        return {
            'statusCode': 200,
            'body': json.dumps(result, default=str)
        }

    raise InsufficientFundsException(f'{account_id=}; {balance=}')
