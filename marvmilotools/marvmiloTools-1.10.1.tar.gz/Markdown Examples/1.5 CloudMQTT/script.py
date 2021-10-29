import marvmiloTools as mmt

#init cloudMQTT client
cloudmqtt = mmt.CloudMQTT(
    client_name = "clientname", 
    channel = "channel", 
    qos = 0
)

#connect to server
cloudmqtt.connect(
    user = "user", 
    pw = "p@ssw0rd", 
    addr = "cloudmqtt.com", 
    port = 1234
)

#reconnecting to server if no connection
if not cloudmqtt.check_connection():
    cloudmqtt.reconnect()

#on message function
def on_message(msg, topic):
    print(f"received message: '{msg}', topic: '{topic}'")
    
#binding on_message function to a topic
cloudmqtt.bind(topic = "hello", function = on_message)

#publishing a message
cloudmqtt.publish(topic = "hello", message = "world")

#response function
def on_request(msg, topic):
    resp = "hello world"
    print(f"publishing response: {resp}")
    return(resp)

#binding on_request to request topic
cloudmqtt.bind_response("demo", on_request)

#request data from server
resp = (
    cloudmqtt.request(
        topic = "demo",
        message = ".",
        retry = 5
    )
)
print("got response: " + resp)

#disconnecting form server
cloudmqtt.disconnect()