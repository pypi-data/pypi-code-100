import hmac
import hashlib
import logging


logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def hash_function(secret_key, message):
    digest = hmac.new(secret_key, message, hashlib.sha256).digest()
    return digest.hex()
