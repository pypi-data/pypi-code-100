import ssl, json, time, sys, queue, atexit, logging, threading
import paho.mqtt.client as paho


LOG = logging.getLogger(__name__)

class MQTTJSONMessage:
  def __init__ (self, topic, payload):
    self.topic = topic
    self.ts = time.time() * 1000.0
    self.payload = json.loads(payload)

class MQTTSubscriber:
  def __init__ (self, mqtt, topic):
    self.mqtt = mqtt
    self.topic = topic
    self.queue = queue.Queue()

  def add_message (self, message):
    self.queue.put(message)
  
  def subscribe (self):
    sys.stdout.write('subscribe to: ' + self.topic + '\n')
    self.mqtt.subscribe([(self.topic + '/#', 1,)])

  def is_subscribed (self, topic):
    return topic.startswith(self.topic)
  
  def __iter__ (self):
    while not self.queue.empty():
      msg = self.queue.get()
      yield MQTTJSONMessage(msg.topic, msg.payload)

  def consume (self, sleep=0.01):
    while 1:
      for msg in self:
        yield msg
      time.sleep(sleep)


class MQTTMessage:
  def __init__ (self, topic, payload):
    self.topic = topic
    self.payload = payload
    self.publish_info = None
  
  def publish (self, client):
    self.publish_info = client.publish(self.topic, self.payload)



class MQTT:
  def __init__ (self, host, port, client_id, use_ssl=False, transport='tcp'):
    self.use_ssl = use_ssl
    self.client_id = client_id
    self.mqtt_host = host
    self.mqtt_port = port
    self.subscriptions = []
    self.is_connected = None
    self.transport = transport

    self.client = paho.Client(transport=self.transport, client_id=self.client_id)
    self.client.on_message = self.on_message
    self.client.on_connect = self.on_connect
    self.client.on_disconnect = self.on_disconnect
    self.client.max_inflight_messages_set(0)

    self.out_messages = queue.Queue()

    if self.use_ssl:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        self.client.tls_set_context(ssl_ctx)
        #self.client.tls_insecure_set(True)

    atexit.register(self.on_exit)

    self.thread = threading.Thread(target=self.main)
    self.thread.daemon = True
    self.thread.start()

  def _ensure_connection (self):
    while 1:
      try:
        result = self.client.connect(self.mqtt_host, self.mqtt_port)
        self.client.loop_start()
      except:
        LOG.warning('failed to connect to server')
        time.sleep(5)
      else:
        break

  def main (self):
    self._ensure_connection()
    while 1:
      time.sleep(0.02)
      if not self.is_connected or self.out_messages.empty():
        continue
      msg = self.out_messages.get()
      msg.publish(self.client)
            
  def subscribe (self, topic):
    sub = MQTTSubscriber(self.client, topic)
    self.subscriptions.append(sub)
    return sub

  def on_connect (self, *args, **kw):
    sys.stdout.write('connected: %s\n' % self.client_id)
    self.is_connected = True
    for sub in self.subscriptions:
      sub.subscribe()
    
  def on_disconnect (self, *args, **kw):
    sys.stdout.write('disconnected\n')
    self.is_connected = False
    
  def on_message (self, client, _, msg):
    sys.stdout.write('received: %s\n' % msg.topic)
    for sub in self.subscriptions:
      if not sub.is_subscribed(msg.topic):
        continue
      sub.add_message(msg)
    
  def publish (self, topic, msg):
    self.out_messages.put(
      MQTTMessage(topic, json.dumps(msg))
    )
  
  def on_exit (self):
    # TODO: save unsent messages to file until confirmed
    time.sleep(1) 