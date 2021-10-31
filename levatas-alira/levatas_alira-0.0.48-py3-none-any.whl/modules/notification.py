import os
import re
import logging
import boto3

from alira.instance import Instance
from alira.modules.redis import RedisModule

from botocore.exceptions import ClientError, EndpointConnectionError

PIPELINE_MODULE_NAME = "alira.modules.notification.email"


class EmailNotification(RedisModule):
    def __init__(
        self,
        model_identifier: str,
        model_directory: str,
        sender: str,
        recipients: list,
        subject: str,
        template_html_filename: str,
        template_text_filename: str,
        redis_server: str = None,
        filtering_fn: callable = None,
        provider=None,
        **kwargs,
    ):
        super().__init__(
            pipeline_module_name=PIPELINE_MODULE_NAME,
            model_identifier=model_identifier,
            model_directory=model_directory,
            redis_server=redis_server,
        )

        self.sender = sender
        self.recipients = recipients
        self.filtering_fn = filtering_fn

        self.template_html_filename = template_html_filename
        self.template_text_filename = template_text_filename

        self.subject = subject

        self.provider = provider or AwsSesEmailNotification(**kwargs)

    def run(self, instance: Instance, **kwargs):
        if self.filtering_fn and not self.filtering_fn(instance):
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
            instance, os.path.join(self.model_directory, self.template_text_filename)
        )

        if not template_text:
            logging.info("Couldn't load the template text file")
            return None

        template_html = self._load_template(
            instance, os.path.join(self.model_directory, self.template_html_filename)
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
                    f"[[{variable}]]", str(instance.get_attribute(variable))
                )

            return template

        except FileNotFoundError:
            logging.info(f"Template file {template_file} not found")
            return None
        except Exception as e:
            logging.exception(e)
            return None


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
