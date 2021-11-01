import logging
import json
import requests

from alira.instance import Instance


class SocketIO(object):
    def __init__(self, socketio_url, **kwargs):
        self.socketio_url = socketio_url

    def run(self, instance: Instance, pipeline_id: str = None, **kwargs):
        payload = {
            "message": "pipeline-new-instance",
            "data": instance.__dict__,
            "pipeline_id": pipeline_id,
        }

        self.emit(self.event, payload, pipeline_id)

        return None

    def emit(self, event: str, payload=None, namespace=None):
        if not self.socketio_url:
            return

        logging.info(
            f"Sending socket io notification to server {self.socketio_url}. Namespace {namespace}"
        )

        payload["event"] = event

        if namespace:
            payload["namespace"] = namespace

        try:
            requests.post(
                url=self.socketio_url,
                data=json.dumps(payload),
                headers={"Content-type": "application/json"},
            )
        except Exception:
            logging.exception("There was an error sending the socket io notification")
