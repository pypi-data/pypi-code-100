from contextlib import contextmanager

from dofast.oss import Bucket
from dofast.pyavatar import PyAvataaar
from dofast.toolkits.qredis import QRedis
from dofast.toolkits.textparser import TextParser
from dofast.utils import DeeplAPI
from dofast.weather import Weather


class AppInterfaces(object):
    def __init__(self):
        self.weather = Weather()
        self.textparser = TextParser
        self.deepl = DeeplAPI()
        self.avatar = PyAvataaar()
        self.redis = QRedis()
        self.bucket = Bucket()

from contextlib import contextmanager
@contextmanager
def yield_api():
    yield AppInterfaces()

api = yield_api()


