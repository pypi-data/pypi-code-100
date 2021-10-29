##
# This file is part of GNU TALER.
# Copyright (C) 2017, 2020 Taler Systems SA
#
# TALER is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free Software
# Foundation; either version 2.1, or (at your option) any later version.
#
# TALER is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with
# GNU TALER; see the file COPYING.  If not, see <http://www.gnu.org/licenses/>
#
# @author Marcello Stanisci
# @brief Minimal Website to tip users who fill the survey.

import os
import re
import datetime
import base64
import logging
from urllib.parse import urljoin
import flask
from flask import request
from flask_babel import Babel
from flask_babel import refresh
from flask_babel import force_locale
from flask_babel import gettext
import traceback
from taler.util.talerconfig import TalerConfig, ConfigurationError
from ..httpcommon import (
    backend_get,
    backend_post,
    self_localized,
    BackendException,
    make_utility_processor,
    get_locale,
)
import sys

if not sys.version_info.major == 3 and sys.version_info.minor >= 6:
    print("Python 3.6 or higher is required.")
    print(
        "You are using Python {}.{}.".format(
            sys.version_info.major, sys.version_info.minor
        )
    )
    sys.exit(1)

app = flask.Flask(__name__, template_folder="../templates", static_folder="../static")
app.debug = True
app.secret_key = base64.b64encode(os.urandom(64)).decode("utf-8")

LOGGER = logging.getLogger(__name__)
TC = TalerConfig.from_env()
try:
    BACKEND_URL = TC["frontends"]["backend"].value_string(required=True)
    CURRENCY = TC["taler"]["currency"].value_string(required=True)
    APIKEY = TC["frontends"]["backend_apikey"].value_string(required=True)
except ConfigurationError as ce:
    print(ce)
    exit(1)

BABEL_TRANSLATION_DIRECTORIES = "../translations"

app.config.from_object(__name__)
babel = Babel(app)
babel.localeselector(get_locale)

INSTANCED_URL = urljoin(BACKEND_URL, f"instances/survey/")

LOGGER.info("Using translations from:" + ":".join(list(babel.translation_directories)))
translations = [str(translation) for translation in babel.list_translations()]
if not "en" in translations:
    translations.append("en")
LOGGER.info(
    "Operating with the following translations available: " + " ".join(translations)
)

app.add_template_global(self_localized)


# Add context processor that will make additional variables
# and functions available in the template.
app.context_processor(make_utility_processor("survey"))


##
# Exception handler to capture all the unmanaged errors.
#
# @param e the Exception object, currently unused.
# @return flask-native response object carrying the error message
#         (and execution stack!).
@app.errorhandler(Exception)
def internal_error(e):
    return flask.render_template("survey-error.html.j2", message=str(e))

##
# Serve the /favicon.ico requests.
#
# @return the favicon.ico file.
@app.route("/favicon.ico")
def favicon():
    LOGGER.info("will look into: " + os.path.join(app.root_path, "static"))
    return flask.send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.ico",
    )


##
# Tell the backend to 'authorize' a tip; this means that
# the backend will allocate a certain amount to be later
# picked up by the wallet.
#
# @return the URL where to redirect the browser, in order
#         for the wallet to pick the tip up, or a error page
#         otherwise.
@app.route("/<lang>/submit-survey", methods=["POST"])
def submit_survey(lang):
    tip_spec = dict(
        amount=CURRENCY + ":1.0",
        next_url=os.environ.get("TALER_ENV_URL_INTRO", "https://taler.net/"),
        justification="Payment methods survey",
    )
    backend_resp = backend_post(
        INSTANCED_URL, "private/tips", tip_spec, auth_token=APIKEY
    )
    return flask.redirect(backend_resp["tip_status_url"])


##
# Serve the main index page, redirecting to /<lang>/
#
# @return response object of the index page.
@app.route("/")
def index():
    default = "en"
    target = flask.request.accept_languages.best_match(translations, default)
    return flask.redirect("/" + target + "/", code=302)


##
# Serve the internationalized main index page.
#
# @return response object of the index page.
@app.route("/<lang>/", methods=["GET"])
def start(lang):
    return flask.render_template(
        "survey-index.html.j2",
        merchant_currency=CURRENCY,
    )


@app.errorhandler(404)
def handler_404(e):
    return flask.render_template(
        "survey-error.html.j2",
        message=gettext("Page not found"),
    )


@app.errorhandler(405)
def handler_405(e):
    return flask.render_template(
        "survey-error.html.j2",
        message=gettext("HTTP method not allowed for this page"),
    )


@app.errorhandler(BackendException)
def handler_backend_exception(e):

    # The tip reserve was never created
    if e.backend_json.get("code") == 2753:
        t = flask.render_template(
            "survey-error-graceful.html.j2",
            message="Tip money were never invested, we are sorry!"
        )
        return flask.make_response(t, 500)

    # The tip reserve was never created
    if e.backend_json.get("code") == 2752:
        t = flask.render_template(
            "survey-error-graceful.html.j2",
            message="Tip money got all given, please return later!"
        )
        return flask.make_response(t, 500)


    t = flask.render_template(
        "survey-error.html.j2",
        message=e.args[0],
        json=e.backend_json,
        status_code=e.backend_status,
    )
    return flask.make_response(t, 500)
