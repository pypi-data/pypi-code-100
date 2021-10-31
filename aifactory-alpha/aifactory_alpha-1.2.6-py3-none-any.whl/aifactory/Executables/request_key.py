from aifactory.Authentication import AFAuth
from aifactory.constants import SUBMISSION_DEFAULT_URL, AUTH_DEFAULT_URL


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--user-email', '-u', help='Example) random@aifactory.page',
                        default=None, dest='user_id')
    parser.add_argument('--auth-url', '-a', help='Example) http://auth.aifactory.solutions',
                        default=AUTH_DEFAULT_URL, dest='auth_url')
    args = parser.parse_args()
    auth = AFAuth(submit_key='dummy', auth_url=args.auth_url)
    auth.request_submit_key(user_id=args.user_id)

