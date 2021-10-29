import flask
import requests
from urllib.parse import urljoin
from flask import request
from datetime import datetime
import time
from flask_babel import gettext
import os
import re
import logging

LOGGER = logging.getLogger(__name__)

class BackendException(Exception):
    """Exception for failed communication with the Taler merchant backend"""

    def __init__(self, message, backend_status=None, backend_json=None):
        super().__init__(backend_json.get("hint", message))
        self.backend_status = backend_status
        self.backend_json = backend_json

##
# POST a request to the backend, and return a error
# response if any error occurs.
#
# @param endpoint the backend endpoint where to POST
#        this request.
# @param json the POST's body.
# @return the backend response (JSON format).
def backend_post(backend_url, endpoint, json, auth_token=None):
    headers = dict()
    if auth_token:
        headers["Authorization"] = "Bearer " + auth_token
    final_url = urljoin(backend_url, endpoint)
    print("POSTing to: " + final_url)
    try:
        resp = requests.post(final_url, json=json, headers=headers)
    except requests.ConnectionError:
        raise BackendException(
            message=gettext("Could not establish connection to backend")
        )
    try:
        response_json = resp.json()
    except ValueError:
        raise BackendException(
            message=gettext("Could not parse response from backend"),
            backend_status=resp.status_code,
        )
    if resp.status_code != 200:
        raise BackendException(
            message=gettext("Backend returned error status"),
            backend_status=resp.status_code,
            backend_json=response_json,
        )
    print("Backend responds to {}: {}/{}".format(
        final_url,
        str(response_json),
        resp.status_code
    ))
    return response_json


##
# Issue a GET request to the backend.
#
# @param endpoint the backend endpoint where to issue the request.
# @param params (dict type of) URL parameters to append to the request.
# @return the JSON response from the backend, or a error response
#         if something unexpected happens.
def backend_get(backend_url, endpoint, params, auth_token=None):
    headers = dict()
    if auth_token is not None:
        headers["Authorization"] = "Bearer " + auth_token
    final_url = urljoin(backend_url, endpoint)
    print("GETting: " + final_url + " with params: " + str(params))
    try:
        resp = requests.get(final_url, params=params, headers=headers)
    except requests.ConnectionError:
        raise BackendException(
            message=gettext("Could not establish connection to backend")
        )
    try:
        response_json = resp.json()
    except ValueError:
        raise BackendException(message=gettext("Could not parse response from backend"))
    if resp.status_code != 200:
        raise BackendException(
            message=gettext("Backend returned error status"),
            backend_status=resp.status_code,
            backend_json=response_json,
        )
    print("Backend responds to {}: {}".format(final_url, str(response_json)))
    return response_json


def get_locale():
    parts = request.path.split("/", 2)
    if 2 >= len(parts):
        # Totally unexpected path format, do not localize
        return "en"
    lang = parts[1]
    if lang == "static":
        # Static resource, not a language indicator.
        # Do not localize then.
        return "en"
    return lang


##
# Helper function used inside Jinja2 logic to create a links
# to the current page but in a different language. Used to
# implement the "Language" menu.
#
def self_localized(lang):
    """
    Return URL for the current page in another locale.
    """
    path = request.path
    # path must have the form "/$LANG/$STUFF"
    parts = path.split("/", 2)
    if 2 >= len(parts):
        # Totally unexpected path format, do not localize
        return path
    return "/" + lang + "/" + parts[2]


class Deadline:
    def __init__(self, value):
        self.value = value

    def isExpired(self):
        if self.value == "never":
            return False
        now = int(round(time.time()) * 1000)
        now_dt = datetime.fromtimestamp(now / 1000)
        deadline_dt = datetime.fromtimestamp(self.value / 1000)
        print(
            "debug: checking refund expiration, now: {}, deadline: {}".format(
                now_dt.strftime("%c"), deadline_dt.strftime("%c")
            )
        )
        return now > self.value


all_languages = {
    "en": "English&nbsp;[en]",
    "ar": "عربى&nbsp;[ar]",
    "zh_Hant": "繁體中文&nbsp;[zh]",
    "fr": "Français&nbsp;[fr]",
    "de": "Deutsch&nbsp;[de]",
    "hi": "हिंदी&nbsp;[hi]",
    "it": "Italiano&nbsp;[it]",
    "ja": "日本語&nbsp;[ja]",
    "ko": "한국어&nbsp;[ko]",
    "pt": "Português&nbsp;[pt]",
    "pt_BR": "Português (Brazil)&nbsp;[pt_BR]",
    "ru": "Ру́сский язы́к&nbsp;[ru]",
    "es": "Español&nbsp;[es]",
    "sv": "Svenska&nbsp;[sv]",
    "tr": "Türk&nbsp;[tr]",
}


##
# Make the environment available into templates.
#
# @return the environment-reading function
def make_utility_processor(pagename):
    def utility_processor():
        def getactive():
            return pagename

        def getlang():
            return get_locale()

        def env(name, default=None):
            return os.environ.get(name, default)

        def prettydate(talerdate):
            parsed_time = re.search(r"/Date\(([0-9]+)\)/", talerdate)
            if not parsed_time:
                return "malformed date given"
            parsed_time = int(parsed_time.group(1))
            timestamp = datetime.datetime.fromtimestamp(parsed_time)
            # returns the YYYY-MM-DD date format.
            return timestamp.strftime("%Y-%b-%d")

        def static(name):
            return flask.url_for("static", filename=name)

        return dict(
            env=env,
            prettydate=prettydate,
            getactive=getactive,
            getlang=getlang,
            all_languages=all_languages,
            static=static,
        )

    return utility_processor
