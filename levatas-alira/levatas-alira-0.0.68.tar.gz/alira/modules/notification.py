import os
import re
import json
import logging
import boto3
import requests

from importlib import import_module

from alira.instance import Instance
from alira.modules.redis import RedisModule

from botocore.exceptions import ClientError, EndpointConnectionError

PIPELINE_MODULE_NAME = "alira.modules.notification.email"


class EmailNotification(RedisModule):
    def __init__(
        self,
        model_identifier: str,
        configuration_directory: str,
        sender: str,
        recipients: list,
        subject: str,
        template_html_filename: str,
        template_text_filename: str,
        redis_server: str = None,
        filtering: str = None,
        provider=None,
        **kwargs,
    ):
        super().__init__(
            pipeline_module_name=PIPELINE_MODULE_NAME,
            model_identifier=model_identifier,
            configuration_directory=configuration_directory,
            redis_server=redis_server,
        )

        self.sender = sender
        self.recipients = recipients
        self.filtering = self._load_function(filtering)

        self.template_html_filename = template_html_filename
        self.template_text_filename = template_text_filename

        self.subject = subject

        self.provider = provider or AwsSesEmailNotification(**kwargs)

    def run(self, instance: Instance, **kwargs):
        if self.filtering and not self.filtering(instance):
            logging.info(
                f"The instance didn't pass the filtering criteria. Instance: {instance}"
            )
            return None

        if not hasattr(self.provider, "send_email") or not callable(
            self.provider.send_email
        ):
            logging.info("The specified provider is not valid")
            return None

        template_text = self._load_template(
            instance,
            os.path.join(
                self.configuration_directory,
                self.model_identifier,
                self.template_text_filename,
            ),
        )

        if not template_text:
            logging.info("Couldn't load the template text file")
            return None

        template_html = self._load_template(
            instance,
            os.path.join(
                self.configuration_directory,
                self.model_identifier,
                self.template_html_filename,
            ),
        )

        if not template_html:
            logging.info("Couldn't load the template html file")
            return None

        logging.info(
            f"Sending an email with specified provider {self.provider.__class__.__name__}"
        )

        arguments = {
            "sender": self.sender,
            "recipients": self.recipients,
            "subject": self.subject,
            "template_text": template_text,
            "template_html": template_html,
        }

        try:
            queue = self.get_redis_queue()
            if queue:
                queue.enqueue(self.provider.send_email, **arguments)
            else:
                self.provider.send_email(
                    sender=self.sender,
                    recipients=self.recipients,
                    subject=self.subject,
                    template_text=template_text,
                    template_html=template_html,
                )
        except Exception as e:
            logging.exception("There was an error sending the notification email", e)

        return None

    def _load_template(self, instance: Instance, template_file):
        try:
            with open(template_file, encoding="UTF-8") as file:
                template = file.read()

            variables_pattern = re.compile(r"\[\[([A-Za-z0-9_.]+)\]\]")

            variables = variables_pattern.findall(template)
            for variable in variables:
                template = template.replace(
                    f"[[{variable}]]", str(instance.get_attribute(variable, default=""))
                )

            return template

        except FileNotFoundError:
            print("ERROR 1")
            logging.info(f"Template file {template_file} not found")
            return None
        except Exception as e:
            print(f"ERROR 2 {e}")
            logging.exception(e)
            return None

    def _load_function(self, function_name: str):
        if function_name is None:
            return None

        try:
            module_path, _, fn_name = function_name.rpartition(".")
            function = getattr(import_module(module_path), fn_name)
            logging.info(f"Loaded function {function_name}")

            return function
        except Exception as e:
            logging.exception(f"Unable to load function {function_name}", e)
            return None


class SocketIO(object):
    def __init__(
        self,
        model_identifier: str,
        endpoint: str,
        event: str = "dispatch",
        **kwargs,
    ):
        self.model_identifier = model_identifier
        self.endpoint = endpoint
        self.event = event

    def run(self, instance: Instance, **kwargs):
        payload = {
            "message": "pipeline-new-instance",
            "data": instance.__dict__,
            "pipeline_id": self.model_identifier,
        }

        self.emit(self.event, payload)

        return None

    def emit(self, event: str, payload=None):
        if not self.endpoint:
            return

        logging.info(
            f"Sending Socket IO notification to {self.endpoint}. Namespace: {self.model_identifier}"
        )

        payload["event"] = event
        payload["namespace"] = self.model_identifier

        try:
            requests.post(
                url=self.endpoint,
                data=json.dumps(payload),
                headers={"Content-type": "application/json"},
            )
        except Exception:
            logging.exception("There was an error sending the socket io notification")


class AwsSesEmailNotification(object):
    def __init__(
        self, aws_access_key: str, aws_secret_key: str, aws_region_name: str, **kwargs
    ):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_region_name = aws_region_name

    def send_email(
        self,
        sender: str,
        recipients: list,
        subject: str,
        template_text: str,
        template_html: str,
    ):
        payload = {
            "Destination": {"ToAddresses": recipients},
            "Message": {
                "Body": {
                    "Html": {"Charset": "UTF-8", "Data": template_html},
                    "Text": {"Charset": "UTF-8", "Data": template_text},
                },
                "Subject": {"Charset": "UTF-8", "Data": subject},
            },
            "Source": sender,
        }

        try:
            logging.info(
                (
                    "Sending an email using AWS SES Service... \n"
                    f"Sender: {sender}\n"
                    f"Recipients: {recipients}\n"
                    f"Subject: {subject}"
                )
            )

            client = boto3.client(
                "ses",
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.aws_region_name,
            )

            client.send_email(**payload)

        except EndpointConnectionError as e:
            logging.exception(e)

            # If we can't connect to the service to send the email, let's
            # raise a RuntimeError so that the process can be retried as part
            # of the Redis queue.
            raise RuntimeError(e)
        except ClientError as e:
            logging.exception(e)
        except Exception as e:
            logging.exception(e)
