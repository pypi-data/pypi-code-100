from unittest import TestCase

from ntropy_sdk import SDK, Transaction


class TxTest(TestCase):
    def test_enrich(self):
        api_key = "R6yiREz91PfXPjIfsjHqpVE4VGgjATXVjGrxuv3H"
        sdk = SDK(api_key)
        sdk.base_url = "http://staging.ntropy.network"

        tx = Transaction(
            amount=24.56,
            description="TARGET T- 5800 20th St 11/30/19 17:32",
            entry_type="debit",
            date="2012-12-10",
            account_holder_id="1",
            account_holder_type="business",
            iso_currency_code="USD",
        )

        resp = sdk.enrich(tx)

        print("HELLO")
        print(resp)

        resp = sdk.enrich(tx, latency_optimized=True)
        print(resp)

        txs = [tx, tx, tx]

        resp = sdk.enrich_batch(txs, labeling=False)

        print(resp)

        result = resp.wait()

        print(result.transactions)

    def test_enrich_business(self):
        api_key = "R6yiREz91PfXPjIfsjHqpVE4VGgjATXVjGrxuv3H"
        sdk = SDK(api_key)
        sdk.base_url = "http://staging.ntropy.network"

        tx = Transaction(
            amount=24.56,
            description="AMAZON WEB SERVICES AWS.AMAZON.CO WA Ref5543286P25S Crd15",
            entry_type="debit",
            date="2012-12-10",
            account_holder_id="1",
            account_holder_type="business",
            iso_currency_code="USD",
        )

        resp = sdk.enrich(tx)

        print("HELLO")
        print(resp)

        resp = sdk.enrich(tx, latency_optimized=True)
        print(resp)

        txs = [tx, tx, tx]

        resp = sdk.enrich_batch(txs, labeling=False)

        print(resp)

        result = resp.wait()

        print(result.transactions)
