from aifactory.API import AFContest

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--key_path', '-p', help='Example) my_key.afk', default=None, dest='submit_key_path')
    parser.add_argument('--key', '-k', help='Example) 1234567somerandomekey7654321', default=None, dest='submit_key')
    parser.add_argument('--file', '-f', nargs='+', help='Example) answer.csv', dest='file')
    parser.add_argument('--debug', '-d', type=bool, help='Example) False', default=True, dest='debug')
    parser.add_argument('--submit_url', help='Example) http://submit.aifactory.solutions',
                        default=SUBMISSION_DEFAULT_URL, dest='submit_url')
    parser.add_argument('--log_dir', help='Example) http://auth.aifactory.solutions',
                        default="./log", dest='log_dir')
    args = parser.parse_args()
    if args.debug:
        submit_key_path = './sample_data/my_key.afk'
        files = ['./sample_data/sample_answer.csv'] if args.file is None else args.file
        c = AFContest(submit_key_path=submit_key_path, debug=args.debug,
                      submit_url=args.submit_url, log_dir=args.log_dir)
        c.summary()
        c.submit(files[0])
    else:
        c = AFContest(submit_key_path=submit_key_path, submit_key=submit_key, debug=args.debug,
                      submit_url=args.submit_url, log_dir=args.log_dir)
        c.summary()
        c.submit(args.file[0])