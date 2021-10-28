import enum
import json
import logging
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence, Union

from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError
from ruteni import EndpointTransform, configuration
from ruteni.app import WebApp
from ruteni.utils.color import Color
from ruteni.utils.icon import Icon
from ruteni.utils.locale import Locale, get_locale_from_request
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, Response
from urlobject.path import URLPath

logger = logging.getLogger(__name__)

# https://github.com/madskristensen/WebEssentials.AspNetCore.ServiceWorker/blob/master/src/Webmanifest/WebManifest.cs

WEBMANIFEST_MIME_TYPE = "application/manifest+json"
IMPORTMAP_MIME_TYPE = "application/importmap+json"


class IconSchema(Schema):
    src = fields.String(required=True)  # /static/store/images/icons/icon-144x144.png
    sizes = fields.String(required=True)  # 144x144
    type = fields.String(required=True)  # image/png
    # purpose = Enum(..., required=False)  monochrome maskable any


class InvalidManifest(Exception):
    pass


class ManifestSchema(Schema):
    """
    https://developer.mozilla.org/en-US/docs/Web/Manifest
    https://developers.google.com/web/fundamentals/web-app-manifest
    https://w3c.github.io/manifest/
    """

    background_color = fields.String(required=False)
    # categories = List(fields.String, required=False)
    description = fields.String(required=False)
    # dir = Enum(..., required=False)
    display = fields.String(required=False)
    # display_override
    # iarc_rating_id = fields.String(required=False)
    icons = fields.List(fields.Nested(IconSchema), required=True)
    lang = fields.String(required=False)
    name = fields.String(required=True)
    # orientation = Enum(..., required=False)
    # prefer_related_applications = Boolean(required=False)
    # protocol_handlers = Nested(..., required=False)
    # related_applications = Nested(required=False)
    scope = fields.String(required=False)
    # screenshots = Nested(..., required=False)
    # shortcuts = Nested(..., required=False)
    short_name = fields.String(required=False)
    start_url = fields.String(required=False)
    theme_color = fields.String(required=False)
    # splash_pages


def validate_manifest(manifest: Mapping) -> Mapping:
    schema = ManifestSchema()
    try:
        data = schema.load(manifest)
    except ValidationError:
        raise InvalidManifest()  # TODO: add parameters

    # TODO: the icon property must include a 192px and a 512px sized icons
    return data


def load_manifest(manifest_path: str) -> Mapping[str, Any]:
    with open(manifest_path) as f:  # TODO: async?
        return validate_manifest(json.load(f))


class RelatedApplication:
    def __init__(self, platform: str, id: str) -> None:
        self.platform = platform
        self.id = id

    def to_dict(self) -> dict:
        return dict(platform=self.platform, id=self.id)


class Display(enum.Enum):
    DISPLAY = "fullscreen"
    STANDALONE = "standalone"
    MINIMAL_UI = "minimal-ui"
    BROWSER = "browser"


class I18n:
    def __init__(
        self,
        *,
        full_name: Optional[str] = None,
        short_name: Optional[str] = None,
        description: Optional[str] = None,
        categories: Optional[Sequence[str]] = None,
    ):
        if not full_name and not short_name:
            raise ValueError("either full_name or short_name must be not empty")
        self.full_name = full_name
        self.short_name = short_name
        self.description = description
        self.categories = categories

    @property
    def name(self) -> str:
        if self.full_name is not None:
            return self.full_name
        else:
            assert self.short_name
            return self.short_name

    def to_dict(self) -> dict:
        result: dict[str, Union[str, Sequence[str]]] = dict()
        if self.full_name:
            result["name"] = self.full_name
        if self.short_name:
            result["short_name"] = self.short_name
        if self.description:
            result["description"] = self.description
        if self.categories:
            result["categories"] = self.categories
        return result


class ProgressiveWebApp(WebApp):
    """
    Manage a progressive web app
    https://web.dev/add-manifest/
    """

    def __init__(
        self,
        name: str,
        version: int,
        *,
        transform: Optional[EndpointTransform] = None,
        manifest_name: Optional[str] = None,
        resources_name: Optional[str] = None,
        sw_name: Optional[str] = None,
        scope: Optional[URLPath] = None,
        display: Optional[Display] = None,
        theme_color: Optional[Color] = None,
        background_color: Optional[Color] = None,
        prefer_related_applications: Optional[bool] = False,
    ) -> None:
        super().__init__(name, version, transform=transform)
        self.i18ns: dict[Locale, I18n] = {}
        self.icons: list[Icon] = []
        self.related_applications: list[RelatedApplication] = []
        self.manifest_name = manifest_name or f"{self.name}.webmanifest"
        self.resources_name = resources_name or "resources.json"
        self.sw_name = sw_name or "sw.js"
        self.scope = scope
        self.display = display
        self.theme_color = theme_color
        self.background_color = background_color
        self.prefer_related_applications = prefer_related_applications
        self.add_route(self.manifest_name, self.handle_manifest)

    @property
    def available_locales(self) -> Sequence[Locale]:
        return list(self.i18ns.keys())

    async def handle_manifest(self, request: Request) -> Response:
        locale = get_locale_from_request(request, self.available_locales)
        return JSONResponse(self.get_manifest(locale), media_type=WEBMANIFEST_MIME_TYPE)

    def set_service_worker(self, sw_path: Path) -> None:
        self.add_route(self.sw_name, lambda request: FileResponse(sw_path))
        self.add_route(  # TODO: fix
            self.sw_name + ".map", lambda request: FileResponse(str(sw_path) + ".map")
        )

    def set_resources(self, resources_path: Path) -> None:
        self.add_route(
            self.resources_name, lambda request: FileResponse(resources_path)
        )

    def add_icon(self, icon: Icon) -> None:
        self.icons.append(icon)
        self.static.add_route(icon.src, icon.handle_request)

    def add_i18n(
        self,
        locale: Locale,
        *,
        full_name: Optional[str] = None,
        short_name: Optional[str] = None,
        description: Optional[str] = None,
        categories: Optional[Sequence[str]] = None,
    ) -> None:
        self.i18ns[locale] = I18n(
            full_name=full_name,
            short_name=short_name,
            description=description,
            categories=categories,
        )

    def add_related_application(self, related_application: RelatedApplication) -> None:
        self.related_applications.append(related_application)

    def get_manifest(self, locale: Locale) -> dict:
        if locale not in self.i18ns:
            raise KeyError(f"unknown locale {locale}")

        # not sure where people got that some sizes are required
        # https://w3c.github.io/manifest/#icons-member
        # https://web.dev/installable-manifest/
        # https://stackoverflow.com/questions/48839338/
        if not any(icon.has("192x192") or icon.has("512x512") for icon in self.icons):
            raise ValueError("invalid icon list")

        result = dict(
            lang=str(locale),
            icons=[icon.to_dict() for icon in self.icons],
            start_url=str(self.ns),
            **self.i18ns[locale].to_dict(),
        )

        if self.display:
            result["display"] = self.display.value
        if self.theme_color:
            result["theme_color"] = self.theme_color
        if self.background_color:
            result["background_color"] = self.background_color
        if self.prefer_related_applications:
            result["prefer_related_applications"] = self.prefer_related_applications
        if self.related_applications:
            result["related_applications"] = [
                related_application.to_dict()
                for related_application in self.related_applications
            ]
        return result


configuration.add_static_resource_mount("pwa", __name__)

logger.info("loaded")
