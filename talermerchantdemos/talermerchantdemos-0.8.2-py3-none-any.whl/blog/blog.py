##
# This file is part of GNU Taler.
# Copyright (C) 2014-2020 Taler Systems SA
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
# @brief Implementation of a Taler-compatible blog.

import urllib.parse
import logging
import os
import traceback
import uuid
import base64
import flask
from flask import request
from flask_babel import Babel
from flask_babel import refresh
from flask_babel import force_locale
from flask_babel import gettext
import time
import sys
from urllib.parse import urljoin, urlencode, urlparse
from taler.util.talerconfig import TalerConfig, ConfigurationError
from ..blog.content import ARTICLES, get_article_file, get_image_file
from talermerchantdemos.httpcommon import (
    backend_get,
    backend_post,
    self_localized,
    Deadline,
    BackendException,
    make_utility_processor,
    get_locale,
)


def err_abort(abort_status_code, **params):
    """
    Return a error response to the client.

    @param abort_status_code status code to return along the response.
    @param params _kw_ arguments to passed verbatim to the templating engine.
    """
    t = flask.render_template("blog-error.html.j2", **params)
    flask.abort(flask.make_response(t, abort_status_code))


def refundable(pay_status):
    refunded = pay_status.get("refunded")
    refund_deadline = pay_status.get("contract_terms", {}).get("refund_deadline")
    assert refunded != None and refund_deadline
    t_ms = refund_deadline.get("t_ms")
    assert t_ms
    rd = Deadline(t_ms)
    if not refunded and not rd.isExpired():
        return True
    return False


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
    BACKEND_BASE_URL = TC["frontends"]["backend"].value_string(required=True)
    CURRENCY = TC["taler"]["currency"].value_string(required=True)
    APIKEY = TC["frontends"]["backend_apikey"].value_string(required=True)
except ConfigurationError as ce:
    print(ce)
    exit(1)

ARTICLE_AMOUNT = CURRENCY + ":0.5"
BACKEND_URL = urljoin(BACKEND_BASE_URL, "instances/blog/")

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
app.context_processor(make_utility_processor("blog"))


##
# "Fallback" exception handler to capture all the unmanaged errors.
#
# @param e the Exception object, currently unused.
# @return flask-native response object carrying the error message
#         (and execution stack!).
@app.errorhandler(Exception)
def internal_error(e):
    return flask.render_template(
        "blog-error.html.j2",
        message=gettext("Internal error"),
        stack=traceback.format_exc(),
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
# Serve the main index page for a particular language.
#
# @return response object of the index page.
@app.route("/<lang>/")
def start(lang):
    if lang in ARTICLES:
        translated = ARTICLES[lang]
    else:
        translated = {}
    return flask.render_template(
        "blog-index.html.j2",
        merchant_currency=CURRENCY,
        articles=translated.values(),
    )


@app.route("/<lang>/confirm-refund/<order_id>", methods=["GET"])
def confirm_refund(lang, order_id):
    session_id = flask.session.get("session_id", "")
    pay_status = backend_get(
        BACKEND_URL,
        f"private/orders/{order_id}",
        params=dict(session_id=session_id),
        auth_token=APIKEY,
    )
    order_status = pay_status.get("order_status")
    if order_status != "paid":
        err_abort(
            400,
            message=gettext("Cannot refund unpaid article"),
        )
    article_name = pay_status["contract_terms"]["extra"]["article_name"]

    if not refundable(pay_status):
        return flask.render_template(
            "blog-error.html.j2",
            message=gettext("Article is not anymore refundable"),
        )
    return flask.render_template(
        "blog-confirm-refund.html.j2",
        article_name=article_name,
        order_id=order_id,
    )


##
# Triggers the refund by serving /refund/test?order_id=XY.
# Will be triggered by a "refund button".
#
# @param order_id the order ID of the transaction to refund.
# @return the following errors (named by HTTP response code):
#         - 400: order unknown
#         - 402: the refund was asked on an unpaid article.
#         - 302: in the successful case, a redirection to the
#           "refund URL" is returned; then the wallet will run
#           the refund protocol in a transparent way.
@app.route("/refund/<order_id>", methods=["POST"])
def refund(order_id):
    if not order_id:
        return flask.jsonify(dict(error="Aborting refund: order unknown")), 400
    session_id = flask.session.get("session_id", "")
    pay_status = backend_get(
        BACKEND_URL,
        f"private/orders/{order_id}",
        params=dict(session_id=session_id),
        auth_token=APIKEY,
    )
    order_status = pay_status.get("order_status")

    if order_status != "paid":
        err_abort(
            402,
            message=gettext("You did not pay for this article (nice try!)"),
            json=pay_status,
        )
    if not refundable(pay_status):
        err_abort(
            403, message=gettext("Item not refundable (anymore)"), json=pay_status
        )
    refund_spec = dict(reason="Demo reimbursement", refund=ARTICLE_AMOUNT)
    backend_post(
        BACKEND_URL, f"private/orders/{order_id}/refund", refund_spec, auth_token=APIKEY
    )
    return flask.redirect(pay_status["order_status_url"])


##
# Render the article after a successful purchase.
#
# @param article_name _slugged_ (= spaces converted to underscores) article title.
# @param lang language the article is to be in
# @param data image filename to return along the article.
# @param order_id the ID of the order where this article got purchased.
#        (Will be put in the refund-request form action, since any article
#         will also have a "refund button" aside.)
# @return the following errors (named by HTTP return code):
#         - 500: file for article not found.
#         - 404: supplemental @a data not found.
#         In the successful case, a response object carrying the
#         article in it will be returned.
def render_article(article_name, lang, data, order_id, refundable):
    article_info = ARTICLES[lang].get(article_name)
    if article_info is None:
        m = gettext("Internal error: Files for article ({}) not found.").format(
            article_name
        )
        err_abort(500, message=m)
    if data is not None:
        if data in article_info.extra_files:
            return flask.send_file(get_image_file(data))
        m = gettext("Supplemental file ({}) for article ({}) not found.").format(
            data, article_name
        )
        err_abort(404, message=m)
    # the order_id is needed for refunds
    article_contents = open(get_article_file(article_info)).read()
    return flask.render_template(
        "blog-article-frame.html.j2",
        article_contents=article_contents,
        article_name=article_name,
        order_id=order_id,
        refundable=refundable,
    )


##
# Setup a fresh order with the backend.
#
# @param article_name which article the order is for
# @param lang which language to use
#
def post_order(article_name, lang):
    name_decoded = urllib.parse.unquote(article_name).replace("_", " ")
    summary = f"Essay: {name_decoded}"
    order = dict(
        amount=ARTICLE_AMOUNT,
        extra=dict(article_name=article_name),
        fulfillment_url=flask.request.base_url,
        public_reorder_url=flask.request.base_url,
        summary=summary,
        # FIXME: add support for i18n of summary!
        # 10 minutes time for a refund
        wire_transfer_deadline=dict(t_ms=1000 * int(time.time() + 15 * 30)),
    )
    order_resp = backend_post(
        BACKEND_URL,
        "private/orders",
        dict(order=order, refund_delay=dict(d_ms=1000 * 120)),
        auth_token=APIKEY,
    )
    return order_resp


##
# Trigger a article purchase.  The logic follows the main steps:
#
# 1. Always check if the article was paid already, via the
#    "/private/orders/$ORDER_ID" API from the backend.
# 2. If so, return the article.
# 3. If not, redirect the browser to a page where the
#    wallet will initiate the payment protocol.
#
# @param article_name (slugged) article title.
# @param data filename of a supplement data (image/sound/..)
# @return the following errors might occur (named by HTTP response code):
#         - 402: @a article_name does not correspond to the @a order_id
#                of a PAYED article.
#         - 500: neither the article was paid, nor a payment was triggered.
#         - 400: a invalid order_id was passed along the GET parameters.
#         In the successful case, either the article is returned, or
#         the browser gets redirected to a page where the wallet can
#         send the payment.
@app.route("/<lang>/essay/<article_name>")
@app.route("/<lang>/essay/<article_name>/data/<data>")
@app.route("/essay/<article_name>/data/<data>")
def article(article_name, lang=None, data=None):
    # We use an explicit session ID so that each payment (or payment replay) is
    # bound to a browser.  This forces re-play and prevents sharing the article
    # by just sharing the URL.
    session_id = flask.session.get("session_id")
    order_id = flask.request.cookies.get("order_id")

    if not session_id:
        session_id = flask.session["session_id"] = str(uuid.uuid4())
        order_id = None
    ##
    # First-timer; generate order first.
    if not order_id:
        if not lang:
            err_abort(403, message=gettext("Direct access forbidden"))
        order_resp = post_order(article_name, lang)
        order_id = order_resp["order_id"]

    # Ask the backend for the status of the payment
    pay_status = backend_get(
        BACKEND_URL,
        f"private/orders/{order_id}",
        params=dict(session_id=session_id),
        auth_token=APIKEY,
    )
    order_status = pay_status.get("order_status")
    if order_status == "claimed":
        if not lang:
            err_abort(403, message=gettext("Direct access forbidden"))
        # Order already claimed, must setup fresh order
        order_resp = post_order(article_name, lang)
        order_id = order_resp["order_id"]
        pay_status = backend_get(
            BACKEND_URL,
            f"private/orders/{order_id}",
            params=dict(session_id=session_id),
            auth_token=APIKEY,
        )
        order_status = pay_status.get("order_status")
        # This really must be 'unpaid' now...

    if order_status == "paid":
        refunded = pay_status["refunded"]
        if refunded:
            return flask.render_template(
                "blog-article-refunded.html.j2",
                article_name=article_name,
                order_id=order_id,
            )
        response = render_article(
            article_name, lang, data, order_id, refundable(pay_status)
        )
        return response

    # Check if the customer came on this page via the
    # re-purchase detection mechanism
    ai = pay_status.get("already_paid_order_id")
    au = pay_status.get("already_paid_fulfillment_url")
    if ai is not None and au is not None:
        response = flask.redirect(au)
        response.set_cookie(
            "order_id", ai, path=urllib.parse.quote(f"/essay/{article_name}")
        )
        response.set_cookie(
            "order_id", ai, path=urllib.parse.quote(f"/{lang}/essay/{article_name}")
        )
        return response

    # Redirect the browser to a page where the wallet can
    # run the payment protocol.
    response = flask.redirect(pay_status["order_status_url"])
    response.set_cookie("order_id", order_id, path=f"/essay/{article_name}")
    response.set_cookie("order_id", order_id, path=f"/{lang}/essay/{article_name}")
    return response


@app.errorhandler(500)
def handler_500(e):
    return flask.render_template(
        "blog-error.html.j2",
        message=gettext("Internal server error"),
    )


@app.errorhandler(404)
def handler_404(e):
    return flask.render_template(
        "blog-error.html.j2",
        message=gettext("Page not found"),
    )


@app.errorhandler(BackendException)
def handler_backend_exception(e):
    t = flask.render_template(
        "blog-error.html.j2",
        message=e.args[0],
        json=e.backend_json,
        status_code=e.backend_status,
    )
    return flask.make_response(t, 500)
