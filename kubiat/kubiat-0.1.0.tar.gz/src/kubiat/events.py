import requests
import os
from cloudevents.http import CloudEvent, to_structured
from kubiat.service import APP

app_space = ''
if 'KUBIAT' in os.environ:
    app_space = os.environ['KUBIAT']
else:
    APP.logger.error('No App Space defined')


def callService(myfn, data):
    dest = "https://"+myfn+"."+app_space+".kubiat.eu/"
    attributes = {"type": "direct-call", "source": "empty"}
    return sendEvent(dest, data, attributes)


def callBroker(data, attributes):
    broker = ("http://broker-ingress.knative-eventing.svc.cluster.local/"
              + app_space
              + "/default")
    return sendEvent(broker, data, attributes)


def sendEvent(dest, data, attributes):
    event = CloudEvent(attributes, data)
    headers, body = to_structured(event)
    r = requests.post(url=dest, data=body, headers=headers)
    if (r is not None and r.ok and r.status_code == 200):
        return r.json()
    if (r.status_code != 202):
        APP.logger.error('unexpected response ' + str(r.status_code) + r.text)
    return {}
