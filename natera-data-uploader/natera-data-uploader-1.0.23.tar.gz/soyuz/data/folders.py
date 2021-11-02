#!/usr/bin/env python

import logging
import os
import re
import time
from abc import ABCMeta, abstractmethod

from soyuz.data.files import WesDataFile, RawDataFile, QcDataFile, PersonalisDataFile, PersonalisQcDataFile
from soyuz.utils import UploaderException


class WatchDirectory(object):
    UPLOADED_FILE = ".uploaded"

    def __init__(self, path):
        self.__path = path

    def is_uploaded(self, folder):
        return str(folder) in self.__read_file(self.__uploaded_file)

    def complete(self, folder):
        self.__write_file(self.__uploaded_file, str(folder))

    @property
    def __uploaded_file(self):
        return os.path.join(self.__path, self.UPLOADED_FILE)

    @property
    def __copied_file(self):
        return os.path.join(self.__path, self.COPIED_FILE)

    def get_seq_folders(self):
        return self.__get_seq_folders(self.__path)

    def __get_seq_folders(self, root):
        result = []
        if not os.path.exists(root):
            logging.error("Watch directory {} doesn't exist".format(root))
            return result

        for f in os.listdir(root):
            path = os.path.join(root, f)
            if os.path.isdir(path):
                seq_folder = SeqFolderFactory.create(root, f)
                if seq_folder:
                    result.append(seq_folder)
                else:
                    result += self.__get_seq_folders(path)
        return result

    @staticmethod
    def __read_file(file_with_history):
        result = []
        if not os.path.isfile(file_with_history):
            return result
        with open(file_with_history, "r") as f:
            for line in f.readlines():
                result.append(line.strip())
        return result

    @staticmethod
    def __write_file(file_with_history, seq_folder_name):
        with open(file_with_history, "a") as f:
            f.write(seq_folder_name)


class SeqFolderBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, path):
        self._path = self.__get_abs_path(path).replace("\\", "/")

    def get_name(self):
        return os.path.basename(self._path)

    def get_path(self):
        return self._path

    @property
    @abstractmethod
    def is_valid(self):
        raise NotImplementedError()

    @property
    def is_uploading(self):
        return os.path.isfile(self._path + ".uploading")

    @property
    @abstractmethod
    def is_completed(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def complete(self):
        raise NotImplementedError()

    def is_older_than(self, seconds):
        return time.time() - os.path.getmtime(self.__str__()) > seconds

    @abstractmethod
    def list_files(self):
        raise NotImplementedError()

    @staticmethod
    def __get_abs_path(path):
        abs_path = os.path.abspath(os.path.expanduser(path))
        if not os.path.isdir(abs_path):
            raise UploaderException("{} does not exist".format(abs_path))
        return abs_path


class WesSignateraSeqFolder(SeqFolderBase):
    FOLDER_REGEX = re.compile("[A-Z0-9]*_[0-9]{8}")

    def __init__(self, path):
        SeqFolderBase.__init__(self, path)
        self.__wes_subfolder = os.path.join(self._path, "WES_data")
        self.__qc_subfolder = os.path.join(self._path, "QC_reports")

    @property
    def is_valid(self):
        if WesSignateraSeqFolder.FOLDER_REGEX.match(self.get_name()) is None \
                or not os.path.isdir(self.__wes_subfolder) \
                or not os.path.isdir(self.__qc_subfolder):
            return False

        if len(self.__list_from_wes()) == 0:
            logging.info("{} does not contain any data".format(self.__wes_subfolder))
            return False
        if len(self.__list_from_qc_reports()) == 0:
            logging.info("{} does not contain any data".format(self.__qc_subfolder))
            return False

        success = True
        for f in self.list_files():
            if not f.is_valid:
                logging.info("{} has invalid format".format(f.get_full_path()))
                success = False
        return success

    def list_files(self):
        return self.__list_from_wes() + self.__list_from_qc_reports()

    def __list_from_wes(self):
        result = []
        for f in os.listdir(self.__wes_subfolder):
            result.append(WesDataFile(self.__wes_subfolder, f, self))
        return result

    def __list_from_qc_reports(self):
        result = []
        for f in os.listdir(self.__qc_subfolder):
            result.append(QcDataFile(self.__qc_subfolder, f, self))
        return result


class PersonalisSeqFolder(SeqFolderBase):
    FOLDER_REGEX = re.compile("[A-Za-z0-9_-]{1,48}")

    def __init__(self, path):
        SeqFolderBase.__init__(self, path)
        self.__alignment_subfolder = os.path.join(self._path, '{}', "Alignment")
        self.__fastq_subfolder = os.path.join(self._path, '{}', "FASTQ")
        self.__qc_metrics_path = self._path

    @property
    def is_valid(self):
        if PersonalisSeqFolder.FOLDER_REGEX.match(self.get_name()) is None:
            return False

        if len(self.__list_qc_metrics(self._path)) == 0:
            logging.info("{} does not contain any data".format(self.__qc_metrics_path))
            return False

        for folder in os.listdir(self._path):
            if not os.path.isdir(os.path.join(self._path, folder)):
                continue
            if not os.path.isdir(self.__alignment_subfolder.format(folder)):
                return False
            if len(self.__list_from(self.__alignment_subfolder.format(folder))) == 0:
                logging.info("{} does not contain any data".format(self.__alignment_subfolder))
                return False
            if os.path.isdir(self.__fastq_subfolder.format(folder)) and \
                    len(self.__list_from(self.__fastq_subfolder.format(folder))) == 0:
                logging.info("{} does not contain any data".format(self.__fastq_subfolder))
                return False

        success = True
        for f in self.list_files():
            if not f.is_valid:
                logging.info("{} has invalid format".format(f.get_full_path()))
                success = False
        return success

    def list_files(self):
        list_files = self.__list_qc_metrics(self._path)
        for folder in os.listdir(self._path):
            if not os.path.isdir(os.path.join(self._path, folder)):
                continue
            list_files.extend(self.__list_from(self.__alignment_subfolder.format(folder)))
            if os.path.isdir(self.__fastq_subfolder.format(folder)):
                list_files.extend(self.__list_from(self.__fastq_subfolder.format(folder)))
        return list_files

    def __list_from(self, subfolder):
        result = []
        for f in os.listdir(subfolder):
            result.append(PersonalisDataFile(subfolder, f, self))
        return result

    def __list_qc_metrics(self, path):
        result = []
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)):
                result.append(PersonalisQcDataFile(path, f, self))
        return result


class RawSeqFolder(SeqFolderBase):
    def __init__(self, path):
        super(RawSeqFolder, self).__init__(path)

    @property
    def is_valid(self):
        return True

    def list_files(self):
        result = []
        for root, subdirs, files in os.walk(self._path):
            for f in files:
                result.append(RawDataFile(root, f, self))
        return result


class BgiSeqFolder(SeqFolderBase):
    FOLDER_REGEX = re.compile("V[A-Za-z0-9]{9}")

    def __init__(self, path):
        super(BgiSeqFolder, self).__init__(path)
        self.__lane_folders = [os.path.join(self._path, lane) for lane in ["L01", "L02", "L03", "L04"]]
        self.__wes_subfolder = os.path.join(self._path, "WES_data")
        self.__qc_subfolder = os.path.join(self._path, "QC_reports")

    @property
    def is_completed(self):
        if self.is_valid:
            return all([os.path.isfile(os.path.join(lane_folder, "{}_{}_FileInfo.csv".format(os.path.basename(self._path), os.path.basename(lane_folder)))) for lane_folder in self.__lane_folders])
        return False

    @property
    def is_valid(self):
        if (BgiSeqFolder.FOLDER_REGEX.match(self.get_name())
                and all([os.path.join(self._path, folder) in self.__lane_folders for folder in os.listdir(self._path) if os.path.isdir(os.path.join(self._path, folder))])):
            return True
        return False

    def list_files(self):
        result = []
        for root, subdirs, files in os.walk(self._path):
            for f in files:
                result.append(RawDataFile(root, f, self))
        return result


class SeqFolderFactory(object):
    @staticmethod
    def create(base_path, name):
        if BgiSeqFolder.FOLDER_REGEX.match(name):
            return BgiSeqFolder(os.path.join(base_path, name))
        if WesSignateraSeqFolder.FOLDER_REGEX.match(name):
            return WesSignateraSeqFolder(os.path.join(base_path, name))
        logging.error("Folder {} is not allowed.".format(os.path.join(base_path, name)))
        return None

    @staticmethod
    def create_from_full_path(full_path):
        base_path, name = SeqFolderFactory.__parse_full_path(full_path)
        return SeqFolderFactory.create(base_path, name)

    @staticmethod
    def __parse_full_path(full_path):
        path = full_path.rstrip('/')
        return os.path.dirname(path), os.path.basename(path)
