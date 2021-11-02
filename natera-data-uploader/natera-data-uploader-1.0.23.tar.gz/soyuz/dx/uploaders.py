#!/usr/bin/env python

import logging
import multiprocessing
import os
import time
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager

from soyuz.dx.sentinels import WesSignateraSentinel, RawSentinel, PersonalisSentinel
from soyuz.dx.variables import Type, Property
from soyuz.data.folders import WesSignateraSeqFolder, PersonalisSeqFolder, RawSeqFolder, BgiSeqFolder
from soyuz.data.storages import StorageFactory
from soyuz.utils import UploaderException


@contextmanager
def poolcontext(*args, **kwargs):
    pool = multiprocessing.Pool(*args, **kwargs)
    yield pool
    pool.terminate()


class WatchUploader(object):
    __metaclass__ = ABCMeta

    def __init__(self, settings):
        self.settings = settings

    def watch(self, watch_dir):
        while True:
            for seq_folder in watch_dir.get_seq_folders():
                if watch_dir.is_uploaded(seq_folder.get_name()):
                    logging.info("{} already uploaded. Skipping".format(seq_folder.get_name()))
                    continue
                try:
                    uploader = DxUploaderFactory.create(self.settings, seq_folder)
                    uploader.upload(seq_folder)
                    watch_dir.complete(seq_folder.get_name())
                except UploaderException as e:
                    logging.error("{}. Skipping".format(e))
                    continue
            time.sleep(self.settings.get_interval())


class DxUploaderBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, settings):
        self.settings = settings
        self.storage = StorageFactory.create(settings)

    def __call__(self, data_file):
        return self.upload_file(data_file)

    def upload(self, seq_folder):
        self._validate_target_dir(seq_folder)
        logging.info("Starting upload for {}".format(seq_folder.get_name()))
        sentinel = self._create_sentinel(seq_folder.get_name())
        if self.settings.get_process_count() > 1:
            with poolcontext(processes=self.settings.get_process_count()) as pool:
                results = pool.map(self, seq_folder.list_files())
        else:
            results = [self.upload_file(data_file) for data_file in seq_folder.list_files()]
        for data_file, file_id in results:
            sentinel.add_file(data_file, file_id)
        sentinel.close()
        logging.info("{} has been successfully uploaded".format(seq_folder.get_name()))

    def upload_file(self, data_file):
        remote_folder = os.path.join(self.settings.get_base_dir(),
                                     data_file.get_seq_folder_name(),
                                     data_file.get_relative_path()).replace("\\", "/")
        types = self._get_additional_types(data_file)
        types.append(Type.UPLOAD_DATA)
        properties = self._get_additional_properties(data_file, data_file.get_seq_folder_name())
        properties[Property.RUN_FOLDER] = data_file.get_seq_folder_name()
        file_id = self.storage.upload_file(data_file, remote_folder, types, properties)
        return data_file, file_id

    def _validate_target_dir(self, folder):
        self.storage.validate_target_dir(folder)

    @abstractmethod
    def _create_sentinel(self, seq_folder_name):
        raise NotImplementedError()

    @abstractmethod
    def _get_additional_types(self, data_file):
        raise NotImplementedError()

    @abstractmethod
    def _get_additional_properties(self, data_file, seq_folder_name):
        raise NotImplementedError()


class WesSignateraDxUploader(DxUploaderBase):
    SEQ_FOLDER_TYPE = WesSignateraSeqFolder

    def _create_sentinel(self, seq_folder_name):
        return WesSignateraSentinel(self.storage, self.settings.get_base_dir(), seq_folder_name)

    def _get_additional_types(self, data_file):
        types = []
        data_type = data_file.get_type()
        if data_type:
            types.append(data_type)
            if data_type == Type.CSV and data_file.get_name().startswith("WES-QCMetrics"):
                types.append(Type.WESQCREPORT)
        return types

    def _get_additional_properties(self, data_file, seq_folder_name):
        properties = {}
        if data_file.get_sample_id():
            properties[Property.SAMPLE_REFERENCE] = "{}/{}".format(seq_folder_name, data_file.get_sample_id())
        return properties


class PersonalisDxUploader(DxUploaderBase):
    SEQ_FOLDER_TYPE = PersonalisSeqFolder

    def _create_sentinel(self, seq_folder_name):
        return PersonalisSentinel(self.storage, self.settings.get_base_dir(), seq_folder_name)

    def _get_additional_types(self, data_file):
        types = []
        data_type = data_file.get_type()
        if data_type:
            types.append(data_type)
            if data_type == Type.CSV and data_file.get_name().startswith("QCMetrics"):
                types.append(Type.WESQCREPORT)
        return types

    def _get_additional_properties(self, data_file, seq_folder_name):
        properties = {}
        if data_file.get_sample_id():
            properties[Property.SAMPLE_REFERENCE] = "{}/{}".format(seq_folder_name, data_file.get_sample_id())
        return properties


class RawDxUploader(DxUploaderBase):
    SEQ_FOLDER_TYPE = RawSeqFolder

    def _create_sentinel(self, seq_folder_name):
        return RawSentinel(self.storage, self.settings.get_base_dir(), seq_folder_name)

    def _get_additional_types(self, data_file):
        return []

    def _get_additional_properties(self, data_file, seq_folder_name):
        return {}


class BgiDxUploader(DxUploaderBase):
    SEQ_FOLDER_TYPE = BgiSeqFolder

    def _create_sentinel(self, seq_folder_name):
        return RawSentinel(self.storage, self.settings.get_base_dir(), seq_folder_name)

    def _get_additional_types(self, data_file):
        return []

    def _get_additional_properties(self, data_file, seq_folder_name):
        return {}


class DxUploaderFactory(object):
    @staticmethod
    def create(settings, seq_folder):
        if isinstance(seq_folder, BgiDxUploader.SEQ_FOLDER_TYPE):
            return BgiDxUploader(settings)
        elif isinstance(seq_folder, RawDxUploader.SEQ_FOLDER_TYPE):
            return RawDxUploader(settings)
        elif isinstance(seq_folder, WesSignateraDxUploader.SEQ_FOLDER_TYPE):
            return WesSignateraDxUploader(settings)
        raise UploaderException(
                "Uploader for the folder {} was not found".format(seq_folder.get_name()))
