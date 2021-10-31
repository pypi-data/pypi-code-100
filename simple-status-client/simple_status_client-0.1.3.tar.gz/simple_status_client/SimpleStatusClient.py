import hashlib
import json
from datetime import datetime
import logging

import requests
import yarl
from requests import Response

from simple_status_client.models import ConfigIn, StatusIn
from simple_status_client import Colors

logger = logging.getLogger(__name__)


class APIClient():

    def __init__(self, url):
        logging.info(f"Instantiating Client for {url}")
        self.url = yarl.URL(url)
        logging.debug("sending ping")
        response = requests.get(url=self.url / "ping")
        try:
            assert b"pong" in response.content
        except AssertionError as e:
            logging.error("Failed to ping the server.  This generally means that your server is not accessible from here, please verify that you can reach ")
            raise e

    def set_config_base(self,
                        component_key: int,
                        name: str,
                        details: str,
                        timeout_min: int,
                        timeout_color: Colors,
                        parent_key: int = 0,
                        ):
        """
        Base methods have full capability, but there may be an easier implementation for you to use.
        This method will set a config for a given a component using it's component_key to identify it.  The
        component_key must be unique, an easy way to do this is to pick a unqiue name and hash it
        :param component_key: a unique identifier for your component, non unique values will result in overwriting
        the config
        :param name: The name of your component
        :param parent_key: a key for your parent component, results in your
        :param details: Any further information about your component you wish to convey
        :param timeout_min: the number of minutes your status should remain valid for
        :param timeout_color: the color your status should change to once it times out, will never "improve" the
        color of your status
        :return:
        """
        logging.info(f"set_config_base being called")
        logging.debug(f"creating a ConfigIn object name={name}, parent_key={parent_key}, details={details}, timeout_min={timeout_min}, timeout_color={timeout_color}")
        config = ConfigIn(name=name, parent_key=parent_key, details=details, timeout_min=timeout_min,
                          timeout_color=timeout_color)
        url = self.url / "components" / str(component_key) / "config"
        logging.debug(f"sending to {url}")
        response = self.post_it(config, url)
        return response

    def set_config(self,
                   name: str,
                   details: str,
                   timeout_min: int,
                   timeout_color: Colors,
                   parent_name: str = "",
                   ):
        """
        This method will set a config for a given a component using it's name to identify it.  The
        name must be unique!
        :param name: The name of your component
        :param details: Any further information about your component you wish to convey
        :param timeout_min: the number of minutes your status should remain valid for
        :param timeout_color: the color your status should change to once it times out, will never "improve" the
        color of your status
        :param parent_name: a key for your parent component, results in your
        :return:
        """

        logging.info(f"set_config being called")
        logging.debug(f"parent_name={parent_name}")
        if not parent_name:
            parent_id = 0
        else:
            parent_id = self.name_to_component_id(parent_name)
        logging.debug(f"parent_id is calculated to be {parent_id}")

        component_id = self.name_to_component_id(name)
        logging.debug(f"comporent_id is calculated to be {component_id}")

        return self.set_config_base(component_id, name, details, timeout_min, timeout_color, parent_id)

    @staticmethod
    def name_to_component_id(name: str) -> int:
        """
        creates a unique component id assuming a unique name
        :param name: the name you wish converted to a component id
        :return:
        """
        return int.from_bytes(hashlib.md5(name.encode('utf-8')).digest(), 'little')

    def set_status_base(self,
                        component_key: int,
                        color: Colors,
                        message: str,
                        date: datetime = False,
                        ):
        """
        Base methods have full capability, but there may be an easier implementation for you to use.
        Sets the status for a given component_key
        :param component_key:
        :param color: The color to use for the status
        :param message: Any information you wish accessible on the server about the status
        :param date: the date of the status, defaults to now
        :return:
        """
        logging.info(f"set_status_base being called")
        logging.debug(f"color={color} message={message} date={date}")

        if not date:
            date = datetime.now()
        logging.debug(f"calculated date={date}")
        logging.debug(f"creating StatusIn with the above")
        status = StatusIn(color=color, date=date, message=message)
        url = self.url / "components" / str(component_key) / "status"
        logging.debug(f"sending to {url}")
        response = self.post_it(status, url)
        return response

    def set_status(self,
                   name: str,
                   color: Colors,
                   message: str,
                   date: datetime=False,
                   ):
        """
        Base methods have full capability, but there may be an easier implementation for you to use.
        Sets the status for a given component_key
        :param component_key:
        :param color: The color to use for the status
        :param message: Any information you wish accessible on the server about the status
        :param date: the date of the status, defaults to now
        :return:
        """
        return self.set_status_base(self.name_to_component_id(name), color, message, date)


    def clear_statuses_base(self, component_key) -> Response:
        """
        clear the statuses from a specific component by component_key.  Will clear entire status history
        :param component_key: the unique component id identifying which component to clear status history from
        :return: str: from server
        """
        logging.info(f"clear_statuses being called on {component_key}")

        url = self.url / "components" / str(component_key) / "status" / "clear"
        logging.debug(f"sending to {url}")
        response = self.get_it(url)
        return response

    def clear_statuses(self, name) -> Response:
        """
        clear the statuses from a specific component by name.  Will clear entire status history
        :param name:
        :return:
        """
        logging.info(f"clear_statuses being called on {name}")
        response = self.clear_statuses_base(self.name_to_component_id(name))
        return response

    def clear_all_statuses(self)-> Response:
        """
        clear all statuses from every component
        :return:
        """
        logging.info(f"clear_all_statuses being called")
        url = self.url / "components" / "statuses" / "clear"
        response = self.get_it(url)
        return  response

    def clear_config_base(self, component_key) -> str:
        return "not implemented, in general you shouldn't need to clear these.  You either overwrite them, ignore them, or if you want to restart the docker container to start fresh"


    def clear_config(self, name) -> str:
        return "not implemented, in general you shouldn't need to clear these.  You either overwrite them, ignore them, or if you want to restart the docker container to start fresh"

    def clear_all_config(self) -> str:
        return "not implemented, in general you shouldn't need to clear these.  You either overwrite them, ignore them, or if you want to restart the docker container to start fresh"

    @staticmethod
    def post_it(post_content, url):
        response = APIClient.send_it("post",content=post_content,url=url)
        return response

    @staticmethod
    def get_it(url):
        response = APIClient.send_it("get",url=url)
        return response

    @staticmethod
    def send_it(type: str,url,content:dict={} ):
        if "post" in type.lower():
            response = requests.post(url, json=json.loads(content.json()))
        elif "get" in type.lower():
            response = requests.get(url)

        logging.info(f"status_code={response.status_code} content={response.content}")
        if response.status_code != 200:
            raise Exception(response.content)
        return response

