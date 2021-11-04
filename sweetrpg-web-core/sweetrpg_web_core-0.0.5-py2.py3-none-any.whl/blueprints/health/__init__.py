# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""health.py
Health endpoints.
"""

from flask import Blueprint, current_app, jsonify
from werkzeug.exceptions import HTTPException
import json
import os
from sweetrpg_web_core import constants


blueprint = Blueprint("health", __name__, url_prefix="/health")


@blueprint.route("/status")
def health_check():
    r = {'services':{}}
    build_info_path = os.environ.get(constants.BUILD_INFO_PATH)
    if build_info_path:
        with open(build_info_path, "r") as bi:
            build_info = json.load(bi)
            r["build"] = build_info

    return r


@blueprint.route("/ping")
def ping():
    return "pong"
