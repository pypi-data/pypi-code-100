#!/usr/bin/env python

import argparse
import json
import logging
import multiprocessing
import os
import sys

from soyuz import __version__ as version
from soyuz.utils import UploaderException, Logging
from soyuz.data.storages import StorageType


class Parameters(object):
    UPLOAD_ACTION = "upload"
    WATCH_ACTION = "watch"
    WATCH_INTERVAL = 600
    WES_SIGNATERA_UPLOAD = "wes_signatera"
    RAW_UPLOAD = "raw"
    BGI_UPLOAD = "bgi"
    PERSONALIS_UPLOAD = 'personalis'
    CONFIG_ACTION = "config"
    GET_CONFIG = "get"
    SET_CONFIG = "set"
    START_WATCH = "start"
    STOP_WATCH = "stop"
    STATUS_WATCH = "status"
    VERSION_ACTION = "version"

    def __init__(self, args=sys.argv[1:]):
        parser = argparse.ArgumentParser(description="Constellation Sequencing Uploader v{}".format(version))

        parser.add_argument('--token', '-t', help='DNAnexus token with access to a single project with level UPLOAD')

        sp = parser.add_subparsers(dest='command')
        sp.required = True

        ##################
        # uploader upload
        ##################
        upload_parser = sp.add_parser(Parameters.UPLOAD_ACTION, help='Upload sequencing folder')
        upload_parser.set_defaults(action=Parameters.UPLOAD_ACTION)

        sup = upload_parser.add_subparsers(dest='upload type')
        sup.required = True

        # uploader upload wes_signatera
        wes_signatera_parser = sup.add_parser(Parameters.WES_SIGNATERA_UPLOAD, help='Upload for WES Signatera')
        wes_signatera_parser.set_defaults(upload_type=Parameters.WES_SIGNATERA_UPLOAD)
        wes_signatera_parser.add_argument('folder', metavar='Folder')

        # uploader upload bgi
        bgi_parser = sup.add_parser(Parameters.BGI_UPLOAD, help='Upload for BGI with fastq files')
        bgi_parser.set_defaults(upload_type=Parameters.BGI_UPLOAD)
        bgi_parser.add_argument('folder', metavar='Folder')

        # uploader upload raw
        raw_parser = sup.add_parser(Parameters.RAW_UPLOAD, help='Raw upload without any validation and modifications')
        raw_parser.set_defaults(upload_type=Parameters.RAW_UPLOAD)
        raw_parser.add_argument('folder', metavar='Folder')

        # uploader upload personalis
        personalis_parser = sup.add_parser(Parameters.PERSONALIS_UPLOAD, help='Upload for Personalis')
        personalis_parser.set_defaults(upload_type=Parameters.PERSONALIS_UPLOAD)
        personalis_parser.add_argument('folder', metavar='Folder')

        ##################
        # uploader watch
        ##################
        watch_parser = sp.add_parser(Parameters.WATCH_ACTION, help='Watch sequencing folder')
        watch_parser.set_defaults(action=Parameters.WATCH_ACTION)

        watch_parser.add_argument('--interval', '-n', default=Parameters.WATCH_INTERVAL, type=int, help='Interval in seconds between every run in watch mode')

        sup = watch_parser.add_subparsers(dest='watch type')
        sup.required = True

        # uploader watch start
        start_watch_parser = sup.add_parser(Parameters.START_WATCH, help='Start watching folder')
        start_watch_parser.set_defaults(watch_type=Parameters.START_WATCH)
        start_watch_parser.add_argument('folder', metavar='Folder')
        start_watch_parser.add_argument('--foreground', '-fg', help='Run in foreground.', default=False, action='store_true')

        # uploader watch stop
        stop_watch_parser = sup.add_parser(Parameters.STOP_WATCH, help='Stop watching folder')
        stop_watch_parser.set_defaults(watch_type=Parameters.STOP_WATCH)

        # uploader watch status
        status_watch_parser = sup.add_parser(Parameters.STATUS_WATCH, help='Status of watching folder')
        status_watch_parser.set_defaults(watch_type=Parameters.STATUS_WATCH)

        ##################
        # uploader config
        ##################
        config_parser = sp.add_parser(Parameters.CONFIG_ACTION,
                                      help='Configure uploader. This action updates ~/.uploader file')
        config_parser.set_defaults(action=Parameters.CONFIG_ACTION, show_help=config_parser.print_help)

        scp = config_parser.add_subparsers(dest='config action')
        scp.required = True

        # uploader config get
        get_config_parser = scp.add_parser(Parameters.GET_CONFIG,
                                           help='Get uploader configuration')
        get_config_parser.set_defaults(config_action=Parameters.GET_CONFIG)
        get_config_parser.add_argument('config_parameter_key', metavar='Key')

        # uploader config set
        set_config_parser = scp.add_parser(Parameters.SET_CONFIG,
                                           help='Configure uploader. This action updates ~/.uploader file')
        set_config_parser.set_defaults(config_action=Parameters.SET_CONFIG)
        set_config_parser.add_argument('config_parameter_key', metavar='Key')
        set_config_parser.add_argument('config_parameter_value', metavar='Value')

        ##################
        # uploader version
        ##################
        version_parser = sp.add_parser(Parameters.VERSION_ACTION, help='Show version')
        version_parser.set_defaults(action=Parameters.VERSION_ACTION)

        self.__args = parser.parse_args(args)

        if self.__args.action == Parameters.VERSION_ACTION:
            print("v" + version)
            quit(0)

    def get_token(self):
        return self.__args.token

    def get_interval(self):
        return self.__args.interval

    def get_folder(self):
        return self.__args.folder

    def foreground(self):
        return self.__args.foreground

    def get_action(self):
        return self.__args.action

    def get_upload_type(self):
        return self.__args.upload_type

    def get_watch_type(self):
        return self.__args.watch_type

    def get_config_action(self):
        return self.__args.config_action

    def get_config_parameter_key(self):
        return self.__args.config_parameter_key

    def get_config_parameter_value(self):
        return self.__args.config_parameter_value


class Settings(object):
    SETTING_FILE = ".uploader"

    def __init__(self, settings_base_path="~"):
        self.__settings = {}
        self.logging = Logging()
        self.__full_path_to_settings = os.path.join(os.path.expanduser(settings_base_path), Settings.SETTING_FILE)

        if os.path.isfile(self.__full_path_to_settings):
            try:
                self.__settings = json.load(open(self.__full_path_to_settings))
            except Exception:
                raise UploaderException("{} is not a valid JSON".format(Settings.SETTING_FILE))

    def get_token(self):
        return self.__get_dnanexus().get('token')

    def set_token(self, token):
        self.__get_dnanexus()["token"] = token

    def get_base_dir(self):
        return self.__get_dnanexus().get('basedir', '/data/seq')

    def set_basedir(self, basedir):
        self.__get_dnanexus()["basedir"] = basedir

    def get_storage(self):
        return self.__settings.get("storage", StorageType.DEFAULT)

    def set_storage(self, storage):
        if storage not in StorageType.ALL:
            raise UploaderException("Storage type {} is not available.".format(storage))
        self.__settings["storage"] = storage

    def get_exodus_url(self):
        return self.__get_exodus().get("url")

    def set_exodus_url(self, exodus_url):
        self.__get_exodus()["url"] = exodus_url

    def get_exodus_username(self):
        return self.__get_exodus().get("username")

    def set_exodus_username(self, exodus_username):
        self.__get_exodus()["username"] = exodus_username

    def get_exodus_password(self):
        return self.__get_exodus().get("password")

    def set_exodus_password(self, exodus_password):
        self.__get_exodus()["password"] = exodus_password

    def get_interval(self):
        return self.__settings.get("interval")

    def set_interval(self, interval):
        self.__settings["interval"] = int(interval)

    def get_ua_path(self):
        return self.__get_dnanexus().get("ua_path") if os.path.isfile(self.__get_dnanexus().get("ua_path", '')) else None

    def set_ua_path(self, ua_path):
        if not os.path.isfile(ua_path):
            raise UploaderException("ua_path {} no such file.".format(ua_path))
        self.__get_dnanexus()["ua_path"] = ua_path

    def get_ua_parameters(self):
        return self.__get_dnanexus().get("ua_parameters", '')

    def set_ua_parameters(self, ua_parameters):
        self.__get_dnanexus()["ua_parameters"] = ua_parameters

    def get_chunk_size(self):
        return int(self.__settings.get("chunk_size", 200*10**6))

    def set_chunk_size(self, chunk_size):
        if isinstance(chunk_size, basestring):
            if chunk_size.endswith('M'):
                chunk_size = int(chunk_size.rstrip('M')) * 10**6
            elif chunk_size.endswith('G'):
                chunk_size = int(chunk_size.rstrip('G')) * 10**9
            if chunk_size < 5*10**6 or chunk_size > 5*10**9:
                raise UploaderException("Chunk size should be between 5M and 5G")
        self.__settings["chunk_size"] = int(chunk_size)

    def get_process_count(self):
        return self.__settings.get("process_count", 1)

    def set_process_count(self, process_count):
        process_count = int(process_count)
        if process_count > multiprocessing.cpu_count():
            logging.info("The number of upload threads cannot be higher than the number of CPU cores. Setting to {}".format(multiprocessing.cpu_count()))
            process_count = multiprocessing.cpu_count()
        elif process_count == 0:
            logging.info("The number of upload threads cannot be lower than 1. Setting to 1")
            process_count = 1
        if self.get_storage() == StorageType.DNANEXUS and not self.get_ua_path():
            logging.info("The multiprocessing is not allowed for DNAnexus without defining ua_path. Setting to 1")
            process_count = 1
        self.__settings["process_count"] = process_count

    def dump(self):
        with open(self.__full_path_to_settings, 'wt') as out:
            json.dump(self.__settings, out, sort_keys=True, indent=4, separators=(',', ': '))

    def __get_dnanexus(self):
        return self.__settings.setdefault("dnanexus", {})

    def __get_exodus(self):
        return self.__settings.setdefault("exodus", {})
