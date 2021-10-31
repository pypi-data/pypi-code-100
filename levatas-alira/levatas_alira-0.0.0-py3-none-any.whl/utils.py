import os
import base64
import uuid
import logging
import sys
import traceback

import requests
import boto3

from urllib.parse import urlparse


logger = logging.getLogger(__name__)


def download_http_image(image: str) -> bytes:
    try:
        response = requests.get(image)
        return response.content
    except Exception:
        return None


def download_s3_image(
    aws_bucket_name: str, s3_key: str,
    aws_access_key: str, aws_secret_key: str,
    aws_region_name: str
) -> bytes:
    try:
        session = boto3.Session(
            region_name=aws_region_name,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
        )
        s3_client = session.client('s3')
        s3_object = s3_client.get_object(
            Bucket=aws_bucket_name, Key=s3_key
        )

        return s3_object['Body'].read()
    except Exception as e:
        _, _, exc_tb = sys.exc_info()
        logger.error(traceback.print_tb(exc_tb))

        message = "There was an error in Alira::download_s3_image: {}".format(
            str(e))
        logger.error(message)
        return None


def base64decode(data: str) -> bytes:
    base64buffer = data.encode('utf-8')
    return base64.b64decode(base64buffer)


def base64encode(data: bytes) -> str:
    base64buffer = base64.b64encode(data)
    return base64buffer.decode('utf-8')


def export_image(image: str, export_to: str) -> str:
    fragments = urlparse(image, allow_fragments=False)
    if fragments.scheme in ("http", "https", "file", "s3"):
        return image

    if len(image) < 256:
        filepath = os.path.join(export_to if export_to else "", image)
        if os.path.exists(filepath):
            return filepath

    os.makedirs(export_to, exist_ok=True)

    image_file_name = "{}.png".format(uuid.uuid4().hex)
    image_file = os.path.join(export_to, image_file_name)

    buffer = base64decode(image)
    with open(image_file, "wb") as file:
        file.write(buffer)

    return image_file_name


def to_base64(image: str, image_directory=None, **kwargs) -> str:
    fragments = urlparse(image, allow_fragments=False)
    if fragments.scheme in ("http", "https"):
        buffer = download_http_image(image)
        return base64encode(buffer)

    if fragments.scheme == "file":
        image_file = os.path.abspath(
            os.path.join(fragments.netloc, fragments.path))
        with open(image_file, "rb") as file:
            buffer = file.read()
            return base64encode(buffer)

    if fragments.scheme == "s3":
        aws_access_key = kwargs.get("aws_access_key", None)
        aws_secret_key = kwargs.get("aws_secret_key", None)
        aws_region_name = kwargs.get("aws_region_name", None)

        buffer = download_s3_image(
            fragments.netloc, fragments.path,
            aws_access_key, aws_secret_key,
            aws_region_name
        )

        return base64encode(buffer)

    filepath = os.path.join(image_directory if image_directory else "", image)
    
    if os.path.exists(filepath):
        with open(filepath, "rb") as file:
            buffer = file.read()
            return base64encode(buffer)

    return image


def process_image(image: str, image_directory: str, **kwargs):
    base64 = to_base64(image, image_directory, **kwargs)
    filename = export_image(image, export_to=image_directory) if image_directory else None
    
    return base64, filename


def get_value_from_dict(obj: dict, field: str):
    if not isinstance(obj, dict):
        return None

    fields = field.split(".", 1)
    current_field = ""
    while len(fields) > 1:
        current_field += (
            ".{}".format(fields[0]) if len(current_field) > 0 else fields[0]
        )
        field = fields[1]
        if current_field in obj:
            result = get_value_from_dict(obj[current_field], field)
            if result is not None:
                return result

        fields = field.split(".", 1)

    current_field += (
        ".{}".format(fields[0]) if len(current_field) > 0 else fields[0]
    )
    return obj.get(current_field, None)


def remove_attribute_from_dict(obj: dict, field: str):
    if not isinstance(obj, dict):
        return False

    fields = field.split(".", 1)
    current_field = ""
    while len(fields) > 1:
        current_field += (
            ".{}".format(fields[0]) if len(current_field) > 0 else fields[0]
        )
        field = fields[1]
        if current_field in obj:
            result = remove_attribute_from_dict(obj[current_field], field)
            if result:
                return result

        fields = field.split(".", 1)

    current_field += (
        ".{}".format(fields[0]) if len(current_field) > 0 else fields[0]
    )

    if current_field in obj:
        del obj[current_field]
        return True

    return False


def update_attribute_in_dict(obj: dict, field: str, value):
    if not isinstance(obj, dict):
        return False

    fields = field.split(".", 1)
    current_field = ""
    while len(fields) > 1:
        current_field += (
            ".{}".format(fields[0]) if len(current_field) > 0 else fields[0]
        )
        field = fields[1]
        if current_field in obj:
            result = update_attribute_in_dict(obj[current_field], field, value)
            if result:
                return result

        fields = field.split(".", 1)

    current_field += (
        ".{}".format(fields[0]) if len(current_field) > 0 else fields[0]
    )

    if current_field in obj:
        obj[current_field] = value

        return True

    return False
