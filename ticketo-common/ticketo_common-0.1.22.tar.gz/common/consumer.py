import json
from signal import SIGINT, SIGTERM, signal

import boto3
from django.conf import settings


class SignalHandler:
    def __init__(self):
        self.received_signal = False
        signal(SIGINT, self._signal_handler)
        signal(SIGTERM, self._signal_handler)

    def _signal_handler(self, signal, frame):
        print(f"handling signal {signal}, exiting gracefully")
        self.received_signal = True


def sqs_consume(exchanges):
    sqs_client_options = {
        "region_name": settings.AWS_REGION_NAME,
        "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
        "endpoint_url": settings.AWS_SQS_ENDPOINT_URL,
    }
    sqs = boto3.resource("sqs", **sqs_client_options)
    queue = sqs.get_queue_by_name(QueueName=settings.SERVICE_QUEUE)
    signal_handler = SignalHandler()
    wait_time_seconds = settings.AWS_SQS_CONSUMER_WAIT_TIME_SECONDS or 60
    while not signal_handler.received_signal:
        for message in queue.receive_messages(
            MaxNumberOfMessages=100, WaitTimeSeconds=wait_time_seconds
        ):
            body = json.loads(message.body)
            exchange_fn = exchanges[body.get("Subject")]
            exchange_fn(body.get("Message"))
            message.delete()
