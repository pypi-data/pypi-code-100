import json
import logging
import os
from pathlib import Path

import ruteni.plugins.auth
import ruteni.plugins.quotquot
from pkg_resources import resource_filename
from ruteni import STATICNS, configuration
from ruteni.app import WebApp
from ruteni.components import load_component_dir
from ruteni.plugins.pwa import Display, ProgressiveWebApp
from ruteni.plugins.security import ContentSecurityPolicy, set_security_headers
from ruteni.plugins.users import UserAccessMixin
from ruteni.utils.color import Color
from ruteni.utils.icon import PngIcon
from ruteni.utils.jinja2 import get_template_env
from ruteni.utils.locale import Locale, get_html_lang, get_locale_from_request
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response

logger = logging.getLogger(__name__)

# https://medium.com/@applification/progressive-web-app-splash-screens-80340b45d210

MANIFEST_NAME = "store.webmanifest"

app_store = ProgressiveWebApp(
    "store",
    1,
    manifest_name=MANIFEST_NAME,
    theme_color=Color("#2196f3"),
    background_color=Color("#2196f3"),
    display=Display.STANDALONE,
)


def get_resource(path: str) -> Path:
    return Path(resource_filename(__name__, "resources/" + path))


app_store.set_service_worker(get_resource("sw.js"))
app_store.set_resources(get_resource("resources.json"))

for size in (192, 512):
    name = f"images/icons/icon-{size}x{size}.png"
    icon = PngIcon(
        ns=app_store.static.ns,
        path=name,
        filename=configuration.static_dir / "store" / name,
        purpose="any maskable",
    )
    app_store.add_icon(icon)

app_store.add_i18n(
    Locale("en", "US"),
    full_name="Ruteni app store",
    short_name="app store",
    description="A simple app store",
    categories=["app", "store"],
)

app_store.add_i18n(
    Locale("fr", "FR"),
    full_name="Magasin d'applications de Ruteni",
    short_name="Magasin d'applications",
    description="Un magasin d'applications simple",
    categories=["applications", "magasin"],
)

template_dir = resource_filename(__name__, "templates")
template_env = get_template_env(Path(template_dir))

content_security_policy = ContentSecurityPolicy(
    connect=True, img=True, script=True, manifest=True
)


async def homepage(request: Request) -> Response:
    locale = get_locale_from_request(request, app_store.available_locales)
    i18n = app_store.i18ns[locale]
    params = dict(
        title=i18n.name,
        lang=get_html_lang(locale),
        manifest=MANIFEST_NAME,
        description=i18n.description,
        theme_color=app_store.theme_color,
        apple_touch_icon=app_store.icons[0].src,  # TODO: FIXME
    )
    homepage_template = template_env.get_template("index.j2")
    content = await homepage_template.render_async(params)
    return set_security_headers(HTMLResponse(content), content_security_policy)


app_store.add_route("", homepage)

configuration.add_static_resource_mount("store", __name__)


# list
async def list_apps(request: Request) -> Response:
    result: list = []
    for app in WebApp.all_apps:
        # ignore the app store itself
        if app is app_store:
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


app_store.api.add_route("list", list_apps)

logger.info("loaded")
