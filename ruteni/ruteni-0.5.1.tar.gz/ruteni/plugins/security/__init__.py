import enum
import logging

import werkzeug
from ruteni import ROOTNS, configuration
from ruteni.api import WebApi
from ruteni.plugins.database import database, metadata
from ruteni.plugins.users import users
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Table, func
from sqlalchemy_utils.types.json import JSONType
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, Response
from starlette.routing import Route
from starlette.staticfiles import PathLike
from urlobject.path import URLPath

logger = logging.getLogger(__name__)

# https://scotthelme.co.uk/a-new-security-header-expect-ct/
EXPECT_CT_MAX_AGE: int = configuration.get(
    "RUTENI_SECURITY_EXPECT_CT_MAX_AGE", cast=int, default=60  # 86400  # 1 day
)

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
# https://hstspreload.org/
HSTS_MAX_AGE: int = configuration.get(
    "RUTENI_SECURITY_HSTS_MAX_AGE", cast=int, default=63072000  # 2 years
)

CSP_REPORT_CONTENT_TYPE = "application/csp-report"
EXPECT_CT_CONTENT_TYPE = "application/expect-ct-report+json"
CSP_REPORT_KEY = "csp-report"
EXPECT_CT_KEY = "expect-ct-report"


class ReportType(enum.Enum):
    CSP = 1
    EXPECT_CT = 2


security_reports = Table(
    "security_reports",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("type", Enum(ReportType), nullable=False),
    Column("user_id", Integer, ForeignKey(users.c.id), nullable=True),
    Column("report", JSONType, nullable=False),
    Column("timestamp", DateTime, nullable=False, server_default=func.now()),
)


async def csp_report(request: Request) -> Response:
    """
    {
        "csp-report": {
            "document-uri": "http://localhost:8000/app/store/",
            "referrer": "",
            "violated-directive": "script-src-elem",
            "effective-directive": "script-src-elem",
            "original-policy": "default-src 'self'; worker-src 'self'; frame-src 'none'; child-src 'none'; object-src 'none'; require-trusted-types-for 'script'; report-uri /api/logging/v1/csp-report/;",
            "disposition": "enforce",
            "blocked-uri": "inline",
            "line-number": 16,
            "source-file": "http://localhost:8000/app/store/",
            "status-code": 200,
            "script-sample": "",
        }
    }
    """
    body = await request.json()
    report = body[CSP_REPORT_KEY]  # TODO: have a marshmallow schema to validate report?
    content_type = request.headers["content-type"]
    if content_type != CSP_REPORT_CONTENT_TYPE:
        logger.warning(f"invalid csp-report content type {content_type}")
    logger.debug(report, request.headers)
    user_id = request.user.id if request.user.is_authenticated else None
    await database.execute(
        security_reports.insert().values(
            type=ReportType.CSP, user_id=user_id, report=report
        )
    )
    return JSONResponse(True)


async def expect_ct(request: Request) -> Response:
    """
    https://shaunc.com/blog/article/implementing-a-reporturi-endpoint-for-expectct-and-other-headers~Xdf4cU8EurV1
    https://www.tpeczek.com/2017/05/preparing-for-chromes-certificate.html
    {
        "expect-ct-report": {
            "date-time": "2017-05-05T12:45:00Z",
            "hostname": "example.com",
            "port": 443,
            "effective-expiration-date": "2017-05-05T12:45:00Z",
            ...
        }
    }
    """
    body = await request.json()
    report = body[EXPECT_CT_KEY]
    content_type = request.headers["content-type"]
    if content_type != EXPECT_CT_CONTENT_TYPE:
        logger.warning(f"invalid expect-ct content type {content_type}")
    user_id = request.user.id if request.user.is_authenticated else None
    await database.execute(
        security_reports.insert().values(
            type=ReportType.EXPECT_CT, user_id=user_id, report=report
        )
    )
    return JSONResponse(True)


api = WebApi("security", 1)
api.add_route("csp-report", csp_report, methods=["POST"], name="csp-report")
api.add_route("expect-ct", expect_ct, methods=["POST"], name="expect-ct")

CSP_REPORT_URI = api.url_for("csp-report")
EXPECT_CT_URI = api.url_for("expect-ct")


class ContentSecurityPolicy(werkzeug.datastructures.ContentSecurityPolicy):
    """
    https://csp.withgoogle.com/docs/strict-csp.html
    """

    def __init__(
        self,
        connect: bool = False,
        img: bool = False,
        manifest: bool = False,
        script: bool = False,
        style: bool = False,
        worker: bool = False,
    ) -> None:
        super().__init__()
        self.report_uri = CSP_REPORT_URI
        self.base_uri = "'none'"
        self.default_src = "'none'"
        if connect:
            self.connect_src = "'self'"
        if img:
            self.img_src = "'self'"
        if manifest:
            self.manifest_src = "'self'"
        if script:
            self.script_src = "'self'"
        if style:
            self.style_src = "'self'"
        if worker:
            self.worker_src = "'self'"

    def to_header(self) -> str:
        return (
            super().to_header()
            + "; require-trusted-types-for 'script'; trusted-types default dompurify"
        )


def set_security_headers(
    response: Response,
    content_security_policy: ContentSecurityPolicy,
    *,
    csp_report_only: bool = False,
) -> Response:
    """
    https://web.dev/csp-xss/
    https://flask.palletsprojects.com/en/2.0.x/security/
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
    https://github.com/shieldfy/API-Security-Checklist/blob/master/README.md
    https://mechlab-engineering.de/2019/01/security-testing-and-deployment-of-an-api-release-your-flask-app-to-the-internet/
    """
    hsts = f"max-age={HSTS_MAX_AGE}; includeSubDomains; preload"
    ect = f'max-age={EXPECT_CT_MAX_AGE}, enforce, report-uri="{EXPECT_CT_URI}"'

    headers = response.headers
    headers[
        "Content-Security-Policy-Report-Only"
        if csp_report_only
        else "Content-Security-Policy"
    ] = content_security_policy.to_header()
    headers["Strict-Transport-Security"] = hsts
    headers["Expect-CT"] = ect
    headers["X-Content-Type-Options"] = "nosniff"
    headers["X-Frame-Options"] = "deny"
    headers["X-XSS-Protection"] = "1; mode=block"
    headers["Access-Control-Allow-Methods"] = "GET"
    return response


def add_html_file_route(
    path: URLPath,
    filename: PathLike,
    content_security_policy: ContentSecurityPolicy,
    *,
    ns: URLPath = ROOTNS,
    media_type: str = None,
    name: str = None,
) -> Route:
    return configuration.add_route(
        path,
        lambda request: set_security_headers(
            FileResponse(filename, media_type=media_type), content_security_policy
        ),
        ns=ns,
        name=name,
        include_in_schema=False,
    )


configuration.add_static_resource_mount("security", __name__)

# TODO: add middleware that checks that csp header is set on html?

logger.info("loaded")
