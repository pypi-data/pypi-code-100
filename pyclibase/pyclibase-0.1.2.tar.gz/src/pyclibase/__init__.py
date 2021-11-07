import logging
import warnings
from rich.logging import RichHandler
from rich import traceback
from rich import print
from pyfiglet import Figlet

log = None
def print_title(title, logger_name):
    global log
    title = pyfiglet.figlet_format('DCCE CLI', font='slant')
    print(f'[blue]{title}[/blue]')
    FORMAT = "%(message)s"
    logging.basicConfig(format=FORMAT, datefmt="[%X]", level="NOTSET", handlers=[RichHandler(rich_tracebacks=True, markup=True)])
    traceback.install()
    log = logging.getLogger("rich")
