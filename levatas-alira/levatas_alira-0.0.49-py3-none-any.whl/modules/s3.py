import boto3
import uuid
import logging
import os
from pathlib import Path

from alira.instance import Instance
from alira.modules.redis import RedisModule

from botocore.exceptions import ClientError, EndpointConnectionError

PIPELINE_MODULE_NAME = "alira.modules.s3"


class S3(RedisModule):
    def __init__(
        self,
        model_identifier: str,
        model_directory: str,
        aws_s3_bucket: str,
        aws_s3_key_prefix: str,
        aws_s3_public: bool,
        aws_access_key: str,
        aws_secret_key: str,
        aws_region_name: str,
        redis_server: str = None,
        filtering_fn: callable = None,
        **kwargs,
    ):
        super().__init__(
            pipeline_module_name=PIPELINE_MODULE_NAME,
            model_identifier=model_identifier,
            model_directory=model_directory,
            redis_server=redis_server,
        )

        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_region_name = aws_region_name

        self.filtering_fn = filtering_fn
        self.aws_s3_bucket = aws_s3_bucket
        self.aws_s3_key_prefix = aws_s3_key_prefix

        if self.aws_s3_key_prefix and self.aws_s3_key_prefix.endswith("/"):
            self.aws_s3_key_prefix = self.aws_s3_key_prefix[:-1]

        self.aws_s3_public = aws_s3_public

    def run(self, instance: Instance, **kwargs):
        if self.filtering_fn and not self.filtering_fn(instance):
            logging.info(
                f"The instance didn't pass the filtering criteria. Instance: {instance}"
            )
            return None

        if instance.image is None:
            logging.info("The instance doesn't have an image")
            return None

        image_filename = os.path.join(self.model_directory, "images", instance.image)

        s3_key = f"{instance.image}-{uuid.uuid4().hex}.png"

        if self.aws_s3_key_prefix:
            s3_key = f"{self.aws_s3_key_prefix}/{s3_key}"

        arguments = {
            "aws_s3_bucket": self.aws_s3_bucket,
            "aws_s3_public": self.aws_s3_public,
            "s3_key": s3_key,
            "image_filename": image_filename,
            "aws_access_key": self.aws_access_key,
            "aws_secret_key": self.aws_secret_key,
            "aws_region_name": self.aws_region_name,
        }

        try:
            queue = self.get_redis_queue()
            if queue:
                queue.enqueue(self._upload, **arguments)
            else:
                self._upload(**arguments)

            result = {"s3_image_uri": f"s3://{self.aws_s3_bucket}/{s3_key}"}

            if self.aws_s3_public:
                result[
                    "s3_image_public_uri"
                ] = f"https://{self.aws_s3_bucket}.s3.amazonaws.com/{s3_key}"

            return result

        except Exception as e:
            logging.exception("There was an error sending the notification email", e)
            return None

    def _upload(
        self,
        aws_s3_bucket,
        aws_s3_public,
        s3_key,
        image_filename,
        aws_access_key,
        aws_secret_key,
        aws_region_name,
    ):
        logging.info(
            f'Uploading {image_filename} to bucket "{aws_s3_bucket}" and location {s3_key}...'
        )
        try:
            session = boto3.Session(
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=aws_region_name,
            )
            client = session.client("s3")

            with open(image_filename, "rb") as file:
                buffer = file.read()

            arguments = {"Bucket": aws_s3_bucket, "Key": s3_key, "Body": buffer}
            content_type = "binary/octet-stream"

            extension = Path(image_filename).suffix.lower()

            if extension in ["jpg", "jpeg"]:
                content_type = "image/jpeg"
            elif extension == "png":
                content_type = "image/png"

            arguments["ContentType"] = content_type

            if aws_s3_public:
                arguments["ACL"] = "public-read"

            client.put_object(**arguments)

            s3_location = f"s3://{aws_s3_bucket}/{s3_key}"
            logging.info(f"Uploaded {image_filename} to {s3_location}")

            return s3_location

        except EndpointConnectionError as e:
            logging.exception(e)

            # If we can't connect to the service to upload the image, let's
            # raise a RuntimeError so that the process can be retried as part
            # of the Redis queue.
            raise RuntimeError(e)
        except ClientError as e:
            logging.exception(e)
        except Exception as e:
            logging.exception(e)

        return None


