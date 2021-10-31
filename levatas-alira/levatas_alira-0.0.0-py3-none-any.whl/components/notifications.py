import os
import logging
import sys
import traceback
import re
import json

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError

from ..instance import Instance
from ..utils import get_value_from_dict
from .utils import ONLY_POSITIVE_INSTANCES, has_to_notify

from .asynchronous import AsynchronousModule


logger = logging.getLogger(__name__)


class SesNotifications(AsynchronousModule):

    @staticmethod
    def get_message_from_template(instance: dict, template_path: str, charset: str):
        variables_pattern = re.compile("{{\s*\w[\w|'.']*\s*}}")
        with open(template_path, encoding=charset) as file:
            file_content = file.read()
        
        variables = variables_pattern.findall(file_content)
        for variable in variables:
            variable_name = variable[2:-2].strip()
            value = str(get_value_from_dict(instance, variable_name))

            file_content = file_content.replace(variable, value, 1)

        return file_content

    def __init__(
        self,
        sender: str,
        recipients: list,
        subject: str,
        template_html: str,
        template_text: str = None,
        notification = ONLY_POSITIVE_INSTANCES,
        aws_access_key: str = None,
        aws_secret_key: str = None,
        aws_region_name: str = None,
        charset: str = "UTF-8",
        data_transformation_fn: callable = None,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.name = kwargs.get("name", "alira.sesnotifications")
        self.sender = sender
        self.recipients = recipients
        self.template_html = template_html
        self.template_text = template_text
        self.subject = subject
        self.charset = charset

        if (
            not isinstance(notification, str)
            and not callable(notification)
        ):
            raise ValueError("'notification' must be 'str' or 'callable'.")

        self.notification = notification

        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_region_name = aws_region_name

        if (
            data_transformation_fn is not None
            and not callable(data_transformation_fn)
        ):
            raise ValueError("'data_transformation_func' must be 'None' or 'callable'.")

        self.data_transformation_fn = data_transformation_fn

        self.directory = kwargs.get(
            "model_base_directory",
            "/opt/ml/alira"
        )

    def run(self, instance: Instance, pipeline_id: int, **kwargs):
        if not has_to_notify(
            instance=instance,
            notification=self.notification,
            pipeline_id=pipeline_id,
            **kwargs
        ):
            return None

        logger.info("Sending SES email")

        data_transformation = None
        instance_dict = instance.to_dict()
        if callable(self.data_transformation_fn):
            data_transformation = self.data_transformation_fn(
                instance=instance,
                pipeline_id=pipeline_id,
                **kwargs
            )

            logger.debug("Data transformation: {}".format(
                json.dumps(data_transformation, default= lambda x: "Not serializable")
            ))

            instance_dict[self.name] = data_transformation

        arguments = self._get_ses_arguments(instance_dict)
        queue = self._get_queue()
        if queue:
            job = queue.enqueue(self._send_email, **arguments)
            if self.job_field and data_transformation:
                data_transformation[self.job_field] = job.get_id()
        else:
            self._send_email(**arguments)

        return data_transformation

    def _get_ses_client_with_credentials(self):
        return boto3.client(
            "ses",
            region_name=self.aws_region_name,
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
        )

    def _get_ses_client_without_credentials(self):
        return boto3.client("ses")

    def _get_ses_client(self):
        return (
            self._get_ses_client_with_credentials()
            if self.aws_access_key is not None
            and self.aws_secret_key is not None
            and self.aws_region_name is not None
            else self._get_ses_client_without_credentials()
        )

    def _get_ses_arguments(self, instance: dict):
        template_html = os.path.join(self.directory, self.template_html)
        if not os.path.isfile(template_html):
            logger.debug("'{}' does not exist.".format(template_html))
            raise Exception("'template_html' does not contain an existent file path.")

        logger.debug("Instance: {}".format(
            json.dumps(instance, default= lambda x: "Not serializable")
        ))
        
        body_html = SesNotifications.get_message_from_template(
            instance, template_html, self.charset
        )
        body_text = ""
        if self.template_text:
            template_text = os.path.join(self.directory, self.template_text)
            if not os.path.isfile(template_text):
                logger.debug("'{}' does not exist.".format(template_text))
                raise Exception(
                    "'template_text' does not contain an existent file path."
                )
    
            body_text = SesNotifications.get_message_from_template(
                instance, template_text, self.charset
            )

        return {
            "Destination": {
                "ToAddresses": self.recipients
            },
            "Message": {
                "Body": {
                    "Html": {
                        "Charset": self.charset,
                        "Data": body_html
                    },
                    "Text": {
                        "Charset": self.charset,
                        "Data": body_text
                    }
                },
                "Subject": {
                    "Charset": self.charset,
                    "Data": self.subject
                }
            },
            "Source": self.sender
        }

    def _send_email(self, **kwargs):
        try:
            self._get_ses_client().send_email(**kwargs)
        except ClientError as e:
            self._retry(e)
        except EndpointConnectionError as e:
            self._retry(e)
        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            logger.error(traceback.print_tb(exc_tb))

            message = "There was an error in SnsNotification::process: {}".format(str(e))
            logger.error(message)

    def _retry(self, e: Exception):
        _, _, exc_tb = sys.exc_info()
        logger.error(traceback.print_tb(exc_tb))

        message = "There was an error in SnsNotification::process: {}".format(str(e))
        logger.error(message)

        raise RuntimeError(e)
