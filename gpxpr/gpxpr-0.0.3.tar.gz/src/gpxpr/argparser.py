import argparse
from typing import KeysView


class GPXPRArgParserFactory:
    @staticmethod
    def create_argparser(  # noqa: WPS602,WPS605
        available_renderers: KeysView[str],
    ) -> argparse.ArgumentParser:
        argparser = argparse.ArgumentParser()
        argparser.add_argument(
            "-r",
            "--renderer",
            required=True,
            type=str,
            help=f"Renderer to use [{', '.join(available_renderers)}]",  # noqa: WPS237
            action="store",
            dest="renderer",
        )
        argparser.add_argument(
            "-w",
            "--min-walking-speed",
            required=True,
            type=float,
            help="Slowest min/km where a runner is considered 'walking'",
            action="store",
            dest="walking",
        )
        argparser.add_argument(
            "-v",
            "--min-running-speed",
            required=True,
            type=float,
            help="Slowest min/km when a runner is considered 'running'",
            action="store",
            dest="running",
        )
        argparser.add_argument(
            "-a",
            "--aggregation-value",
            required=True,
            choices=["time", "distance"],
            type=str,
            help="Value to base the aggregation on",
            action="store",
            dest="aggregation",
        )
        argparser.add_argument(
            "-o",
            "--output",
            required=False,
            type=str,
            help="Output location. Default is /dev/stdout",
            action="store",
            dest="destination",
        )
        argparser.add_argument(
            "target",
            type=str,
            help="File to process",
            action="store",
        )
        return argparser
