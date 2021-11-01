import argparse
from pathlib import Path

from .generator import create_elasticsearch_in_dir


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Create elasticsearch.json using schema.json"
    )

    parser.add_argument("ids_dir", type=Path, help="Path to the IDS folder")

    args = parser.parse_args()

    create_elasticsearch_in_dir(args.ids_dir)
