import base64
import csv
import json
import logging
import os
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Tuple, Text, Dict, Callable

import requests
from pkg_resources._vendor.packaging.version import Version
from tornado.httputil import HTTPServerRequest

import jupyter_cogram

config_location = Path().home() / ".ipython/nbextensions/jupyter-cogram"
log_file_name = "cogram_access_log"
token_file_name = "cogram_auth_token"
config_file = "cogram_config.json"

debug_mode = os.environ.get("DEBUG_MODE", "false") == "true"

if debug_mode:
    logging.basicConfig(level=logging.DEBUG)

logger: logging.Logger = logging.getLogger(__name__)


def read_csv(
    p: Path = config_location / log_file_name,
) -> Optional[List[Tuple[Text, Text]]]:
    if not p.is_file():
        logger.debug(f"'{p}' is not a file. Cannot read CSV.")
        return None

    out = []
    with p.open() as f:
        reader = csv.reader(f)
        for row in reader:
            k, v = row
            out.append((k, v))

    logger.debug(f"Successfully read CSV with {len(out)} entries.")
    return out


def create_log_file() -> None:
    p = config_location.absolute() / log_file_name
    if not p.is_file():
        logger.debug(f"Touching file '{p}'")
        p.touch()


def append_to_log_file() -> None:
    line = f"{datetime.now().isoformat()},{jupyter_cogram.__version__}"

    logger.debug(f"Appending to log file '{line}'")
    create_log_file()

    p = config_location.absolute() / log_file_name

    content = p.read_text()

    with p.open("a") as f:
        if not content:
            to_write = line
        else:
            to_write = f"\n{line}"

        f.write(to_write)


def save_token(token: Text, loc: Path = config_location) -> None:
    loc = loc.absolute()

    if not loc.is_dir():
        loc.mkdir(parents=True)

    p = loc / token_file_name

    logger.debug(f"Saving token '{token}' at path '{p}'.")
    p.write_text(token)


def read_config() -> Dict:
    p = config_location / config_file
    if p.is_file():
        with p.open() as f:
            return json.load(f)
    return {}


def save_config(d: Dict, loc: Path = config_location) -> None:
    loc = loc.absolute()

    if not loc.is_dir():
        loc.mkdir(parents=True)

    p = loc / config_file

    logger.debug(f"Saving config '{d}' at path '{p}'.")
    with p.open("w") as f:
        json.dump(d, f, indent=2)


def merge_configs(d: Dict) -> Dict:
    _config = read_config()
    _config.update(**d)
    return _config


def bool_arg(request: HTTPServerRequest, name: Text, default: bool = False) -> bool:
    args = request.query_arguments.get(name, [])
    if not args:
        return default

    arg = args[0]

    if isinstance(arg, (bytes, bytearray)):
        arg = arg.decode()

    return arg.lower() == "true"


def get_auth_header(key: Text) -> Dict[Text, Text]:
    key_with_colon = f"{key}:"
    _auth = base64.b64encode(key_with_colon.encode("utf-8")).decode("utf-8")
    return dict(Authorization=f"Basic {_auth}")


def run_in_thread(f: Callable, args: Tuple = (), kwargs: Optional[Dict] = None) -> None:
    logger.debug(f"Starting to run {f.__name__} in thread.")
    t = threading.Thread(target=f, args=args, kwargs=kwargs or {})
    t.start()


def track(
    key: Text, metrics_id: Text, event_name: Text, props: Dict, context: Dict
) -> None:
    props["metrics_id"] = metrics_id
    payload = dict(
        userId=metrics_id, event=event_name, properties=props, context=context
    )
    headers = {
        **get_auth_header(key),
        "Content-Type": "application/json",
    }
    logger.debug(f"Have payload:\n{json.dumps(payload, indent=2)}")
    run_in_thread(
        requests.post,
        args=("https://api.segment.io/v1/track",),
        kwargs=dict(headers=headers, json=payload, timeout=2),
    )


def get_random_uid(prefix: Text = "random-uid:", n_chars: int = 12) -> Text:
    import uuid

    return f"{prefix}{uuid.uuid4().hex[:n_chars]}"


def get_new_version_message(
    previous_version: Version,
) -> Optional[Text]:
    if previous_version.minor == 7:
        return (
            f"Welcome to your new Cogram version 👋 This version improves how you "
            f"can write code with Cogram: You can now generate code by writing a "
            f"Python "
            f"comment and hitting the Tab key, or by beginning a line of code and "
            f"completing with the Tab key."
        )
