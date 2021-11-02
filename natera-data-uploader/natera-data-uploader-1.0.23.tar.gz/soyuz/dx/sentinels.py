#!/usr/bin/env python

from abc import ABCMeta, abstractmethod

from soyuz.data.records import RecordFactory, DNAnexusRecord, ExodusRecord
from soyuz.dx.variables import Type


class SentinelBase(object):
    __metaclass__ = ABCMeta

    DATA_KEY = "data"
    FASTQ_KEY = "fastq"
    METRICS_KEY = "run_metrics"
    DX_LINK_KEY = "$dnanexus_link"

    def __init__(self, storage, basedir, name):
        self.record = RecordFactory.create(storage, basedir, name)

    @abstractmethod
    def add_file(self, data_file, file_id):
        raise NotImplementedError()

    def add_link(self, file_id):
        if isinstance(self.record, DNAnexusRecord):
            return {SentinelBase.DX_LINK_KEY: file_id}
        elif isinstance(self.record, ExodusRecord):
            return file_id

    def get_id(self):
        return self.record.get_id()

    def close(self):
        self.record.close()


class WesSignateraSentinel(SentinelBase):
    def add_file(self, data_file, file_id):
        details = self.record.get_details()
        sample_id = data_file.get_sample_id()
        if sample_id:
            self.record.add_tags([sample_id])
            self.__add_data_file_details(details, sample_id, self.add_link(file_id))
        else:
            self.__add_metrics_details(details, self.add_link(file_id))
        self.record.set_details(details)

    @staticmethod
    def __add_data_file_details(details, sample_id, file_link):
        if SentinelBase.DATA_KEY not in details:
            details[SentinelBase.DATA_KEY] = {}
        data_details = details[SentinelBase.DATA_KEY]
        if sample_id not in data_details:
            data_details[sample_id] = []
        data_details[sample_id].append(file_link)

    @staticmethod
    def __add_metrics_details(details, file_link):
        if SentinelBase.METRICS_KEY not in details:
            details[SentinelBase.METRICS_KEY] = []
        details[SentinelBase.METRICS_KEY].append(file_link)


class PersonalisSentinel(SentinelBase):
    def add_file(self, data_file, file_id):
        details = self.record.get_details()
        sample_id = data_file.get_sample_id()
        if sample_id:
            self.record.add_tags([sample_id])
            if data_file.get_type() == Type.BAM:
                self.__add_data_file_details(details, sample_id, self.add_link(file_id))
            elif data_file.get_type() == Type.FASTQ:
                self.__add_fastq_file_details(details, sample_id, self.add_link(file_id))
        else:
            self.__add_metrics_details(details, self.add_link(file_id))
        self.record.set_details(details)

    @staticmethod
    def __add_data_file_details(details, sample_id, file_link):
        if SentinelBase.DATA_KEY not in details:
            details[SentinelBase.DATA_KEY] = {}
        data_details = details[SentinelBase.DATA_KEY]
        if sample_id not in data_details:
            data_details[sample_id] = []
        data_details[sample_id].append(file_link)

    @staticmethod
    def __add_fastq_file_details(details, sample_id, file_link):
        if SentinelBase.FASTQ_KEY not in details:
            details[SentinelBase.FASTQ_KEY] = {}
        data_details = details[SentinelBase.FASTQ_KEY]
        if sample_id not in data_details:
            data_details[sample_id] = []
        data_details[sample_id].append(file_link)

    @staticmethod
    def __add_metrics_details(details, file_link):
        if SentinelBase.METRICS_KEY not in details:
            details[SentinelBase.METRICS_KEY] = []
        details[SentinelBase.METRICS_KEY].append(file_link)


class RawSentinel(SentinelBase):
    def add_file(self, data_file, file_id):
        pass
