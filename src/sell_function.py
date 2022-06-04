import json

from aws_lambda_powertools.logging import Logger
from cbpro import AuthenticatedClient

from src.commons import init_cbpro_client, get_balance, InsufficientFundsException

client: AuthenticatedClient = init_cbpro_client()
logger = Logger()


def lambda_handler(event, context):
    logger.info({
        'event': event,
        'context': context,
    })

    account_id, balance = get_balance(
        client=client,
        target_currency='BTC'
    )

    logger.info({
        'account_id': account_id,
        'balance': balance,
    })

    if balance > 0.000001:
        order_details = client.place_market_order(
            product_id='BTC-USD',
            side='sell',
            size=balance
        )

        result = {
            'order_details': order_details,
        }

        logger.info(result)
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }

    raise InsufficientFundsException(f'{account_id=}; {balance=}')
