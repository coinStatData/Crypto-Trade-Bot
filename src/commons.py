import math
from typing import List, Union, Tuple
from cbpro import AuthenticatedClient


class InsufficientFundsException(Exception):
    pass


def get_balance(client: AuthenticatedClient, target_currency: str = 'BTC') -> Tuple[Union[str, None], float]:
    accounts: List[dict] = client.get_accounts()

    acc_id: Union[str, None] = None
    balance: float = math.nan
    for acc in accounts:
        currency = acc.get('currency')
        if currency == target_currency:
            acc_id = acc.get('id')

    if acc_id is None:
        return acc_id, balance

    acc_history: List[dict] = client.get_account_history(acc_id)
    for hist in acc_history:
        balance = hist.get('balance', math.nan)
        balance = round(
            number=float(balance) - .000001,
            ndigits=7,
        )
        break
    return acc_id, balance
