import oneagent
import wrapt
from oneagent.common import MessagingDestinationType

from ...log import logger
from ...sdk import sdk


def instrument():
    # @wrapt.patch_function_wrapper("google.pubsub_v1", "SubscriberClient.__init__")
    # def init_wrapper(init, message, args, kwargs):
    #     print(init, message, args, kwargs)
    #     return init(*args, **kwargs)

    @wrapt.patch_function_wrapper("google.cloud.pubsub_v1.publisher.client", "Client.publish")
    def publish_wrapper(publish, client, args, kwargs):
        topic = args[0]
        msi = sdk.create_messaging_system_info("Google Pub/Sub", topic, MessagingDestinationType.TOPIC, oneagent.sdk.Channel(oneagent.sdk.ChannelType.OTHER, "pubsub.googleapis.com:443"))
        with msi:
            with sdk.trace_outgoing_message(msi) as tracer:
                tag = tracer.outgoing_dynatrace_string_tag
                kwargs["x-dynatrace"] = tag
                logger.debug("autodynatrace - Tracing google pub/sub, topic: '{}', tag: '{}'".format(topic, tag))
                return publish(*args, **kwargs)

    # return init(*args, **kwargs)
