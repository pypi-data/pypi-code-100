import argparse

import pyftype


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("p", help="path")
    parser.add_argument(
        "-V", "--version", action="version", version=pyftype.__version__
    )

    args = parser.parse_args()
    kind = pyftype.guess(args.p)
    if kind:
        print(kind.ext)
    else:
        print("Unknown")


if __name__ == "__main__":
    main()
