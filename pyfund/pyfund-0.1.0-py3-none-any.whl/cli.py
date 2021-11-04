"""Console script for pyfund."""
import sys

import click

from pyfund import __version__
from pyfund.cmds.backtest import backtest
from pyfund.cmds.corrcoef import corrcoef
from pyfund.cmds.etf import etf
from pyfund.cmds.fund_bond import fund_bond
from pyfund.cmds.fund_index import fund_index
from pyfund.cmds.fund_mix import fund_mix
from pyfund.cmds.init import init
from pyfund.cmds.init_fund import init_fund
from pyfund.cmds.status import status
from pyfund.cmds.stock import stock
from pyfund.cmds.stocks import stocks
from pyfund.cmds.test import test


@click.group()
@click.version_option(__version__)
@click.pass_context
def main(args=None):
    """Console script for pyfund."""
    return 0

main.add_command(status)
main.add_command(stock)
main.add_command(stocks)
main.add_command(corrcoef)
main.add_command(etf)
main.add_command(test)
main.add_command(backtest)

main.add_command(init)
main.add_command(init_fund)
main.add_command(fund_index)
main.add_command(fund_mix)
main.add_command(fund_bond)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
