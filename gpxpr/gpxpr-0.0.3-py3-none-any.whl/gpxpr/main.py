import sys

from gpx_parser.parser.gpx_file_parser import GPXFileParser
from gpx_renderer.factory import RendererFactory
from gpxpr.argparser import GPXPRArgParserFactory


def parse_and_render(argv: list[str]) -> None:
    argparser = GPXPRArgParserFactory.create_argparser(RendererFactory.RENDERERS.keys())
    arguments = argparser.parse_args(argv)
    parser = GPXFileParser(arguments.target)
    renderer = RendererFactory.renderer_from_string(
        renderer=arguments.renderer,
        aggregation=arguments.aggregation,
        running=arguments.running,
        walking=arguments.walking,
        destination=arguments.destination,
    )
    intervals = parser.parse()
    renderer.render(intervals)


def main() -> None:
    parse_and_render(sys.argv[1:])


if __name__ == "__main__":
    main()
