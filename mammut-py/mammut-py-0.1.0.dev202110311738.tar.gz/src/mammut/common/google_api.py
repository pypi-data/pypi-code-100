# coding=utf-8
import dbm
import logging
from datetime import datetime
from enum import Enum
from typing import List, TypeVar, Callable, Optional, Any

from googleapiclient.errors import HttpError
from pkg_resources import resource_filename
import struct
from urllib import request, parse
from time import sleep
from urllib.error import HTTPError

import io
import os
import httplib2

from oauth2client.tools import argparser
from oauth2client import client
from oauth2client import tools
from oauth2client import service_account

from oauth2client.file import Storage
from apiclient import discovery

from googleapiclient.http import MediaIoBaseDownload

import mammut
from mammut.common.util import get_datetime_from_rfc3339
from mammut.common import GOOGLE_API_AUTH_LOCAL_WEBSERVER
from mammut.common import GOOGLE_API_AUTH_LOCAL_CREDENTIAL


logger = logging.getLogger()


_FuncT = TypeVar("_FuncT")


class GoogleAPIOpType(Enum):
    READ = "Read"
    WRITE = "Write"
    NGRAM = "Ngram"


class GoogleAPI:
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/presentations.readonly",
    ]
    CLIENT_SECRET_FILE = "GoogleSheetsMammutEdilmoCredentials.json"
    SERVICE_ACCOUNT_SECRET_FILE = "mammut-devops-cicd.json"
    APPLICATION_NAME = "Mammut"
    slides_metadata_re_string = "(sheet-id|Sheet-id|SHEET-ID)[ ]*->[ ]*([a-zA-Z0-9-_]+)"
    # List of last operations of the same type executions.
    # The list will never have more than the limit.
    READ_EXECUTIONS_TIME_LIST: List[datetime] = [
        mammut.get_timezone_aware_datetime_now()
    ]
    WRITE_EXECUTIONS_TIME_LIST: List[datetime] = [
        mammut.get_timezone_aware_datetime_now()
    ]
    NGRAM_EXECUTIONS_TIME_LIST: List[datetime] = [
        mammut.get_timezone_aware_datetime_now()
    ]
    EXECUTIONS_TIME_LIST = {
        GoogleAPIOpType.READ: READ_EXECUTIONS_TIME_LIST,
        GoogleAPIOpType.WRITE: WRITE_EXECUTIONS_TIME_LIST,
        GoogleAPIOpType.NGRAM: NGRAM_EXECUTIONS_TIME_LIST,
    }
    # Max amount of operations of the same type per time limit
    READ_EXECUTION_LIMIT: int = 100
    WRITE_EXECUTION_LIMIT: int = 100
    NGRAM_EXECUTION_LIMIT: int = 10
    EXECUTION_LIMIT = {
        GoogleAPIOpType.READ: READ_EXECUTION_LIMIT,
        GoogleAPIOpType.WRITE: WRITE_EXECUTION_LIMIT,
        GoogleAPIOpType.NGRAM: NGRAM_EXECUTION_LIMIT,
    }
    # Time spam for max amount of continues operations of the same type in seconds
    READ_EXECUTION_TIME_LIMIT: int = 100
    WRITE_EXECUTION_TIME_LIMIT: int = 100
    NGRAM_EXECUTION_TIME_LIMIT: int = 1
    EXECUTION_TIME_LIMIT = {
        GoogleAPIOpType.READ: READ_EXECUTION_TIME_LIMIT,
        GoogleAPIOpType.WRITE: WRITE_EXECUTION_TIME_LIMIT,
        GoogleAPIOpType.NGRAM: NGRAM_EXECUTION_TIME_LIMIT,
    }
    # Max amount of retries
    MAX_READ_RETRIES: int = 100
    MAX_WRITE_RETRIES: int = 100
    MAX_NGRAM_RETRIES: int = 100
    MAX_RETRIES = {
        GoogleAPIOpType.READ: MAX_READ_RETRIES,
        GoogleAPIOpType.WRITE: MAX_WRITE_RETRIES,
        GoogleAPIOpType.NGRAM: NGRAM_EXECUTION_TIME_LIMIT,
    }
    # Min delay in seconds
    MIN_API_OP_DELAY: float = 1.50
    # Ratio of EXECUTION_TIME_LIMIT to wait after a failure
    EXECUTION_TIME_LIMIT_PROPORTION = 0.3
    CREDENTIALS = None
    SHEETS_SERVICE = None
    DRIVE_SERVICE = None
    SLIDES_SERVICE = None
    IS_AUTHENTICATED = False

    @classmethod
    def ensure_credentials(cls, func: Callable[[_FuncT], _FuncT]):
        def wrapped(*args, **kwargs):
            cls.get_credentials()
            return func(*args, **kwargs)

        return wrapped

    @classmethod
    def ensure_credentials_and_read_limits(cls, func: Callable[[_FuncT], _FuncT]):
        return cls._get_wrapped(func, GoogleAPIOpType.READ)

    @classmethod
    def ensure_credentials_and_write_limits(cls, func: Callable[[_FuncT], _FuncT]):
        return cls._get_wrapped(func, GoogleAPIOpType.WRITE)

    @classmethod
    def ensure_credentials_and_ngram_limits(cls, func: Callable[[_FuncT], _FuncT]):
        return cls._get_wrapped(func, GoogleAPIOpType.NGRAM, 0.0)

    @classmethod
    def _get_wrapped(
        cls,
        func: Callable[[_FuncT], _FuncT],
        op_type: GoogleAPIOpType,
        suppress_exception_value: Optional[Any] = None,
    ):
        def is_exceeded_quote_error(http_error: Exception) -> bool:
            res = False
            if isinstance(http_error, HttpError):
                res = str(http_error.resp.status) == "429"
            elif isinstance(http_error, HTTPError):
                res = http_error.code == 429
            if not res:
                http_error_str = str(http_error).lower()
                res = "quota exceeded" in http_error_str
            return res

        def wrapped(*args, **kwargs):
            cls.get_credentials()
            retries = 0
            result = None
            while result is None:
                cls._check_exec_limit(op_type)

                try:
                    result = func(*args, **kwargs)
                except (HttpError, HTTPError) as http_error:
                    result = None
                    if is_exceeded_quote_error(http_error):
                        retries += 1
                        if retries > cls.MAX_RETRIES[op_type]:
                            mess = "Max amount of google read retries reached"
                            logger.error(mess)
                            raise RuntimeError(mess)
                        else:
                            # If we got an exception is because we didn't wait long enough
                            sleep(
                                cls.EXECUTION_TIME_LIMIT[op_type]
                                * cls.EXECUTION_TIME_LIMIT_PROPORTION
                                * retries
                            )
                            logger.debug(
                                f"Retrying google read operation: {retries}/{cls.MAX_RETRIES[op_type]}"
                            )
                    else:
                        logger.error(
                            f"Unexpected Http Error in read operation: {func.__name__} - Args: {args} - {kwargs}",
                            exc_info=True,
                        )
                        if suppress_exception_value is not None:
                            result = suppress_exception_value
                        else:
                            raise http_error
                except Exception as ex:
                    logger.error(
                        "Unexpected Error in read operation: {func.__name__} - Args: {args} - {kwargs}",
                        exc_info=True,
                    )
                    if suppress_exception_value is not None:
                        result = suppress_exception_value
                    else:
                        raise ex
                finally:
                    current_time: datetime = mammut.get_timezone_aware_datetime_now()
                    cls.EXECUTIONS_TIME_LIST[op_type].append(current_time)
            return result

        return wrapped

    @classmethod
    def get_credentials(cls):
        if not cls.IS_AUTHENTICATED:
            flgs_args = []
            if GOOGLE_API_AUTH_LOCAL_WEBSERVER:
                flgs_args.append("--noauth_local_webserver")
            flags = argparser.parse_args(flgs_args)
            credential_dir = os.getcwd()
            if not GOOGLE_API_AUTH_LOCAL_CREDENTIAL:
                home_dir = os.path.expanduser("~")
                credential_dir = os.path.join(home_dir, ".credentials")
                if not os.path.exists(credential_dir):
                    os.makedirs(credential_dir)
            credential_path = os.path.join(
                credential_dir, "sheets.googleapis.com-python-mammut.json"
            )
            store = Storage(credential_path)
            credentials = store.get()

            secret_file_name = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), cls.CLIENT_SECRET_FILE
            )
            service_account_path = os.path.join(
                credential_dir, cls.SERVICE_ACCOUNT_SECRET_FILE
            )

            if not credentials or credentials.invalid:
                if os.path.isfile(service_account_path):
                    print("service account exist, google_storage_sheet.py")
                    credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(
                        service_account_path, scopes=cls.SCOPES
                    )
                    store.locked_put(credentials)
                else:
                    print("service account not found, google_storage_sheet.py")
                    flow = client.flow_from_clientsecrets(
                        secret_file_name,
                        cls.SCOPES,
                        redirect_uri="urn:ietf:wg:oauth:2.0:oob",
                    )
                    flow.user_agent = cls.APPLICATION_NAME
                    credentials = tools.run_flow(flow, store, flags)

            http = credentials.authorize(httplib2.Http())
            discoveryUrl = "https://sheets.googleapis.com/$discovery/rest?" "version=v4"
            cls.SHEETS_SERVICE = discovery.build(
                "sheets", "v4", http=http, discoveryServiceUrl=discoveryUrl
            )
            cls.DRIVE_SERVICE = discovery.build("drive", "v3", http=http)
            cls.SLIDES_SERVICE = discovery.build("slides", "v1", http=http)
            cls.CREDENTIALS = credentials
            cls.IS_AUTHENTICATED = True

        return cls.CREDENTIALS

    @classmethod
    def _get_next_diff(cls, op_type: GoogleAPIOpType) -> int:
        next_in_list = cls.EXECUTIONS_TIME_LIST[op_type][0]
        current_time = mammut.get_timezone_aware_datetime_now()
        diff = current_time - next_in_list
        current_diff_sec = diff.total_seconds()
        return current_diff_sec

    @classmethod
    def _get_next_sleep(cls, op_type: GoogleAPIOpType) -> float:
        next_in_list = cls.EXECUTIONS_TIME_LIST[op_type][0]
        if len(cls.EXECUTIONS_TIME_LIST[op_type]) >= 1:
            next_next_in_list = cls.EXECUTIONS_TIME_LIST[op_type][1]
        else:
            next_next_in_list = mammut.get_timezone_aware_datetime_now()
        diff = next_next_in_list - next_in_list
        next_diff_sec = diff.total_seconds()
        if float(next_diff_sec) >= cls.MIN_API_OP_DELAY:
            return next_diff_sec
        else:
            return cls.MIN_API_OP_DELAY

    @classmethod
    def _check_exec_limit(cls, op_type: GoogleAPIOpType):
        if len(cls.EXECUTIONS_TIME_LIST[op_type]) >= cls.EXECUTION_LIMIT[op_type]:
            while cls._get_next_diff(op_type) <= cls.EXECUTION_TIME_LIMIT[op_type]:
                current_diff_sec = cls._get_next_diff(op_type)
                # If we met the read quota limit, we need to wait at least this
                # difference
                match_quata_limit_sleep = (
                    cls.EXECUTION_TIME_LIMIT[op_type] - current_diff_sec
                )
                total_next_sleep = (
                    cls._get_next_sleep(op_type) + match_quata_limit_sleep
                )
                logger.debug(f"Current next diff {current_diff_sec} - sleeping")
                sleep(total_next_sleep)
                cls.EXECUTIONS_TIME_LIST[op_type] = cls.EXECUTIONS_TIME_LIST[op_type][
                    1:
                ]


class GoogleStorageDrive(GoogleAPI):
    @classmethod
    @GoogleAPI.ensure_credentials_and_read_limits
    def exist_folder(cls, folder_id):
        cls.get_credentials()

        folder_found = True
        try:
            result_images_desc = (
                GoogleStorageDrive.DRIVE_SERVICE.files().get(fileId=folder_id).execute()
            )
            if not result_images_desc.get("id", ""):
                folder_found = False
        except:
            folder_found = False
        return folder_found

    @classmethod
    @GoogleAPI.ensure_credentials_and_read_limits
    def get_folders_in_folder(cls, folder_id):
        cls.get_credentials()
        files_tuples = list()
        response = (
            GoogleStorageDrive.DRIVE_SERVICE.files()
            .list(
                q=f"'{folder_id}' in parents",
                fields="files(id, name, mimeType, modifiedTime)",
            )
            .execute()
        )
        for elem in response.get("files"):
            if elem["mimeType"] == "application/vnd.google-apps.folder":
                files_tuples.append((elem["name"], elem["id"]))
        return files_tuples

    @classmethod
    @GoogleAPI.ensure_credentials_and_read_limits
    def get_all_files_in_folder(cls, folder_id):
        logger.info(
            "Download files from folder: method-get_all_files_in_folder "
            + str(folder_id)
        )
        cls.get_credentials()
        file_tuples = {}
        file_dates = {}

        def add_tuple(item):
            tuple = (item["name"], item["id"])
            file_tuples[item["name"]] = tuple
            file_dates[item["name"]] = get_datetime_from_rfc3339(item["modifiedTime"])

        result_files = (
            GoogleStorageDrive.DRIVE_SERVICE.files()
            .list(
                q=f"'{folder_id}' in parents",
                fields="files(id, name, mimeType, modifiedTime)",
            )
            .execute()
        )
        items = result_files.get("files", [])
        if items:
            for item in items:
                if item["mimeType"] != "application/vnd.google-apps.folder":
                    if item["name"] not in file_dates:
                        add_tuple(item)
                    else:
                        current_time = file_dates[item["name"]]
                        new_time = get_datetime_from_rfc3339(item["modifiedTime"])
                        if new_time > current_time:
                            add_tuple(item)
        return list(file_tuples.values())

    @classmethod
    @GoogleAPI.ensure_credentials_and_read_limits
    def download_files(
        cls,
        source_folder_id: str,
        dest_path: str = os.path.join(os.path.expanduser("~"), "temp"),
        file_names: List[str] = [],
        show_progress=None,
    ):
        logger.info(
            "Download file from folder: method-download_files" + str(source_folder_id)
        )
        cls.get_credentials()
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        file_tuples = []
        result_files = (
            GoogleStorageDrive.DRIVE_SERVICE.files()
            .list(q=f"'{source_folder_id}' in parents")
            .execute()
        )
        items = result_files.get("files", [])
        if items:
            for item in items:
                if item["mimeType"] != "application/vnd.google-apps.folder":
                    if len(file_names) == 0 or item["name"] in file_names:
                        result_file = (
                            GoogleStorageDrive.DRIVE_SERVICE.files()
                            .get(
                                fileId=item["id"],
                                fields="mimeType,name,id,webContentLink,webViewLink",
                            )
                            .execute()
                        )
                        request = GoogleStorageDrive.DRIVE_SERVICE.files().get_media(
                            fileId=item["id"]
                        )
                        full_path = os.path.join(dest_path, item["name"])
                        if not os.path.exists(full_path):
                            fh = io.FileIO(full_path, mode="wb")
                            downloader = MediaIoBaseDownload(fh, request)
                            done = False
                            while done is False:
                                status, done = downloader.next_chunk()
                                if show_progress != None:
                                    show_progress(
                                        "Downloading {} - {}".format(
                                            item["name"], int(status.progress() * 100)
                                        )
                                    )
                            fh.close()
                        preview_url = "https://drive.google.com/file/d/{}/preview".format(
                            result_file["id"]
                        )
                        file_tuples.append(
                            (
                                result_file["name"],
                                result_file["id"],
                                result_file["webContentLink"],
                                preview_url,
                                result_file["webViewLink"],
                            )
                        )
                else:
                    cls.download_files(item["id"], dest_path, file_names, show_progress)
        return file_tuples


NGRAM_CORPORA = {
    "english": 15,
    "american english": 17,
    "british english": 18,
    "english fiction": 16,
    "chinese": 23,
    "french": 19,
    "german": 20,
    "hebrew": 24,
    "italian": 22,
    "russian": 25,
    "spanish": 21,
}

NGRAM_CORPORA_BY_REGIONAL_SETTINGS = {"en": "english", "sp": "spanish", "es": "spanish"}


def get_ngram_db_file_names() -> str:
    file_name = resource_filename("mammut.resources.ngram", "google_ngram_cache.db")
    file_name = file_name[:-3]
    return file_name


@GoogleAPI.ensure_credentials_and_ngram_limits
def ngram_frequency(
    token,
    regional_settings,
    smoothing=0,
    year_start=2000,
    year_end=2008,
    case_insensitive=True,
):
    def inner_func(file_db):
        with dbm.open(file_db, "c") as db:
            token_db_key = "{} <---> {}".format(regional_settings, token)
            if token_db_key in db:
                res_from_db = struct.unpack("f", db[token_db_key])[0]
                return res_from_db
            else:
                res = 0.0
                corpus_id = NGRAM_CORPORA[
                    NGRAM_CORPORA_BY_REGIONAL_SETTINGS[regional_settings]
                ]
                token_url = parse.quote(token)
                case_insen = ""
                if case_insensitive:
                    case_insen = "&case_insensitive=on"
                url = (
                    "https://books.google.com/ngrams/graph?content={}{}&year_start={}&year_end={}"
                    "&corpus={}&smoothing={}".format(
                        token_url,
                        case_insen,
                        year_start,
                        year_end,
                        corpus_id,
                        smoothing,
                    )
                )
                page = request.urlopen(url).read()
                start = page.find("data = ".encode("utf-8"))
                end = page.find("];\n".encode("utf-8"), start)
                data = eval(page[start + 8 : end])
                if not isinstance(data, tuple) and not isinstance(data, list):
                    data = [data]
                for d in data:
                    if "type" in d and d["type"] == "CASE_INSENSITIVE":
                        res = float(d["timeseries"][-1])
                        break
                    else:
                        res = res + float(d["timeseries"][-1])
                res_db = struct.pack("f", res)
                db[token_db_key] = res_db
                return res

    file_name = get_ngram_db_file_names()
    return inner_func(file_name)


def del_cache_ngram_frequency(token, regional_settings):
    def inner_del_func(file_db):
        with dbm.open(file_db, "c") as db:
            token_db_key = "{} <---> {}".format(regional_settings, token)
            if token_db_key in db:
                del db[token_db_key]

    file_name = get_ngram_db_file_names()
    inner_del_func(file_name)


def unigram_frecuency(
    token,
    regional_settings,
    smoothing=0,
    year_start=2000,
    year_end=2008,
    case_insensitive=True,
):
    return ngram_frequency(
        token, regional_settings, smoothing, year_start, year_end, case_insensitive
    )


def unordered_bigram_frecuency(
    tokens_bituple,
    regional_settings,
    smoothing=0,
    year_start=2000,
    year_end=2008,
    case_insensitive=True,
):
    bigram_1 = tokens_bituple[0] + " " + tokens_bituple[1]
    res = ngram_frequency(
        bigram_1, regional_settings, smoothing, year_start, year_end, case_insensitive
    )
    bigram_2 = tokens_bituple[1] + " " + tokens_bituple[0]
    res = res + ngram_frequency(
        bigram_2, regional_settings, smoothing, year_start, year_end, case_insensitive
    )
    return res


def unordered_trigram_frecuency(
    tokens_trituple,
    regional_settings,
    smoothing=0,
    year_start=2000,
    year_end=2008,
    case_insensitive=True,
):
    trigram_123 = (
        tokens_trituple[0] + " " + tokens_trituple[1] + " " + tokens_trituple[2]
    )
    res = ngram_frequency(
        trigram_123,
        regional_settings,
        smoothing,
        year_start,
        year_end,
        case_insensitive,
    )
    trigram_132 = (
        tokens_trituple[0] + " " + tokens_trituple[2] + " " + tokens_trituple[1]
    )
    res = res + ngram_frequency(
        trigram_132,
        regional_settings,
        smoothing,
        year_start,
        year_end,
        case_insensitive,
    )
    trigram_213 = (
        tokens_trituple[1] + " " + tokens_trituple[0] + " " + tokens_trituple[2]
    )
    res = res + ngram_frequency(
        trigram_213,
        regional_settings,
        smoothing,
        year_start,
        year_end,
        case_insensitive,
    )
    trigram_231 = (
        tokens_trituple[1] + " " + tokens_trituple[2] + " " + tokens_trituple[0]
    )
    res = res + ngram_frequency(
        trigram_231,
        regional_settings,
        smoothing,
        year_start,
        year_end,
        case_insensitive,
    )
    trigram_312 = (
        tokens_trituple[2] + " " + tokens_trituple[0] + " " + tokens_trituple[1]
    )
    res = res + ngram_frequency(
        trigram_312,
        regional_settings,
        smoothing,
        year_start,
        year_end,
        case_insensitive,
    )
    trigram_321 = (
        tokens_trituple[2] + " " + tokens_trituple[1] + " " + tokens_trituple[0]
    )
    res = res + ngram_frequency(
        trigram_321,
        regional_settings,
        smoothing,
        year_start,
        year_end,
        case_insensitive,
    )
    return res
