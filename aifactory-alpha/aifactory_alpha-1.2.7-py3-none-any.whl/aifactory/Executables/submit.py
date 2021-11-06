from aifactory.AFAPIClient import AFCompetition
from aifactory.constants import SUBMISSION_DEFAULT_URL, AUTH_DEFAULT_URL

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--key-path', '-p', help='Example) my_key.afk', default=None, dest='submit_key_path')
    parser.add_argument('--key', '-k', help='Example) 1234567somerandomekey7654321', default=None, dest='submit_key')
    parser.add_argument('--file', '-f', nargs='+', help='Example) answer.csv', dest='file')
    parser.add_argument('--debug', '-d', type=bool, help='Example) False', default=False, dest='debug')
    parser.add_argument('--submit-url', help='Example) http://submit.aifactory.solutions',
                        default=SUBMISSION_DEFAULT_URL, dest='submit_url')
    parser.add_argument('--log-dir', help='Example) ./log', default="./log", dest='log_dir')
    args = parser.parse_args()

    api_call_client = AFCompetition(submit_key_path=args.submit_key_path, submit_key=args.submit_key,
                                debug=args.debug, submit_url=args.submit_url, log_dir=args.log_dir)
    api_call_client.summary()
    api_call_client.submit(args.file[0])
