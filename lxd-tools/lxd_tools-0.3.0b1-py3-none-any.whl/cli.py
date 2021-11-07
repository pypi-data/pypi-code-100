from argparse import ArgumentParser
from contextlib import closing

from pylxd import Client

from .resources import print_resources

__all__ = [
    'run_print_resources',
]


def run_print_resources():
    parser = ArgumentParser(description='Tool for displaying  LXD containers '
                                        'actual resources.')
    parser.add_argument('-e',
                        '--endpoint',
                        help='LXD endpoint to connect to.',
                        required=False,
                        default=None)
    parser.add_argument('-c',
                        '--cert-filepath',
                        help='LXD certificate file path to connect over '
                             'endpoint.',
                        required=False,
                        default=None)
    parser.add_argument('-k',
                        '--key-filepath',
                        help='LXD private key file path to connect over '
                             'endpoint.',
                        required=False,
                        default=None)
    parser.add_argument('--gib',
                        help='Print units in gibibytes.',
                        action='store_true',
                        default=False)

    args = parser.parse_args()

    client = Client(
        endpoint=args.endpoint,
        cert=None if (
            args.cert_filepath is None or args.key_filepath is None
        ) else (args.cert_filepath, args.key_filepath),
    )

    with closing(client.api.session):
        print_resources(client, args.gib)
