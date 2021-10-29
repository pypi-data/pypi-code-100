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
# @author Christian Grothoff
# @brief Minimal Website for the landing page.

import os
import re
import datetime
import base64
import logging
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
    get_locale,
    make_utility_processor,
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

LOGGER.info("Using translations from:" + ":".join(list(babel.translation_directories)))
translations = [str(translation) for translation in babel.list_translations()]
if not "en" in translations:
    translations.append("en")
LOGGER.info(
    "Operating with the following translations available: " + " ".join(translations)
)

# Add context processor that will make additional variables
# and functions available in the template.
app.context_processor(make_utility_processor("landing"))

##
# Exception handler to capture all the unmanaged errors.
#
# @param e the Exception object, currently unused.
# @return flask-native response object carrying the error message
#         (and execution stack!).
@app.errorhandler(Exception)
def internal_error(e):
    return flask.render_template(
        "landing-error.html.j2",
        message=gettext("Internal error"),
        stack=traceback.format_exc(),
    )


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

    if x := os.environ.get("TALER_ENV_URL_BANK"):
        bank_register_url = "/".join([x.strip("/"), f"{lang}/register"])
        bank_public_accounts_url = "/".join([x.strip("/"), f"{lang}/public-accounts"])
    else:
        bank_register_url = "#"
        bank_public_accounts_url = "#"

    if x := os.environ.get("TALER_ENV_URL_MERCHANT_BLOG"):
        merchant_blog_url = "/".join([x.strip("/"), lang])
    else:
        merchant_blog_url = "#"

    if x := os.environ.get("TALER_ENV_URL_MERCHANT_DONATIONS"):
        merchant_donations_url = "/".join([x.strip("/"), lang])
    else:
        merchant_donations_url = "#"

    if x := os.environ.get("TALER_ENV_URL_MERCHANT_SURVEY"):
        merchant_survey_url = "/".join([x.strip("/"), lang])
    else:
        merchant_survey_url = "#"

    return flask.render_template(
        "landing-index.html.j2",
        merchant_currency=CURRENCY,
        bank_register_url=bank_register_url,
        bank_public_accounts_url=bank_public_accounts_url,
        merchant_blog_url=merchant_blog_url,
        merchant_donations_url=merchant_donations_url,
        merchant_survey_url=merchant_survey_url,
    )


@app.errorhandler(404)
def handler_404(e):
    return flask.render_template(
        "landing-error.html.j2", message=gettext("Page not found")
    )


@app.errorhandler(405)
def handler_405(e):
    return flask.render_template(
        "landing-error.html.j2",
        message=gettext("HTTP method not allowed for this page"),
    )
