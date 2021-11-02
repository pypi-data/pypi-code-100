import click


GLOBAL_COMMON_OPTIONS = [
    click.option("--date", "-d", help="Datetime", default="now"),
    click.option("--lat", help="Observer latitude", required=False),
    click.option("--lon", help="Observer longitude", required=False),
    click.option(
        "--force-geoip",
        help="GeoIP information is cached for 1 day, this flag bypasses it.",
        is_flag=True,
    ),
    click.option("--json", "-j", help="Output JSON", is_flag=True),
]


def global_options(func):
    for option in reversed(GLOBAL_COMMON_OPTIONS):
        func = option(func)
    return func
