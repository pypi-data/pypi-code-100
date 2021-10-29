from typing import Type

from gpx_renderer.renderer import Renderer
from gpx_renderer.renderer_not_found_error import RendererNotFoundError
from gpx_renderer.renderers.distance.matplotlib import MatplotLibDistanceRenderer
from gpx_renderer.renderers.distance.stdout import STDOUTDistanceRenderer
from gpx_renderer.renderers.time.matplotlib import MatplotLibTimeRenderer
from gpx_renderer.renderers.time.stdout import STDOUTTimeRenderer


class RendererFactory:
    RENDERERS: dict[str, dict[str, Type[Renderer]]] = {  # noqa: WPS115,WPS234
        "stdout": {
            "time": STDOUTTimeRenderer,
            "distance": STDOUTDistanceRenderer,
        },
        "matplot": {
            "time": MatplotLibTimeRenderer,
            "distance": MatplotLibDistanceRenderer,
        },
    }

    @staticmethod
    def renderer_from_string(  # noqa: WPS602
        renderer: str,
        aggregation: str,
        running: float,
        walking: float,
        destination: str,
    ) -> Renderer:
        if renderer not in RendererFactory.RENDERERS.keys():
            raise RendererNotFoundError(f"No such renderer {renderer}.")
        if aggregation not in RendererFactory.RENDERERS[renderer].keys():
            raise RendererNotFoundError(
                f"No such aggregation method {aggregation} for renderer {renderer}.",
            )
        return RendererFactory.RENDERERS[renderer][aggregation](
            running=running,
            walking=walking,
            destination=destination,
        )
