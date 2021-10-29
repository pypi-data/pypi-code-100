##
# This file is part of GNU TALER.
# Copyright (C) 2014-2016, 2020 Taler Systems SA
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
# @author Florian Dold
# @author Marcello Stanisci
# @brief Implementation of a donations site.

import base64
import logging
import flask
from flask import request
from flask_babel import Babel
from flask_babel import refresh
from flask_babel import force_locale
from flask_babel import gettext
import os
import time
import traceback
import urllib
from taler.util.talerconfig import TalerConfig, ConfigurationError
from urllib.parse import urljoin
from ..httpcommon import backend_post, backend_get, make_utility_processor, get_locale
import sys

if not sys.version_info.major == 3 and sys.version_info.minor >= 6:
    print("Python 3.6 or higher is required.")
    print(
        "You are using Python {}.{}.".format(
            sys.version_info.major, sys.version_info.minor
        )
    )
    sys.exit(1)

LOGGER = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = flask.Flask(__name__, template_folder="../templates", static_folder="../static")
app.debug = True
app.secret_key = base64.b64encode(os.urandom(64)).decode("utf-8")

TC = TalerConfig.from_env()
try:
    BACKEND_BASE_URL = TC["frontends"]["backend"].value_string(required=True)
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
app.context_processor(make_utility_processor("donations"))

##
# Return a error response to the client.
#
# @param abort_status_code status code to return along the response.
# @param params _kw_ arguments to passed verbatim to the templating engine.
def err_abort(abort_status_code, **params):
    t = flask.render_template("donations-error.html.j2", **params)
    flask.abort(flask.make_response(t, abort_status_code))


##
# Issue a GET request to the backend.
#
# @param endpoint the backend endpoint where to issue the request.
# @param params (dict type of) URL parameters to append to the request.
# @return the JSON response from the backend, or a error response
#         if something unexpected happens.
def backend_instanced_get(instance, endpoint, params):
    backend_url = urljoin(BACKEND_BASE_URL, f"instances/{instance}/")
    return backend_get(backend_url, endpoint, params, auth_token=APIKEY)


##
# POST a request to the backend, and return a error
# response if any error occurs.
#
# @param endpoint the backend endpoint where to POST
#        this request.
# @param json the POST's body.
# @return the backend response (JSON format).
def backend_instanced_post(instance, endpoint, json):
    backend_url = urljoin(BACKEND_BASE_URL, f"instances/{instance}/")
    return backend_post(backend_url, endpoint, json, auth_token=APIKEY)


##
# Inspect GET arguments in the look for a parameter.
#
# @param name the parameter name to lookup.
# @return the parameter value, or a error page if not found.
def expect_parameter(name):
    val = flask.request.args.get(name)
    if not val:
        return err_abort(400, message=gettext("parameter '{}' required").format(name))
    return val


##
# "Fallback" exception handler to capture all the unmanaged errors.
#
# @param e the Exception object, currently unused.
# @return flask-native response object carrying the error message
#         (and execution stack!).
@app.errorhandler(Exception)
def internal_error(e):
    return flask.render_template("donations-error.html.j2", message=str(e))

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
# Serve the main index page.
#
# @return response object of the index page.
@app.route("/<lang>/")
def start(lang):
    return flask.render_template("donations-index.html.j2", merchant_currency=CURRENCY)


##
# Serve the "/checkout" page.  This page lets the
# user pick the payment method they want to use,
# and finally confirm the donation.
#
# @return response object for the /checkout page.
@app.route("/<lang>/checkout", methods=["GET"])
def checkout(lang):
    amount = expect_parameter("donation_amount")
    donation_receiver = expect_parameter("donation_receiver")
    donation_donor = expect_parameter("donation_donor")
    return flask.render_template(
        "donations-checkout.html.j2",
        donation_amount=amount,
        donation_receiver=donation_receiver,
        donation_donor=donation_donor,
        merchant_currency=CURRENCY,
    )


##
# Serve the page advising the user about the impossibility
# of further processing the payment method they chose.
#
# @return response object about the mentioned impossibility.
@app.route("/<lang>/provider-not-supported")
def provider_not_supported(lang):
    return flask.render_template("donations-provider-not-supported.html.j2")


##
# POST the donation request to the backend.  In particular,
# it uses the "POST /order" API.
#
# @return response object that will redirect the browser to
#         the fulfillment URL, where all the pay-logic will
#         happen.
@app.route("/<lang>/donate")
def donate(lang):
    donation_receiver = expect_parameter("donation_receiver")
    donation_amount = expect_parameter("donation_amount")
    donation_donor = expect_parameter("donation_donor")
    payment_system = expect_parameter("payment_system")
    if payment_system != "taler":
        return flask.redirect(flask.url_for("provider_not_supported"))
    fulfillment_url = flask.url_for(
        "fulfillment",
        timestamp=str(time.time()),
        receiver=donation_receiver,
        lang=lang,
        _external=True,
    )
    fulfillment_url = fulfillment_url + "&order_id=${ORDER_ID}"
    order = dict(
        amount=donation_amount,
        extra=dict(
            donor=donation_donor, receiver=donation_receiver, amount=donation_amount
        ),
        fulfillment_url=fulfillment_url,
        summary="Donation to {}".format(donation_receiver),
        wire_transfer_deadline=dict(t_ms=1000 * int(time.time() + 15 * 30)),
    )
    order_resp = backend_instanced_post(
        donation_receiver, "private/orders", dict(order=order)
    )

    if not order_resp:
        return err_abort(
            500, # FIXME: status code got lost in the httpcommon module.
            message=gettext("Backend could not create the order")
        )

    order_id = order_resp["order_id"]
    return flask.redirect(
        flask.url_for(
            "fulfillment", receiver=donation_receiver, order_id=order_id, lang=lang
        )
    )


##
# Serve the fulfillment page.
#
# @param receiver the donation receiver name, that should
#        correspond to a merchant instance.
# @return after the wallet sent the payment, the final HTML "congrats"
#         page is returned; otherwise, the browser will be redirected
#         to a page that accepts the payment.
@app.route("/<lang>/donation/<receiver>")
def fulfillment(lang, receiver):
    order_id = expect_parameter("order_id")
    pay_status = backend_instanced_get(
        receiver, f"private/orders/{order_id}", params=dict()
    )
    order_status = pay_status.get("order_status")
    if order_status == "paid":
        extra = pay_status["contract_terms"]["extra"]
        return flask.render_template(
            "donations-fulfillment.html.j2",
            donation_receiver=extra["receiver"],
            donation_amount=extra["amount"],
            donation_donor=extra["donor"],
            order_id=order_id,
            currency=CURRENCY,
        )
    return flask.redirect(pay_status["order_status_url"])


@app.errorhandler(404)
def handler(e):
    return flask.render_template(
        "donations-error.html.j2", message=gettext("Page not found")
    )
