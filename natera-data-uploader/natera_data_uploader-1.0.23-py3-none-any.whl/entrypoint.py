#!/usr/bin/env python

import logging

from soyuz.configuration import Parameters
from soyuz.configuration import Settings
from soyuz.data.daemons import Daemon
from soyuz.data.folders import WesSignateraSeqFolder, BgiSeqFolder, RawSeqFolder, PersonalisSeqFolder, WatchDirectory
from soyuz.data.storages import StorageFactory
from soyuz.dx.uploaders import WesSignateraDxUploader, BgiDxUploader, RawDxUploader, PersonalisDxUploader, WatchUploader
from soyuz.utils import UploaderException


def main():
    try:
        params = Parameters()
        settings = Settings()

        settings.logging.initialize()

        if params.get_action() in [Parameters.UPLOAD_ACTION, Parameters.WATCH_ACTION]:

            settings.set_token(params.get_token() or settings.get_token())

            folder = None
            uploader = None

            if params.get_action() == Parameters.UPLOAD_ACTION:
                if params.get_upload_type() == Parameters.WES_SIGNATERA_UPLOAD:
                    uploader = WesSignateraDxUploader(settings)
                    folder = WesSignateraSeqFolder(params.get_folder())
                elif params.get_upload_type() == Parameters.BGI_UPLOAD:
                    uploader = BgiDxUploader(settings)
                    folder = BgiSeqFolder(params.get_folder())
                elif params.get_upload_type() == Parameters.RAW_UPLOAD:
                    uploader = RawDxUploader(settings)
                    folder = RawSeqFolder(params.get_folder())
                elif params.get_upload_type() == Parameters.PERSONALIS_UPLOAD:
                    uploader = PersonalisDxUploader(settings)
                    folder = PersonalisSeqFolder(params.get_folder())

                if not folder or not uploader:
                    raise UploaderException("Incorrect upload type")

                if not folder.is_valid:
                    raise UploaderException("Data folder is not in a valid state")

                uploader.upload(folder)

            elif params.get_action() == Parameters.WATCH_ACTION:

                settings.set_interval(params.get_interval() or settings.get_interval())

                uploader = WatchUploader(settings)

                if params.get_watch_type() == Parameters.START_WATCH:
                    if params.foreground():
                        uploader.watch(WatchDirectory(params.get_folder()))
                    else:
                        Daemon(uploader.watch, WatchDirectory(params.get_folder())).start()
                elif params.get_watch_type() == Parameters.STOP_WATCH:
                    Daemon().stop()
                elif params.get_watch_type() == Parameters.STATUS_WATCH:
                    Daemon().status()

        elif params.get_action() == Parameters.CONFIG_ACTION:

            if params.get_config_action() == Parameters.GET_CONFIG:
                if params.get_config_parameter_key() == "storage":
                    logging.info(settings.get_storage())
                elif params.get_config_parameter_key() == "token":
                    logging.info(settings.get_token())
                elif params.get_config_parameter_key() == "exodus_url":
                    logging.info(settings.get_exodus_url())
                elif params.get_config_parameter_key() == "basedir":
                    logging.info(settings.get_base_dir())
                elif params.get_config_parameter_key() == "interval":
                    logging.info(settings.get_interval())
                elif params.get_config_parameter_key() == "ua_path":
                    logging.info(settings.get_ua_path())
                elif params.get_config_parameter_key() == "ua_parameters":
                    logging.info(settings.get_ua_parameters())
                elif params.get_config_parameter_key() == "process_count":
                    logging.info(settings.get_process_count())
                elif params.get_config_parameter_key() == "chunk_size":
                    logging.info(settings.get_chunk_size())

            elif params.get_config_action() == Parameters.SET_CONFIG:
                if params.get_config_parameter_key() == "storage":
                    settings.set_storage(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "token":
                    settings.set_token(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "exodus_url":
                    settings.set_exodus_url(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "exodus_username":
                    settings.set_exodus_username(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "exodus_password":
                    settings.set_exodus_password(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "basedir":
                    settings.set_basedir(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "interval":
                    settings.set_interval(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "ua_path":
                    settings.set_ua_path(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "ua_parameters":
                    settings.set_ua_parameters(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "process_count":
                    settings.set_process_count(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "chunk_size":
                    settings.set_chunk_size(params.get_config_parameter_value())
                else:
                    raise UploaderException("There is no parameter '{}'".format(params.get_config_parameter_key()))
                settings.dump()
                logging.info("Set {} to {}".format(params.get_config_parameter_key(), params.get_config_parameter_value()))

    except UploaderException as e:
        logging.error(e)
        quit(1)


if __name__ == "__main__":
    main()
