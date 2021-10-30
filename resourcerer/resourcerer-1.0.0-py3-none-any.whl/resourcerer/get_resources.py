from .get_from_onedrive import download_from_onedrive
from .parse_yaml import get_yaml_obj
import os
import argparse


def close_resources(resources):
    def run(callback, section, source, target):
        for filename in resources[section]:
            callback(
                os.path.join(resources[source], filename).replace("\\", "/"),
                resources[target]
            )
    return run


def main(default_file="resources.yaml"):
    parser = argparse.ArgumentParser(description='Test automation wrapper')
    parser.add_argument('-f', '--file', type=str, help='Path to .kalash.yaml')
    args = parser.parse_args()

    if args.file:
        file = args.file
    else:
        file = default_file

    resources = get_yaml_obj(file)

    close_resources(resources)(
        download_from_onedrive,
        'test_resources',
        'source_folder',
        'target_folder'
    )


if __name__ == "__main__":
    main()
