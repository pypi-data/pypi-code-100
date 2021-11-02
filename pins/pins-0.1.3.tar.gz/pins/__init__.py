"""
A simple package to be able to "pin" data to an RStudio Connect instance
"""

import os
import json
import pickle
import tarfile
import tempfile
import requests as req

try:
    from importlib import metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata

__version__ = metadata.version("pins")


def pin_rsconnect(data, pin_name, pretty_pin_name, connect_server, api_key):
    """
    Make a pin on RStudio Connect.

      Parameters:
        data: any object that has a to_json method (eg. pandas DataFrame)
        pin_name (str): name of pin, only alphanumeric and underscores
        pretty_pin_name (str): display name of pin
        connect_server (str): RStudio Connect server address e.g. https://connect.example.com/
        api_key (str): API key of a user on RStudio Connect

       Return:
         Url of content

    """
    # Save data
    local_dir = tempfile.TemporaryDirectory()
    data.to_json(local_dir.name + "/data.txt")

    # Create landing page
    i = open(local_dir.name + "/index.html", "w")
    lines = ["<h1>Python Pin", "\n"]
    for line in lines:
        i.write(line)
    i.close()

    # Create Manifest
    manifest = {
        "version": 1,
        "locale": "en_US",
        "platform": "3.5.1",
        "metadata": {
            "appmode": "static",
            "primary_rmd": None,
            "primary_html": "index.html",
            "content_category": "pin",
            "has_parameters": False,
        },
        "packages": None,
        "files": None,
        "users": None,
    }
    with open(local_dir.name + "/manifest.json", "w") as manifest_conn:
        json.dump(manifest, manifest_conn)

    # Turn into tarfile
    pins_tf = tempfile.NamedTemporaryFile(delete=False)
    with tarfile.open(pins_tf.name, "w:gz") as tar:
        tar.add(local_dir.name, arcname=os.path.basename(local_dir.name))

    auth = {"Authorization": "Key " + api_key}

    content = get_content(pin_name, pretty_pin_name, connect_server, auth)
    content_url = connect_server + "/__api__/v1/content/" + content["guid"]

    # Upload Bundle
    with open(pins_tf.name, "rb") as tf_conn:
        bundle = req.post(content_url + "/bundles", headers=auth, data=tf_conn)
    bundle_id = bundle.json()["id"]

    # Deploy bundle
    deploy = req.post(
        content_url + "/deploy", headers=auth, json={"bundle_id": bundle_id}
    )
    return {"dash_url": content["dashboard_url"], "content_url": content["content_url"]}


def get_content(pin_name, pretty_pin_name, connect_server, auth):
    """
    Intermediate function to get content from Connect
    """
    content = req.get(
        connect_server + "/__api__/v1/content", headers=auth, params={"name": pin_name}
    ).json()
    if content:  # content item created already
        return content[0]
    data = {"access_type": "acl", "name": pin_name, "title": pretty_pin_name}
    content = req.post(
        connect_server + "/__api__/v1/content", headers=auth, json=data
    ).json()
    return content


def pin_get_rsconnect(url, api_key):
    """
    Get data from a python pin on RStudio Connect

      Parameters:
        url (str) content solo URL on Connect (NOT dashboard URL)
        api_key (str): API key of a user on RStudio Connect

      Returns:
        JSON version of pin
    """
    auth = {"Authorization": "Key " + api_key}
    res = req.get(url + "/data.txt", headers=auth)
    return res.json()
