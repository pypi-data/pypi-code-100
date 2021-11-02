import argparse

from greport.greport import GReport


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="path of an XML file", required=True)
    parser.add_argument("-o", "--output", type=str, help="output file name", required=True)
    args = parser.parse_args()

    GReport(args.file).create_html(args.output)


if __name__ == '__main__':
    main()
