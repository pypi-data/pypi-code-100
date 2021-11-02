#!/usr/bin/env python

from abc import ABCMeta, abstractmethod
import logging
import os
import requests
import subprocess

import dxpy

from soyuz.utils import UploaderException, read_in_chunks


class Storage(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.set_context()

    @abstractmethod
    def set_context(self):
        raise NotImplementedError()

    @abstractmethod
    def validate_target_dir(self):
        raise NotImplementedError()

    @abstractmethod
    def upload_file(self):
        raise NotImplementedError()


class DNAnexusStorage(Storage):
    NAME = "dnanexus"

    def __init__(self, settings):
        self.basedir = settings.get_base_dir()
        self.token = settings.get_token()
        self.ua_path = settings.get_ua_path()
        self.ua_parameters = settings.get_ua_parameters()
        super(DNAnexusStorage, self).__init__()

    def set_context(self):
        if not self.token:
            raise UploaderException("Token was not specified")
        dxpy.set_security_context({'auth_token_type': 'Bearer', 'auth_token': self.token})
        projects = self.__get_projects()
        size = len(projects)
        if size == 0 or size > 1:
            raise UploaderException("Auth Token must have access to exactly 1 project with UPLOAD permission.")
        self.__project = projects[0]
        dxpy.set_project_context(self.__project)
        dxpy.set_workspace_id(self.__project)

    def get_project_id(self):
        return self.__project

    def get_project(self):
        return dxpy.DXProject(self.get_project_id())

    def get_file_by_id(self, file_id):
        return dxpy.get_handler(file_id)

    @staticmethod
    def __get_projects():
        result = []
        try:
            for project in dxpy.bindings.search.find_projects(level='UPLOAD'):
                result.append(str(project['id']))
        except dxpy.exceptions.InvalidAuthentication:
            pass
        return result

    def validate_target_dir(self, folder):
        if not folder.is_valid:
            raise UploaderException(
                    "{} is not valid".format(folder.get_name()))
        project = dxpy.DXProject(self.get_project_id())
        try:
            entities = project.list_folder(os.path.join(self.basedir, folder.get_name()))
            if len(entities["objects"]) > 0 or len(entities["folders"]) > 0:
                raise UploaderException(
                    "{} already exists under {}".format(folder.get_name(), self.basedir))
        except dxpy.exceptions.ResourceNotFound:
            pass

    def upload_file(self, data_file, remote_folder, types, properties):
        logging.info("Uploading {} to {}".format(data_file.get_full_path(), remote_folder))
        dx_file = dxpy.upload_local_file(data_file.get_full_path(),
                                         folder=remote_folder,
                                         keep_open=True,
                                         parents=True)
        if dx_file:
            dx_file.add_types(types)
            dx_file.set_properties(properties)
            dx_file.close()
        else:
            raise UploaderException("Failed to upload {}".format(data_file.get_full_path()))
        return dx_file.get_id()


class DNAnexusStorageUA(DNAnexusStorage):
    def upload_file(self, data_file, remote_folder, types, properties):
        logging.info("Uploading {} to {}".format(data_file.get_full_path(), remote_folder))
        args = [r'"{}"'.format(self.ua_path), data_file.get_full_path().replace("(", "\(").replace(")", "\)")]
        args.extend(["--auth-token", self.token])
        args.extend(["-p", self.get_project_id()])
        args.extend(["-f", remote_folder])
        args.extend([self.ua_parameters])
        args.extend(["--type {}".format(_type) for _type in types])
        args.extend(["--property {}={}".format(key, val) for key, val in properties.items()])
        file_id = subprocess.check_output(" ".join(args), shell=True).strip().decode('utf8').replace("'", '"')
        return file_id


class ExodusStorage(Storage):
    NAME = "exodus"

    def __init__(self, settings):
        self.basedir = settings.get_base_dir()
        self.exodus_url = settings.get_exodus_url()
        self.exodus_username = settings.get_exodus_username()
        self.exodus_password = settings.get_exodus_password()
        self.chunk_size = settings.get_chunk_size()
        super(ExodusStorage, self).__init__()

    def set_context(self):
        if not self.exodus_url:
            raise UploaderException("Exodus URL was not specified")

    def validate_target_dir(self, folder):
        if not folder.is_valid:
            raise UploaderException(
                    "{} is not valid".format(folder.get_name()))

    def upload_file(self, data_file, remote_folder, types, properties):
        logging.info("Uploading {} to {}".format(data_file.get_full_path(), remote_folder))
        data = {'name': data_file.get_name(),
                'folder': remote_folder,
                'types': types,
                'properties': properties,
                'tags': []}
        response = requests.post(os.path.join(self.exodus_url, "2.0/data/files/new"), json=data, auth=(self.exodus_username, self.exodus_password))
        response.raise_for_status()
        data = response.json()
        file_id = data['file']['link']
        uploadId = data['uploadId']

        with open(data_file.get_full_path(), 'rb') as file_object:
            parts = []
            for i, chunk in enumerate(read_in_chunks(file_object, self.chunk_size)):
                data = {'file': {
                            'link': file_id},
                        'uploadId': uploadId,
                        'part': i+1}
                response = requests.post(os.path.join(self.exodus_url, "2.0/data/files/part-upload"), json=data, auth=(self.exodus_username, self.exodus_password))
                response.raise_for_status()
                data = response.json()
                uploadUrl = data['uploadUrl']

                response = requests.put(uploadUrl, data=chunk)
                response.raise_for_status()
                headers = response.headers
                etag = headers['ETag']
                parts.append({'eTag': etag,
                              'part': i+1})

        data = {'file': {
                    'link': file_id},
                'uploadId': uploadId,
                'contentLength': os.path.getsize(data_file.get_full_path()),
                'parts': parts
                }
        response = requests.post(os.path.join(self.exodus_url, "2.0/data/files/finish-upload"), json=data, auth=(self.exodus_username, self.exodus_password))
        response.raise_for_status()
        data = response.json()
        file_id = data['link']
        logging.info("Successfully uploaded: {} to {}".format(data_file.get_full_path(), remote_folder))
        return file_id


class StorageType(object):
    DNANEXUS = DNAnexusStorage.NAME
    EXODUS = ExodusStorage.NAME
    DEFAULT = DNANEXUS
    ALL = [DNANEXUS, EXODUS]


class StorageFactory(object):
    @staticmethod
    def create(settings):
        if settings.get_storage() == DNAnexusStorage.NAME:
            return DNAnexusStorageUA(settings) if settings.get_ua_path() else DNAnexusStorage(settings)
        elif settings.get_storage() == ExodusStorage.NAME:
            return ExodusStorage(settings)
        raise UploaderException("Storage with name {} was not found".format(settings.get_storage()))
