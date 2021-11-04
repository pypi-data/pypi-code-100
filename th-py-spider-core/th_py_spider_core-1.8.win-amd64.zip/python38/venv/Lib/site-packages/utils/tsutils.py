import logging
from cmq.account import Account
from cmq.queue import Message

def getQueue(queue_name,secretId,secretKey):
    my_account = Account("https://cmq-queue-gz.api.qcloud.com",
                         secretId, secretKey, debug=True)
    my_account.set_log_level(logging.DEBUG)
    my_queue = my_account.get_queue(queue_name)
    return my_queue

def send_message(queue_name,messagebody, secretId, secretKey):
    my_account = Account("https://cmq-queue-gz.api.qcloud.com",
                         secretId, secretKey, debug=True)
    my_account.set_log_level(logging.DEBUG)
    msg_body = messagebody
    msg = Message(msg_body)
    my_queue = my_account.get_queue(queue_name)
    my_queue.send_message(msg)