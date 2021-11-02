from .hmac_signature import hash_function
from .secret_key_generator import get_secret_key
import logging


logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


secret_key = get_secret_key()


def check_signature(client_signature, data_message):
    # get the raw data and HMAC signature from client side..
    server_hmac_signature = hash_function(secret_key, data_message)
    logger.info(data_message)
    logger.info(server_hmac_signature)
    if(server_hmac_signature == client_signature):
        return True
    else:
        return False
