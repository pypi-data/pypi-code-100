#!/usr/bin/env python

import logging
import csv
import os
import re
from abc import ABCMeta, abstractmethod

from soyuz.dx.variables import Type


class DataFile(object):
    __metaclass__ = ABCMeta

    def __init__(self, location, name, seq_folder):
        self.__location = location
        self.__name = name
        self.__seq_folder = seq_folder

    def get_location(self):
        return self.__location

    def get_name(self):
        return self.__name

    @property
    def is_valid(self):
        return bool(self.get_regex().match(self.get_name()))

    def get_seq_folder_name(self):
        return self.__seq_folder.get_name()

    def get_relative_path(self):
        relpath = os.path.relpath(self.get_location(), self.__seq_folder.get_path())
        if relpath == ".":
            return ""
        return relpath

    def get_full_path(self):
        return os.path.join(self.__location, self.__name)

    @abstractmethod
    def get_type(self):
        raise NotImplementedError()

    @abstractmethod
    def get_regex(self):
        raise NotImplementedError()

    @abstractmethod
    def get_sample_id(self):
        raise NotImplementedError()


class RawDataFile(DataFile):
    def get_sample_id(self):
        return None

    def get_type(self):
        return None

    def get_regex(self):
        return re.compile(".+?")


class WesDataFile(DataFile):
    def get_regex(self):
        return re.compile("(?P<sample_id>[A-Za-z0-9-.]*)_[A-Za-z0-9-_]*.(?P<extension>fastq.gz|fastq|bam)")

    def get_type(self):
        m = self.get_regex().match(self.get_name())
        if m:
            extension = m.group("extension")
            if extension == "fastq.gz" or extension == "fastq":
                return Type.FASTQ
            if extension == "bam":
                return Type.BAM
        return None

    def get_sample_id(self):
        m = self.get_regex().match(self.get_name())
        if m:
            return m.group("sample_id")
        return None


class PersonalisDataFile(DataFile):
    def get_regex(self):
        return re.compile("[A-Za-z0-9-]*_(?P<sample_id>[A-Za-z0-9-.]*)_[A-Za-z0-9-_.]*.(?P<extension>fastq.gz|fastq|bam)")

    def get_type(self):
        m = self.get_regex().match(self.get_name())
        if m:
            extension = m.group("extension")
            if extension == "fastq.gz" or extension == "fastq":
                return Type.FASTQ
            if extension == "bam":
                return Type.BAM
        return None

    def get_sample_id(self):
        m = self.get_regex().match(self.get_name())
        if m:
            return m.group("sample_id")
        return None


class QcDataFile(DataFile):
    @property
    def is_valid(self):
        if not super(QcDataFile, self).is_valid:
            return False

        if self.get_type() == Type.CSV:
            sniffer = csv.Sniffer()
            with open(self.get_full_path(), 'r') as f:
                data = f.read()
            if sniffer.sniff(data).delimiter != ',':
                logging.error("CSV file {}: expected a comma delimiter, but actual is {}.".format(self.get_full_path(), sniffer.sniff(data).delimiter))
                return False
            if not sniffer.has_header(data):
                logging.error("CSV file {} doesn't have a header.".format(self.get_full_path()))
                return False
            with open(self.get_full_path(), 'r') as f:
                for line in csv.DictReader(f):
                    if not re.compile("^[a-zA-Z0-9\\-_.]+$").match(line['Natera Sample ID']):
                        logging.error("CSV file {} doesn't have a valid 'Natera Sample ID'.".format(self.get_full_path()))
                        return False
                    if not line['aveDedupOnTarget']:
                        logging.error("CSV file {} doesn't have an 'aveDedupOnTarget'.".format(self.get_full_path()))
                        return False
                    metrics = ["Total recovery (ug)", "%gDNA", "A260/A280", "Library into Capture (ng)", "PreCap BioA size (bp)", "Post capture Library concentration (ng/uL)", "PostCap BioA size (bp)", "totReads", "totPairedReads", "averageBaseQ", "combinedQ30pct", "r1Q30pct", "r2Q30pct", "mapq", "pctAlignedToGenome", "gcPCT", "pctDuplicate", "pctOnPanel"]
                    for key, val in line.items():
                        if key in metrics and not val:
                            logging.warning("CSV file {} doesn't have a metric {} defined.".format(self.get_full_path(), key))
                    if line["% Tumor Fraction"] and not line["ffpe100x"]:
                        logging.warning("CSV file {} doesn't have 'ffpe100x' defined.".format(self.get_full_path()))
                    if not line["% Tumor Fraction"] and not line["norm30x"]:
                        logging.warning("CSV file {} doesn't have 'norm30x' defined.".format(self.get_full_path()))
        return True

    def get_regex(self):
        return re.compile("[A-Za-z0-9-_ ]*.(?P<extension>csv|pdf|xlsx)")

    def get_type(self):
        m = self.get_regex().match(self.get_name())
        if m:
            extension = m.group("extension")
            if extension == "csv":
                return Type.CSV
            if extension == "pdf":
                return Type.PDF
            if extension == "xlsx":
                return Type.XLSX
        return None

    def get_sample_id(self):
        return None


class PersonalisQcDataFile(QcDataFile):
    @property
    def is_valid(self):
        if not super(QcDataFile, self).is_valid:
            return False

        if self.get_type() == Type.CSV:
            sniffer = csv.Sniffer()
            with open(self.get_full_path(), 'r') as f:
                data = f.read()
            if sniffer.sniff(data).delimiter != ',':
                logging.error("CSV file {}: expected a comma delimiter, but actual is {}.".format(self.get_full_path(), sniffer.sniff(data).delimiter))
                return False
            if not sniffer.has_header(data):
                logging.error("CSV file {} doesn't have a header.".format(self.get_full_path()))
                return False
            with open(self.get_full_path(), 'r') as f:
                for line in csv.DictReader(f):
                    if not re.compile("^[a-zA-Z0-9\\-_.]+$").match(line['Natera Sample ID']):
                        logging.error("CSV file {} doesn't have a valid 'Natera Sample ID'.".format(self.get_full_path()))
                        return False
                    if not line['aveDedupOnTarget']:
                        logging.error("CSV file {} doesn't have an 'aveDedupOnTarget'.".format(self.get_full_path()))
                        return False
                    metrics = ["% Tumor Fraction", "extraction_ng", "DIN", "Q30_reads", "mapQ", "pct_reads_mapped", "pct_GC", "duplication_rate", "cap_spec", "aveDedupOnTarget", "f_above_30x", "f_above_100x"]
                    for key, val in line.items():
                        if key in metrics and not val:
                            logging.warning("CSV file {} doesn't have a metric {} defined.".format(self.get_full_path(), key))
        return True
