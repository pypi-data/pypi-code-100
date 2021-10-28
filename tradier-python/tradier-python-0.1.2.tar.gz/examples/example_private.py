import os
from datetime import date

from tradier_python import TradierAPI

if __name__ == "__main__":
    token = os.environ["TRADIER_TOKEN"]
    account_id = os.environ["TRADIER_ACCOUNT_ID"]
    t = TradierAPI(token=token, default_account_id=account_id)

    h = t.get_historical_quotes("SPY")
    print(h)