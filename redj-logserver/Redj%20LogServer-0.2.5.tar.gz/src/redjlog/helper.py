import string
import random
from .management.server import reqApi


def cPrint(massage, color="warning"):
    print(printColor(color) + massage + printColor(color))


def printColor(color):
    colors = {
        "warning": '\033[93m',
        "error": '\033[91m',
        "HEADER": '\033[95m',
        "OKBLUE": '\033[94m',
        "OKCYAN": '\033[96m',
        "OKGREEN": '\033[92m',
        "WARNING": '\033[93m',
        "FAIL": '\033[91m',
        "ENDC": '\033[0m',
        "BOLD": '\033[1m',
        "UNDERLINE": '\033[4m'
    }

    return colors[color]


def sendToServer(data, type, config=None):
    return reqApi(data, type, config)


def randomString(size=40):
    text = string.digits
    text += string.punctuation
    text += string.ascii_letters
    text += string.ascii_lowercase
    text += string.ascii_uppercase

    return ''.join(random.choice(text) for i in range(size))
