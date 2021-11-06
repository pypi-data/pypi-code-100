import json
import logging
import os
from pathlib import Path

import ruteni.plugins.auth
import ruteni.plugins.quotquot
from pkg_resources import resource_filename
from ruteni import configuration
from ruteni.app import WebApp
from ruteni.plugins.pwa import Display, ProgressiveWebApp
from ruteni.plugins.security import ContentSecurityPolicy, set_security_headers
from ruteni.plugins.users import UserAccessMixin
from ruteni.utils.color import Color
from ruteni.utils.icon import PngIcon
from ruteni.utils.locale import Locale, get_locale_from_request
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from ruteni import URLPath

logger = logging.getLogger(__name__)

# https://medium.com/@applification/progressive-web-app-splash-screens-80340b45d210

MANIFEST_NAME = "store.webmanifest"

store = ProgressiveWebApp(
    "store",
    1,
    theme_color=Color("#2196f3"),
    background_color=Color("#2196f3"),
    display=Display.STANDALONE,
)


def get_resource(path: str) -> Path:
    return Path(resource_filename(__name__, "resources/" + path))


store.set_service_worker(get_resource("sw.js"))
store.set_resources(get_resource("resources.json"))

for size in (192, 512):
    name = f"images/icons/icon-{size}x{size}.png"
    icon = PngIcon(
        ns=URLPath("/static/@ruteni/store/v1"),  # store.static.ns,
        path=name,
        filename=configuration.static_dir / "@ruteni/store/v1" / name,
        purpose="any maskable",
    )
    store.add_icon(icon)

store.add_i18n(
    Locale("en", "US"),
    full_name="Ruteni app store",
    short_name="app store",
    description="A simple app store",
    categories=["app", "store"],
)

store.add_i18n(
    Locale("fr", "FR"),
    full_name="Magasin d'applications de Ruteni",
    short_name="Magasin d'applications",
    description="Un magasin d'applications simple",
    categories=["applications", "magasin"],
)


content_security_policy = ContentSecurityPolicy(
    connect=True, img=True, script=True, manifest=True
)


async def homepage(request: Request) -> Response:
    module = "/static/@ruteni/store/v1/index.js"
    content = f"""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="{module}" type="module" defer></script>
  </head>
  <body></body>
</html>
"""
    return set_security_headers(HTMLResponse(content), content_security_policy)


store.add_route("", homepage)

configuration.add_static_resource_mount("store", __name__)


# list
async def list_apps(request: Request) -> Response:
    result: list = []
    for app in WebApp.all_apps:
        # ignore the app store itself
        if app is store:
            continue

        # if the app requires special access rights, check that the user statifies them
        if isinstance(app, UserAccessMixin) and not (
            request.user.is_authenticated and app.accessible_to(request.user.id)
        ):
            continue

        if isinstance(app, ProgressiveWebApp):
            locale = get_locale_from_request(request, app.available_locales)
            app_info = app.get_manifest(locale)
        else:
            app_info = dict(name=app.name)

        result.append(app_info)
    return JSONResponse(result)


store.api.add_route("list", list_apps)

logger.info("loaded")
