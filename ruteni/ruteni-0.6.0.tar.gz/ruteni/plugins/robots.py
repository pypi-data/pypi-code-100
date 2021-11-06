from ruteni import configuration
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.endpoints import HTTPEndpoint


class Robots(HTTPEndpoint):
    robots_txt = "User-agent: *\nDisallow:"

    async def get(self, request: Request) -> Response:
        return PlainTextResponse(Robots.robots_txt)


configuration.add_route("/robots.txt", Robots)
