import sys
import argparse
import logging

from .exceptions import VkTokenError
from .util.export import Exporter
from .vk_api import VkApiSess
from .config import Default
from .get_token import get_access_token


def process_args(args, defaults):
    """
    Parse config/stdin arguments and set program entry point (phase).

    Args:
        defaults: Default settings from config file.
    """

    parser = argparse.ArgumentParser()
    parser.prog = 'vkinfo'
    subparsers = parser.add_subparsers()

    # Global arguments
    parser_base = argparse.ArgumentParser(add_help=False)
    parser_base.add_argument('--format', dest='export_format',
                             choices=['csv', 'json', 'tsv'],
                             type=str, default=defaults.EXPORT_FORMAT,
                             help=('export forman (default: %s)'
                                   % defaults.EXPORT_FORMAT))
    parser_base.add_argument('--path', dest='export_path',
                             type=str, default=defaults.EXPORT_PATH,
                             help=('export path (default: %s)'
                                   % defaults.EXPORT_PATH))
    parser_base.add_argument('--log-path', dest='log_path',
                             type=str, default=defaults.LOG_PATH,
                             help=('log file path (default: %s)'
                                   % defaults.LOG_PATH))
    parser_base.set_defaults(scope=defaults.SCOPE)
    parser_base.set_defaults(app_id=defaults.CLIENT_ID)
    parser_base.set_defaults(fields=defaults.FIELDS)
    parser_base.set_defaults(api_version=defaults.API_V)
    parser_base.set_defaults(base_url=defaults.BASE_URL)

    # access_token generation
    parser_token = subparsers.add_parser('token',
                                         parents=[parser_base],
                                         help='get vk access_token.')
    parser_token.set_defaults(phase='token')

    # runtime arguments
    parser_run = subparsers.add_parser('run',
                                       parents=[parser_base],
                                       help='run script.')
    parser_run.set_defaults(phase='run')
    parser_run.add_argument('access_token',
                            help='access token to use for requests',
                            type=str)
    parser_run.add_argument('user_id',
                            help='ID of searched user',
                            type=str)

    parameters = parser.parse_args(args)

    return parameters


def main(args=None):
    """Main function of a script.
    Parses arguments/tunes logging/controls general algorithm flow

    Args:
        args (list, optional): stdin arguments. Defaults to None.
    """
    if args is None:
        args = sys.argv[1:]

    parameters = process_args(args, Default)

    # setting logger levels.
    # info and above: displayed in console
    # debug and above: writes to log file
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s %(name)-5s %(levelname)-8s %(message)s',
        filename=parameters.log_path)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)-15s %(name)-5s %(levelname)-8s %(message)s'
    )
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    if parameters.phase == 'token':
        logging.info("Starting.. Phase: Token")
        get_access_token(parameters.app_id, parameters.scope)

    elif parameters.phase == 'run':
        logging.info("Starting.. Phase: Run")
        sess = VkApiSess(
            access_token=parameters.access_token,
            api_version=parameters.api_version,
            app_id=parameters.app_id,
            base_url=parameters.base_url
        )
        
        if not sess.token_validation():
            raise SystemExit('Your Token is not valid. It may be expired,\
                try getting a new one.')

        logging.info("Token ok")
        
        # get only friends count and ids for additional tests
        fids = sess.method_execute(
            method='friends.get',
            values={
                'user_id': parameters.user_id,
                'count': 10000}
        )

        fids_count = fids['count']

        if not fids_count:
            logging.debug('friendlist is empty. Exiting')
            
            raise SystemExit('User has no friends. Poor thing..')

        friends_df = sess.get_friends(
            fields=parameters.fields,
            search_user_id=parameters.user_id,
            fids_count=fids_count
        )
        

        logging.info("Creating Exporter")
        exporter = Exporter(friends_df)
        exporter.save(
            export_format=parameters.export_format,
            export_path=parameters.export_path
        )

if __name__ == '__main__':
    main()
