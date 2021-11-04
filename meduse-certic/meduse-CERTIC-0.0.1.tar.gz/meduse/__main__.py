import argh
from meduse import (
    serve,
    mirror,
    index,
)


def run_cli():
    parser = argh.ArghParser()
    parser.add_commands([serve, mirror, index])
    parser.dispatch()


if __name__ == "__main__":
    run_cli()
