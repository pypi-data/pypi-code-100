#!/usr/bin/env python3
import argh
import subprocess
import os
from typing import List, Iterator, Union
import bs4
from meduse import bsfilters
import requests
from elasticsearch import Elasticsearch, exceptions as es_exceptions
from datetime import datetime
import re
import logging
from logging import FileHandler
import json
import socket
import sanic
from sanic.exceptions import NotFound, InvalidUsage

pre_index_hook_help = (
    "Use this flag to invoke a script with the "
    "downloaded HTML file as an argument. "
    "This is executed BEFORE indexing. "
    "You can use this to apply transformations to a document."
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger_handler_set = False
log_file_path = None

# filters are executed in order
ACTIVE_FILTERS = [
    bsfilters.remove_navigation_select,
    bsfilters.fix_empty_ids,
    bsfilters.fix_empty_form_action,
    bsfilters.remove_logbox,
    bsfilters.remove_noteslink,
    bsfilters.replace_search_form_action,
]

ELASTICSEARCH_DEFAULT_HOST = "localhost"
ELASTICSEARCH_DEFAULT_PORT = 9200

MEDUSE_VERBOSE_MODE = False


def _slugify(s: str) -> str:
    s = s.lower()
    for c in [" ", "-", ".", "/"]:
        s = s.replace(c, "_")
    s = re.sub("\W", "", s)
    s = s.replace("_", " ")
    s = re.sub("\s+", " ", s)
    s = s.strip()
    s = s.replace(" ", "-")
    return s


def _verbose_print(message: str):
    global logger
    global logger_handler_set
    if not logger_handler_set:
        global log_file_path
        if log_file_path:
            logger.addHandler(FileHandler(log_file_path))
            logger_handler_set = True
    global MEDUSE_VERBOSE_MODE
    if MEDUSE_VERBOSE_MODE:
        print(str(datetime.now()) + " : " + message)
    logger.info(message)


def _es_handle(
    host: str = ELASTICSEARCH_DEFAULT_HOST, port: int = ELASTICSEARCH_DEFAULT_PORT
) -> Elasticsearch:
    return Elasticsearch(hosts=[{"host": host, "port": port}])


def _get_tag_soup(html_file_path: str) -> Union[bs4.BeautifulSoup, None]:
    with open(html_file_path, "r", errors="ignore") as f:
        try:
            soup = bs4.BeautifulSoup(f.read(), features="lxml")
            return soup
        except UnicodeDecodeError:  # when even bs4 can't parse
            return None


def _wget_status_label(wget_status_code: int) -> str:
    if wget_status_code == 0:
        return "No problems occurred."
    if wget_status_code == 1:
        return "Generic error code."
    if wget_status_code == 2:
        return "Parse error—for instance, when parsing command-line options, the ‘.wgetrc’ or ‘.netrc’..."
    if wget_status_code == 3:
        return "File I/O error."
    if wget_status_code == 4:
        return "Network failure."
    if wget_status_code == 5:
        return "SSL verification failure."
    if wget_status_code == 6:
        return "Username/password authentication failure."
    if wget_status_code == 7:
        return "Protocol errors."
    if wget_status_code == 8:
        return "Server issued an error response."
    raise ValueError("Unknown wget status code ({})".format(wget_status_code))


def _scan_dir(start_path: str, extension: str = None) -> Iterator[str]:
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if extension:
                if file[len(extension) * -1:].lower() == extension.lower():
                    yield os.path.join(root, file)
            else:
                yield os.path.join(root, file)


def _prepare_destination_folder(destination_folder: str) -> bool:
    try:
        os.makedirs(destination_folder, exist_ok=True)
        return True
    except PermissionError:
        return False


def _find_sitemaps(base_url: str) -> List[str]:
    if base_url[-1] != "/":
        base_url = base_url + "/"
    sitemaps_found = []
    response = requests.get(base_url + "robots.txt")
    if response.status_code == 200:
        for line in response.text.split("\n"):
            if line[0:len("Sitemap:")].lower() == "sitemap:":
                sitemaps_found.append(line[len("Sitemap:"):].strip())
    # usual suspects
    response = requests.get(base_url + "sitemap.txt")
    if response.status_code == 200:
        sitemaps_found.append(response.url)
    response = requests.get(base_url + "sitemap.xml")
    if response.status_code == 200:
        sitemaps_found.append(response.url)
    return list(set(sitemaps_found))


def _extract_urls_from_sitemap(sitemap_url: str) -> Iterator[str]:
    response = requests.get(sitemap_url)
    if response.status_code == 200:
        if sitemap_url[-4:] == ".xml":
            soup = bs4.BeautifulSoup(response.text, features="lxml")
            for elem in soup.find_all("loc"):
                yield elem.string.strip()
        if sitemap_url[-4:] == ".txt":
            for line in response.text.split("\n"):
                if line[0:4] == "http":
                    yield line.strip()


def _patch(documents_folder: str, project_identifier: str):
    for file_path in _scan_dir(documents_folder, ".html"):
        _verbose_print("  |---> Patching {}".format(file_path))
        tag_soup = _get_tag_soup(file_path)
        if tag_soup:
            for soup_filter in ACTIVE_FILTERS:
                soup_filter(tag_soup, {"project_identifier": project_identifier})
            with open(file_path, "w") as f:
                f.write(str(tag_soup))


def _hook(documents_folder: str, executable_path: str):
    for file_path in _scan_dir(documents_folder, ".html"):
        hook_process = subprocess.Popen(
            [executable_path, file_path],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        for line in hook_process.stdout.readlines():
            print(line.decode("utf-8"), end="")
        hook_process.wait()


def index(
    documents_folder: str,
    elasticsearch_index_name: str,
    elasticsearch_host: str = ELASTICSEARCH_DEFAULT_HOST,
    elasticsearch_port: int = ELASTICSEARCH_DEFAULT_PORT,
):
    """
    (re)Index documents
    """

    es = _es_handle(elasticsearch_host, elasticsearch_port)
    use_es = True
    try:
        # with warnings.catch_warnings():
        #    warnings.simplefilter("never")
        es.indices.delete(index=elasticsearch_index_name, ignore=[400, 404])
    except:  # whatever happens here...
        _verbose_print("No Elasticsearch service available. Will store to file.")
        use_es = False
    with open("{}/indexed.db".format(documents_folder), "w") as index_file:
        for file_path in _scan_dir(documents_folder, ".html"):
            _verbose_print("  |---> Indexing {}".format(file_path))
            tag_soup = _get_tag_soup(file_path)
            if not tag_soup:
                _verbose_print("Failed making soup from {}".format(file_path))
                continue
            title = None
            text = None
            h1 = tag_soup.find("h1")
            if h1:
                title = " ".join(x.strip() for x in h1.text.split("\n")).strip()
            content = tag_soup.find(id="content")
            if content:
                text = content.text
            doc = {
                "title": title,
                "text": text,
                "path": file_path[len(documents_folder):],
            }
            index_file.write("{}\n".format(json.dumps(doc)))
            if use_es:
                es.index(index=elasticsearch_index_name, doc_type="html_page", body=doc)
    return True


def _wget(
    source_url: str,
    destination_folder: str = ".",
    auth_user: str = None,
    auth_password: str = None,
):
    global MEDUSE_VERBOSE_MODE
    sh_command = [
        "wget",
        "--mirror",
        "--convert-links",
        "--adjust-extension",
        "--page-requisites",
        "--no-parent",
        "--directory-prefix={}".format(destination_folder),
        "--verbose"
        if MEDUSE_VERBOSE_MODE
        else "--append-output={}/{}".format(destination_folder, "wget.log"),
    ]

    if auth_user and auth_password:
        sh_command.append("--http-user={}".format(auth_user))
        sh_command.append("--http-password={}".format(auth_password))

    sh_command.append(source_url)

    wget_process = subprocess.Popen(
        sh_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    for line in wget_process.stdout.readlines():
        print(line.decode("utf-8"), end="")
    # see wget's exit status: https://www.gnu.org/software/wget/manual/html_node/Exit-Status.html
    wget_status_code = wget_process.wait()
    # status code 8 is ignored because it may be returned on
    # any of the urls from the current batch (like a 404 on a page)
    if wget_status_code not in [0, 8]:
        print(_wget_status_label(wget_status_code))


def mirror(
    source_url: str,
    destination_folder: str = ".",
    verbose: bool = False,
    auto_find_sitemaps: bool = False,
    elasticsearch_host: str = ELASTICSEARCH_DEFAULT_HOST,
    elasticsearch_port: int = ELASTICSEARCH_DEFAULT_PORT,
    pre_indexing_hook: pre_index_hook_help = "",
    auth_user: "HTTP Basic Auth user" = None,
    auth_password: "HTTP Basic Auth password" = None,
):
    """
    Mirror website and index documents.

    In that order:

    - Mirror website with wget.
    - Patch and reformat HTML documents.
    - Index HTML documents in Elasticsearch.
    """
    global MEDUSE_VERBOSE_MODE
    MEDUSE_VERBOSE_MODE = verbose

    destination_folder = os.path.abspath(destination_folder)
    if not _prepare_destination_folder(destination_folder):
        print("Could not create destination folder.")
        return 1
    global log_file_path
    log_file_path = destination_folder + "/activity.log"
    _verbose_print(
        "Executing wget from URL {} to folder {}...".format(
            source_url, destination_folder
        )
    )
    _wget(
        source_url, destination_folder, auth_user=auth_user, auth_password=auth_password
    )
    _verbose_print("wget mirror done.")

    if auto_find_sitemaps:
        _verbose_print("Looking for sitemaps...")
        for sitemap in _find_sitemaps(source_url):
            _verbose_print(
                "Sitemap found at {}. Proceed with wget mirroring...".format(sitemap)
            )
            for url in _extract_urls_from_sitemap(sitemap):
                _wget(
                    url,
                    destination_folder,
                    auth_user=auth_user,
                    auth_password=auth_password,
                )

    _verbose_print("Patching HTML documents...")
    _patch(destination_folder, _slugify(source_url))
    _verbose_print("Documents patched.")

    if pre_indexing_hook:
        _verbose_print("Hooking {}".format(pre_indexing_hook))
        _hook(destination_folder, pre_indexing_hook)

    _verbose_print("Indexing HTML documents...")
    has_indexed = index(
        destination_folder, _slugify(source_url), elasticsearch_host, elasticsearch_port
    )
    if has_indexed:
        _verbose_print("Documents indexed.")
    else:
        _verbose_print("Indexing skipped.")
    _verbose_print("Done. Quit.")
    with open(destination_folder + "/manifest.json", "w") as manifest_file:
        json.dump(
            {
                "from": socket.getfqdn(),
                "source_url": source_url,
                "timestamp": datetime.timestamp(datetime.now()),
            },
            manifest_file,
            indent=4,
            sort_keys=True,
        )


def serve(
    root_directory: str,
    host: str = "localhost",
    port: int = 8888,
    elasticsearch_host: str = ELASTICSEARCH_DEFAULT_HOST,
    elasticsearch_port: int = ELASTICSEARCH_DEFAULT_PORT,
):

    app = sanic.Sanic(name="meduse-server")

    @app.route("/_esproxy/")
    async def esproxy(request: sanic.request):
        print(request.args.get("q", None))
        project_index = request.args.get("project_index", None)
        q = request.args.get("q", None)

        if project_index and q:
            try:
                es = _es_handle(elasticsearch_host, elasticsearch_port)
                results = es.search(
                    index=project_index,
                    body={
                        "_source": ["title", "path"],  # limit response to these fields
                        "from": 0,
                        "size": 500,  # todo: paginate
                        "query": {
                            "query_string": {"default_field": "text", "query": q}
                        },
                    },
                )
                return sanic.response.json({"q": q, "results": results["hits"]})
            except es_exceptions.NotFoundError:
                raise NotFound('Index "{}" not found'.format(project_index))

        else:
            raise InvalidUsage
    app.static("/", root_directory)
    app.run(host=host, port=port)


if __name__ == "__main__":
    parser = argh.ArghParser()
    parser.add_commands([mirror, serve, index])
    parser.dispatch()
