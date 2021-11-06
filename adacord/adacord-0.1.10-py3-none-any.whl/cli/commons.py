import csv
import json
from typing import Any, Dict, List
from pathlib import Path

CONFIG_FOLDER_PATH = Path.home() / ".adacord"


def save_auth(payload, base_path=CONFIG_FOLDER_PATH):
    Path(base_path).mkdir(exist_ok=True)
    with open(base_path / "auth.json", "w+") as f:
        f.write(json.dumps(payload))


def read_auth(base_path=CONFIG_FOLDER_PATH):
    with open(base_path / "auth.json", "r+") as f:
        return json.loads(f.read())


def get_token(base_path=CONFIG_FOLDER_PATH):
    auth = read_auth(base_path)
    return auth["token"]


def parse_csv(filepath: Path) -> List[Dict[str, Any]]:
    rows = []
    with filepath.open(encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)
        csvReader.fieldnames = [
            field.lower() for field in csvReader.fieldnames
        ]
        rows = [row for row in csvReader]
    return rows


def parse_json(filepath: Path) -> List[Dict[str, Any]]:
    with open(filepath) as f:
        rows = json.load(f)
    if isinstance(rows, dict):
        rows = [rows]
    return rows


def parse_jsonlines(filepath: Path) -> List[Dict[str, Any]]:
    rows = []
    with filepath.open("r") as f:
        for line in f:
            rows.append(json.loads(line))
    return rows
