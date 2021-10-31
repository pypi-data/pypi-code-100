import os
import json
import logging

from time import time

import requests

from ml_metadata.proto import metadata_store_pb2
from ml_metadata.errors import NotFoundError

from ..instance import Instance


logger = logging.getLogger(__name__)


def dumps(payload):
    return json.dumps(
        payload, default=lambda x: "Not serializable"
    )

def _round(value, point_round):
    if point_round is not None:
        return round(value, point_round)

    return value


class NotificationServiceFactory(object):
    """ Factory class of notification services
        responsible for create each notification services.
    """
    def __init__(self, socketio_url):
        """
        :param socketio_url The URL of the socket.io service.
        :type socketio_url: str, required
        """

        self.socketio_url = socketio_url

        self._instance_notification_service = None

    def instance_notification_service(self, event: str = 'dispatch'):
        """ Returns an instance of class:
        `alira.components.socketio.InstanceNotificationService`.
        """
        if not self._instance_notification_service:
            self._instance_notification_service = InstanceNotificationService(
                self.socketio_url, event
            )

        return self._instance_notification_service


class NotificationService(object):
    """ Notification service class responsible for sending
    socket.io notifications to subscribers.
    """
    def __init__(self, socketio_url):
        """
        :param socketio_url The URL of the socket.io service.
        :type socketio_url: str, required
        """
        self.socketio_url = socketio_url

    def emit(self, event: str, payload=None, namespace=None):
        """ Sends a socket.io notification.
        """

        if not self.socketio_url:
            return

        if not payload:
            payload = {}

        payload["event"] = event

        if namespace:
            payload['namespace'] = namespace

        try:            
            requests.post(
                url=self.socketio_url,
                data=dumps(payload),
                headers={'Content-type': 'application/json'})
        except Exception:
            logger.error(
                'There was an error sending the notification',
                exc_info=True
            )


class InstanceNotificationService(NotificationService):
    def __init__(self, socketio_url, event='dispatch'):
        super(InstanceNotificationService, self).__init__(socketio_url)

        self.event = event

    def notify_new_instance(self, model_id, data):
        logger.debug('Notifying new instance.')

        payload = {
            'message': 'pipeline-new-instance',
            'data': data,
            'pipeline_id': model_id
        }

        logger.debug('Instance: {}'.format(dumps(payload)))

        self.emit(self.event, payload, model_id)


class Dashboard(object):
    def __init__(
        self,
        data_transformation_func: callable = None,
        point_round: int = 2,
        socketio_api_url: str = "http://alira-dashboard:5003",
        event: str = "dispatch", **kwargs
    ):
        self.name = "alira.Dashboard"
        self.data_transformation_func = data_transformation_func
        self.point_round = point_round
        self.socketio_api_url = socketio_api_url
        self.event = event
        self.notification_factory = NotificationServiceFactory(socketio_api_url)

        if (
            data_transformation_func is not None
            and not callable(data_transformation_func)
        ):
            raise ValueError("'data_transformation' must be a callable or None.")

        self.model_base_directory = kwargs.get(
            "model_base_directory",
            "/opt/ml/alira"
        )

    def run(self, instance: Instance, pipeline_id: str, **kwargs):
        # Generating dashboard data transformation
        dashboard_result = self._generate_dashboard(instance)
        if self.data_transformation_func:
            data_transformation = self.data_transformation_func(
                instance=instance, pipeline_id=pipeline_id,
                point_round=self.point_round,
                **kwargs
            )

            if not isinstance(data_transformation, dict):
                raise ValueError("The result of 'data_transformation_func' must be a dict.")

            for key, value in data_transformation.items():
                dashboard_result[key] = value

        instance_to_notify = instance.to_dict()
        instance_to_notify[self.name] = dashboard_result
        
        # Notifying instance via SocketIO
        model_id = os.path.basename(self.model_base_directory)
        instance_notification_service = (
            self.notification_factory.instance_notification_service(self.event)
        )
        instance_notification_service.notify_new_instance(model_id, instance_to_notify)

        return dashboard_result

    def register(self, store):
        try:
            component_execution_type = store.get_execution_type(type_name=self.name + "Type")
            component_execution_type_id = component_execution_type.id
        except NotFoundError:
            component_execution_type = metadata_store_pb2.ExecutionType()
            component_execution_type.name = self.name + "Type"
            component_execution_type.properties["name"] = metadata_store_pb2.STRING
            component_execution_type.properties["point_round"] = metadata_store_pb2.INT
            component_execution_type.properties["socketio_api_url"] = metadata_store_pb2.STRING
            component_execution_type.properties["event"] = metadata_store_pb2.STRING
            component_execution_type_id = store.put_execution_type(component_execution_type)

        component_execution = metadata_store_pb2.Execution()
        component_execution.type_id = component_execution_type_id
        component_execution.last_known_state = metadata_store_pb2.Execution.State.NEW
        component_execution.properties["name"].string_value = self.name
        component_execution.properties["point_round"].int_value = self.point_round
        component_execution.properties["socketio_api_url"].string_value = self.socketio_api_url
        component_execution.properties["event"].string_value = self.event
        component_execution.create_time_since_epoch = int(time() * 1000)
        [component_execution_id] = store.put_executions([component_execution])
        component_execution.id = component_execution_id
        
        return component_execution, None

    def _generate_dashboard(self, instance: Instance):
        result = {
            "classification": "Positive"
                if instance.classification == 1
                else "Negative"
        }
        result["confidence"] = str(
            _round(instance.confidence * 100, self.point_round)
        ) + "%"

        selected = (
            instance.get_attribute("alira.StaticSelection")["selected"]
            if  instance.has_attribute("alira.StaticSelection")
            else 0
        )
        flagged = (
            instance.get_attribute("alira.Flagging")["flagged"]
            if instance.has_attribute("alira.Flagging")
            else instance.get_attribute("alira.ConfidenceFlagging")["flagged"]
            if instance.has_attribute("alira.ConfidenceFlagging")
            else 0
        )

        result["list.selected"] = "Yes" if selected or flagged else "No"
        result["detail.selected"] = "Yes" if selected else "No"
        result["detail.flagged"] = "Yes" if flagged else "No"

        return result