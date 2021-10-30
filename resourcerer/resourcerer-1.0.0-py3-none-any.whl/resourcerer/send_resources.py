from .send_to_onedrive import send_to_onedrive
from .parse_yaml import get_yaml_obj
import glob
import os
import argparse


def close_resources(resources):
    def run(callback, section, source, target):
        for pattern in resources[section]:
            for filename in glob.glob(pattern):
                callback(
                    os.path.join(resources[source], filename).replace("\\", "/"),
                    os.path.join(resources[target], filename).replace("\\", "/")
                )
    return run


def main(default_file=".resources.yaml"):
    parser = argparse.ArgumentParser(description='Test automation wrapper')
    parser.add_argument('-f', '--file', type=str, help='Path to .kalash.yaml')
    args = parser.parse_args()

    if args.file:
        file = args.file
    else:
        file = default_file

    resources = get_yaml_obj(file)

    close_resources(resources)(
        send_to_onedrive,
        'uploadables',
        'source_folder',
        'target_folder'
    )


if __name__ == "__main__":
    main()
