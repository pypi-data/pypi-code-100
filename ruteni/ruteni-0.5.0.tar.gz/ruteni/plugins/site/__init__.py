from pkg_resources import resource_filename
from ruteni import configuration
from ruteni.static import WebStatic
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import FileResponse, Response


ABUSE_URL: str = configuration.get("RUTENI_VERIFICATION_ABUSE_URL")
SITE_NAME: str = configuration.get("RUTENI_SITE_NAME")
LOGO_PATH: str = configuration.get(
    "RUTENI_SITE_LOGO_PATH", default=resource_filename(__name__, "/resources/logo.svg")
)
FAVICON_PATH: str = configuration.get(
    "RUTENI_SITE_FAVICON_PATH",
    default=resource_filename(__name__, "/resources/favicon.ico"),
)

static = WebStatic("site", 1)
static.add_file_route("logo.svg", LOGO_PATH)


# TODO: use an Icon from ruteni.utils.icon


class Favicon(HTTPEndpoint):
    # favicon = b64decode(
    #     "AAABAAEAEBACAAEAAQBWAAAAFgAAAIlQTkcNChoKAAAADUlIRFIAAAAQAAAAEAgGAAAAH/P/"
    #     "YQAAAB1JREFUOI1j/P///38GCgATJZpHDRg1YNSAwWQAAGvKBByn4XVTAAAAAElFTkSuQmCC"
    # )
    async def get(self, request: Request) -> Response:
        return FileResponse(FAVICON_PATH, media_type="image/x-icon")
        # return Response(Favicon.favicon, media_type="image/x-icon")


configuration.add_route("/favicon.ico", Favicon)
