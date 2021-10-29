import asyncio
import json
import logging
import os
import platform
import sys
import urllib.parse
from http import HTTPStatus
from pathlib import Path
from typing import List, Text, Optional, Dict, Any, Tuple

import aiohttp
import requests
from notebook.base.handlers import IPythonHandler
from pkg_resources import parse_version
from tornado.iostream import StreamClosedError

import jupyter_cogram
from jupyter_cogram.jupyter_cogram_serverextension.utils import (
    read_csv,
    append_to_log_file,
    save_token,
    read_config,
    save_config,
    merge_configs,
    bool_arg,
    track,
    get_random_uid,
    get_new_version_message,
    config_location,
    token_file_name,
    debug_mode,
)

if debug_mode:
    logging.basicConfig(level=logging.DEBUG)

logger: logging.Logger = logging.getLogger(__name__)

backend_url = os.environ.get("BACKEND_URL", "https://api.cogram.ai")
completions_enpdoint = os.environ.get("SUGGESTIONS_ENDPOINT", "completions")
package_pypi_url = "https://pypi.org/pypi/jupyter-cogram/json"
demo_mode = os.environ.get("DEMO_MODE", "false") == "true"

check_token_endpoint = "checkToken"

logger.debug(f"Backend URL: {backend_url}")
logger.debug(f"Suggestions endpoint: {completions_enpdoint}")
logger.debug(f"PyPI URL: {package_pypi_url}")

suggestions_timeout = float(os.environ.get("SUGGESTIONS_TIMEOUT", "10.0"))

LATEST_PYPI_VERSION: Optional[Text] = None
TELEMETRY_CONTEXT: Optional[Dict] = None
API_TOKEN: Optional[Text] = None
VERSION: Text = jupyter_cogram.__version__

logger.debug(f"Running jupyter-cogram version {VERSION}")


def fetch_token(loc: Path = config_location) -> Optional[Text]:
    loc = loc.absolute()
    fname = loc / token_file_name
    logger.debug(f"Checking for token at {fname}")
    if not fname.is_file():
        return None

    return fname.read_text().strip()


def post_auth_token(token: Text, log_launch: bool = False) -> requests.Response:
    url = urllib.parse.urljoin(backend_url, check_token_endpoint)
    payload = {
        "auth_token": token,
        "version": VERSION,
        "log_launch": log_launch,
    }
    logger.debug(f"Posting auth token to {url}. Payload: {payload}")
    return requests.post(url, json=payload)


def is_installation_up_to_date(
    pypi_url: Text = package_pypi_url,
) -> bool:
    logger.debug("Checking if local installation is up to date.")

    try:
        res = requests.get(pypi_url, timeout=2)
    except Exception as e:
        logger.exception(e)
        return True

    if res.status_code != 200:
        # we don't know, so let's return `True`
        return True

    global LATEST_PYPI_VERSION
    LATEST_PYPI_VERSION = res.json().get("info", {}).get("version")
    if not LATEST_PYPI_VERSION:
        # no version returned
        logger.debug("Could not find latest pypi version.")
        return True

    try:
        is_up_to_date = parse_version(VERSION) >= parse_version(LATEST_PYPI_VERSION)
        logger.debug(
            f"Have package version {VERSION}. "
            f"Latest PyPi version is {LATEST_PYPI_VERSION}. Installed version is up to "
            f"date: {is_up_to_date}."
        )
        return is_up_to_date
    except ValueError as e:
        logger.exception(e)
        return False


async def cogram_api_request(
    url: Text, payload: Optional[Dict] = None, headers: Optional[Dict] = None
) -> Tuple[Dict[Text, Any], int]:
    timeout = aiohttp.ClientTimeout(total=suggestions_timeout)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            return await resp.json(), resp.status


async def async_fetch_suggestion_code(
    queries,
    cell_contents: Optional[List[Text]] = None,
    auth_token: Optional[Text] = None,
    temperature: float = 0.2,
    n_suggestions: int = 3,
    prompt_presets: Text = "",
    language: Text = "python",
    url: Optional[Text] = None,
):
    logger.debug(f"Fetching code for query: {queries}")
    url = urllib.parse.urljoin(url if url else backend_url, completions_enpdoint)
    logger.debug(f"Submitting /completions request to API server: {url}")
    try:
        rjs, status_code = await cogram_api_request(
            url,
            payload={
                "queries": queries,
                "cell_contents": cell_contents or [],
                "auth_token": auth_token,
                "temperature": temperature,
                "n_suggestions": n_suggestions,
                "prompt_presets": prompt_presets,
                "language": language,
            },
        )

        if status_code >= 400:
            if rjs and rjs.get("error"):
                msg = rjs["error"]
            else:
                msg = "n/a"

            error_dict = {
                "status": "error",
                "error_msg": msg,
                "status_code": status_code,
            }

            raise ValueError(json.dumps(error_dict))

        return rjs
    except asyncio.TimeoutError:
        logger.error("Have Timeout")
        error_dict = {
            "status": "error",
            "error_msg": "Request timed out",
            "status_code": HTTPStatus.REQUEST_TIMEOUT,
        }
        logger.debug(f"Submitting error dict {json.dumps(error_dict)}")
        raise ValueError(json.dumps(error_dict))
    except StreamClosedError:
        raise


def get_telemetry_context() -> Dict[Text, Any]:
    global TELEMETRY_CONTEXT

    if not TELEMETRY_CONTEXT:
        TELEMETRY_CONTEXT = {
            "os": {"name": platform.system(), "version": platform.release()},
            "python": sys.version.split(" ")[0],
            "jupyter_cogram": VERSION,
        }

    return TELEMETRY_CONTEXT.copy()


class AsyncJupyterCogramHandler(IPythonHandler):
    def __init__(self, application, request, **kwargs):
        super(AsyncJupyterCogramHandler, self).__init__(application, request, **kwargs)
        self.task: Optional[asyncio.Task] = None

    def on_connection_close(self):
        if self.task:
            self.task.cancel()
            self.task = None

    async def post(self):
        data = json.loads(self.request.body)
        queries = data.get("queries", "")
        cell_contents = data.get("cell_contents", [])
        auth_token = data.get("auth_token", "'")
        temperature = float(data.get("temperature", "0.2"))
        n_suggestions = int(data.get("n_suggestions", "3"))
        prompt_presets = data.get("prompt_presets", "")
        language = data.get("language", "python")
        url = data.get("backend_url")

        try:

            suggestions_coro = async_fetch_suggestion_code(
                queries,
                cell_contents,
                auth_token,
                url=url,
                temperature=temperature,
                n_suggestions=n_suggestions,
                prompt_presets=prompt_presets,
                language=language,
            )

            self.task = asyncio.create_task(suggestions_coro)

            try:
                suggestions = await self.task
            except asyncio.CancelledError:
                return

            logger.debug(f"Have suggestions\n{json.dumps(suggestions, indent=2)}")
            if "choices" in suggestions and suggestions["choices"]:
                message = [
                    {"suggestion": c.get("text", ""), "imports": c.get("imports")}
                    for c in suggestions["choices"]
                ]
            else:
                message = None

            status = "success"
            status_code = 200
        except Exception as e:
            logger.error("Encountered error when submitting to API server.")
            try:
                error_dict = json.loads(str(e))
                status = error_dict["status"]
                message = error_dict["error_msg"]
                status_code = error_dict["status_code"]
            except Exception as e:
                logger.error(f"Unknown error: {e}")
                status_code = 400
                status = "Error"
                message = "Unknown error."

        response = {"status": status, "message": message}
        self.set_status(status_code)
        logger.debug(f"Returning response dict {json.dumps(response, indent=2)}")
        await self.finish(json.dumps(response))


class JupyterCogramTokenHandler(IPythonHandler):
    def __init__(self, application, request, **kwargs):
        super(JupyterCogramTokenHandler, self).__init__(application, request, **kwargs)

    def post(self):
        logger.debug(f"Receiving token Post!")
        data = json.loads(self.request.body)
        token = data.get("auth_token", "")

        post_token_response = post_auth_token(token)

        global API_TOKEN
        if post_token_response.status_code == 200:
            save_token(token)
            status = 200
            API_TOKEN = token
            response = {"status": status, "message": "Token saved."}
        else:
            API_TOKEN = None
            status = post_token_response.status_code
            response = post_token_response.json()
        logger.debug(f"Set API token to {API_TOKEN} -- received {token}")
        self.set_status(status)
        logger.debug(f"Returning response dict {json.dumps(response, indent=2)}")
        self.finish(json.dumps(response))

    def get(self):
        logger.debug(f"Receiving token fetch request")
        token = fetch_token()
        logger.debug(f"Have fetched token {token}")

        log_launch = bool_arg(self.request, "log_launch")

        response = None
        if token is not None:
            logger.debug(f"Checking if token is valid against API: {token}")
            response = post_auth_token(token, log_launch=log_launch)
            token_valid = response.status_code == 200
        else:
            token_valid = False

        global API_TOKEN
        if token_valid:
            API_TOKEN = token
            status = 200
            response = {
                "status": status,
                "message": "Token found.",
                "auth_token": token,
            }
        else:
            API_TOKEN = None
            status = response.status_code
            response = {
                "status": response.status_code,
                "error": response.json().get("error", "N/A"),
                "auth_token": None,
            }

        self.set_status(status)
        logger.debug(f"Returning response dict {json.dumps(response, indent=2)}")
        self.finish(json.dumps(response))


class JupyterCogramConfigHandler(IPythonHandler):
    def __init__(self, application, request, **kwargs):
        super(JupyterCogramConfigHandler, self).__init__(application, request, **kwargs)

    def get(self):
        self.set_status(200)
        response = {"demo_mode": demo_mode, **read_config()}
        logger.debug(f"Returning response dict {json.dumps(response, indent=2)}")
        self.finish(json.dumps(response))

    def put(self):
        data = json.loads(self.request.body)
        logger.debug(f"Receiving Config update: {data}")
        # noinspection PyBroadException
        try:
            merged_configs = merge_configs(data)
            save_config(merged_configs)
            self.set_status(200)
        except Exception as e:
            self.set_status(404)
            logger.error(f"Encountered error while updating config:{e}")

        self.finish(json.dumps({}))


class JupyterCogramEventHandler(IPythonHandler):
    def __init__(self, application, request, **kwargs):
        super(JupyterCogramEventHandler, self).__init__(application, request, **kwargs)

    def post(self):
        data = json.loads(self.request.body)
        logger.debug(f"Receiving event: {data}")
        name = data.get("name")
        props = data.get("properties")
        uid = API_TOKEN if API_TOKEN else get_random_uid()
        write_key = data.get("write_key")

        # noinspection PyBroadException
        try:
            track(write_key, uid, name, props, get_telemetry_context())
        except Exception as e:
            logger.error(f"Encountered error while tracking event:{e}")

        self.set_status(204)
        self.finish()


class JupyterCogramVersionHandler(IPythonHandler):
    def __init__(self, application, request, **kwargs):
        super(JupyterCogramVersionHandler, self).__init__(
            application, request, **kwargs
        )

    def get(self):
        logger.debug(f"Checking package version")
        is_up_to_date = is_installation_up_to_date()
        if is_up_to_date:
            status = 200
            message = (
                f"Installed version ({VERSION}) is up "
                f"to date with PyPI"
                f" version ({LATEST_PYPI_VERSION})."
            )
        else:
            status = 400
            message = (
                f"Installed version ({VERSION}) is **not** up "
                f"to date with PyPI "
                f"version ({LATEST_PYPI_VERSION})."
            )

        self.set_status(status)
        response = {
            "status": status,
            "message": message,
            "pypi_version": LATEST_PYPI_VERSION,
            "installed_version": VERSION,
        }
        logger.debug(f"Returning response dict {json.dumps(response, indent=2)}")
        self.finish(json.dumps(response))


def reload_module_and_update_version():
    from importlib import reload

    reload(jupyter_cogram)

    global VERSION

    VERSION = jupyter_cogram.__version__


class JupyterUpgradeCogramHandler(IPythonHandler):
    def __init__(self, application, request, **kwargs):
        super(JupyterUpgradeCogramHandler, self).__init__(
            application, request, **kwargs
        )

    def post(self):
        logger.debug(f"Receiving request to upgrade")
        import sys

        previous_version = VERSION
        logger.debug(f"Before upgrade, have jupyter-cogram version {previous_version}")
        cmd = f"{sys.executable} -m pip install -U jupyter-cogram"
        logger.debug(f"Running cmd {cmd}")
        status_code = os.system(cmd)

        # Updates global `VERSION` var
        reload_module_and_update_version()

        logger.debug(f"After upgrade, have jupyter-cogram version {VERSION}")

        if status_code == 0 and parse_version(VERSION) >= parse_version(
            previous_version
        ):
            status = 200
            response = {
                "status": "success",
                "message": "Library updated.",
                "new_version": VERSION,
            }
        else:
            status = 400
            response = {
                "status": "error",
                "message": "Could not upgrade library. Please check your "
                "Jupyter Notebook server logs. If you keep encountering "
                "the same problem, please reach out at support@cogram.ai",
                "new_version": LATEST_PYPI_VERSION,
            }

        self.set_status(status)
        logger.debug(f"Returning response dict {json.dumps(response, indent=2)}")
        self.finish(json.dumps(response))


class JupyterCogramLaunchHandler(IPythonHandler):
    def __init__(self, application, request, **kwargs):
        super(JupyterCogramLaunchHandler, self).__init__(application, request, **kwargs)

    def get(self):
        logger.debug(f"Receiving launch query.")

        log_content = read_csv()
        is_first_launch = log_content is None

        previous_version = log_content[-1][1] if log_content else None
        is_new_version = (
            parse_version(VERSION) > parse_version(previous_version)
            if previous_version
            else False
        )

        msg = None
        if is_first_launch:
            status = "first_launch"
            msg = (
                "Welcome to Cogram 👋 Get started by writing comments or code, "
                "and Cogram will generate suggestions when you hit the Tab key. "
                "Cogram will automatically generate suggestions for you if you've "
                "enabled \"Autosuggest\" (check the settings menu: ⚙️)."
            )
        elif is_new_version:
            status = "new_version"
            msg = get_new_version_message(parse_version(previous_version))
        else:
            status = "ok"

        append_to_log_file()

        self.set_status(200)
        response = {
            "status": status,
            "version": VERSION,
            "previous_version": previous_version,
            "msg": msg,
        }

        logger.debug(f"Returning response dict {json.dumps(response, indent=2)}")

        self.finish(json.dumps(response))
