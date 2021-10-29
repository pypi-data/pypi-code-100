import configparser
import csv
import os
from configparser import ConfigParser
from enum import IntEnum
from functools import partial
from logging import getLogger
from typing import List, Callable, Optional

import grpc
import requests
from authlib.oauth2.rfc6749 import OAuth2Token

from ._grpc import ApiCommon_pb2, ApiService_pb2, Constants_pb2
from ._grpc.ApiCommon_pb2 import FileDetails, ResponseStatus
from ._grpc.ApiService_pb2 import UploadAnnotationsResponse, DeleteTaskResponse, UploadDataResponse, \
    DeleteDatasetResponse, GetProjectsResponse, HelloWorldResponse, HelloWorldRequest, DeleteProjectResponse, \
    DeleteDatasetRequest, DeleteTaskRequest, CreateProjectResponse
from ._grpc.ApiService_pb2_grpc import ApiServiceStub
from .auth import InnoAuthClient
from .interceptor import MetadataClientInterceptor
from .helpers import deprecated, check_for_yanked_release, check_for_updates

log = getLogger('innotescus')


class StorageType(IntEnum):
    FILE_SYSTEM = Constants_pb2.FILE_SYSTEM
    URL = Constants_pb2.URL


class DataType(IntEnum):
    IMAGE = ApiCommon_pb2.IMAGE
    VIDEO = ApiCommon_pb2.VIDEO


class AnnotationFormat(IntEnum):
    COCO = Constants_pb2.COCO
    COCO_WITH_METADATA = Constants_pb2.COCO_WITH_METADATA
    MASKS_PER_CLASS = Constants_pb2.MASKS_PER_CLASS
    PASCAL = Constants_pb2.PASCAL
    CSV = Constants_pb2.CSV
    MASKS_SEMANTIC = Constants_pb2.MASKS_SEMANTIC
    MASKS_INSTANCE = Constants_pb2.MASKS_INSTANCE
    INNOTESCUS_JSON = Constants_pb2.INNOTESCUS_JSON
    KITTI = Constants_pb2.KITTI
    YOLO_DARKNET = Constants_pb2.YOLO_DARKNET
    YOLO_KERAS = Constants_pb2.YOLO_KERAS


class TaskType(IntEnum):
    CLASSIFICATION = Constants_pb2.CLASSIFICATION
    OBJECT_DETECTION = Constants_pb2.OBJECT_DETECTION
    SEGMENTATION = Constants_pb2.SEGMENTATION
    INSTANCE_SEGMENTATION = Constants_pb2.INSTANCE_SEGMENTATION


class ExportType(IntEnum):
    DATASETS = Constants_pb2.DATASETS
    ANNOTATIONS = Constants_pb2.ANNOTATIONS


class JobStatus(IntEnum):
    PENDING = Constants_pb2.PENDING
    SUCCEEDED = Constants_pb2.SUCCEEDED
    FAILED = Constants_pb2.FAILED
    CANCELLED = Constants_pb2.CANCELLED


class ResponseCode(IntEnum):
    STATUS_UNSPECIFIED = ApiCommon_pb2.STATUS_UNSPECIFIED
    SUCCESS = ApiCommon_pb2.SUCCESS
    FAILED = ApiCommon_pb2.FAILED
    DUPLICATE_NAME = ApiCommon_pb2.DUPLICATE_NAME
    EMPTY_BYTE_LENGTH = ApiCommon_pb2.EMPTY_BYTE_LENGTH
    STORAGE_EXCEEDED = ApiCommon_pb2.STORAGE_EXCEEDED
    NOT_FOUND = ApiCommon_pb2.NOT_FOUND


class InnoApiClient:
    """ Client for communicating with the Innotescus API.
    """
    def __init__(self, channel_factory_: Callable[[], grpc.Channel], auth_client: InnoAuthClient, api_base_url: str, verify_ssl: bool = True):
        """
        :param `Callable[[], grpc.Channel]` channel_factory_: factory function that returns a Channel for connecting
            to the Innotescus API
        :param auth_client:
        :param api_base_url:
        :param verify_ssl:
        """
        self.channel_factory = channel_factory_
        self.auth_client = auth_client
        self.verify_ssl = verify_ssl
        self.channel: Optional[grpc.Channel] = None
        self.upload_url = f'{api_base_url}/api/upload'
        self.upload_annotations_url = f'{api_base_url}/api/upload/annotations'

    @property
    def _token(self) -> OAuth2Token:
        """ Gets the current API token.  If the currently-downloaded token is expired
        or hasn't yet been fetched, an API call will be made.
        """
        return self.auth_client.fetch_access_token()

    def _connect_to_server(self) -> ApiServiceStub:
        """ Blocking call that will make sure the channel connection
        is ready and then build the GRPC api stub.
        :return: the GRPC API Stub
        """
        try:
            if not self.channel:
                self.channel = self.channel_factory()
            grpc.channel_ready_future(self.channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            raise
        else:
            return ApiServiceStub(self.channel)

    def hello_world(self) -> HelloWorldResponse:
        """ Verify your connection to the server is working.
        """
        stub = self._connect_to_server()
        message = HelloWorldRequest(hello_world="hello")
        response = stub.HelloWorld.with_call(message)
        if (response is not None and
            response[0] is not None):
            return response[0]

        return HelloWorldResponse(status=ResponseStatus(code=ApiCommon_pb2.FAILED))

    def get_projects(self):
        """ Get a list of projects, tasks, and associated datasets.
        """
        stub = self._connect_to_server()
        message = ApiService_pb2.GetProjectsRequest()
        response = stub.GetProjects.with_call(message)
        if (response is not None and
            response[0] is not None and
            response[0].projects is not None and
            response[0].projects[0] is not None):
            return response[0]

        return ApiService_pb2.GetProjectsResponse(projects=[], status=ApiCommon_pb2.ResponseStatus(code=ApiCommon_pb2.FAILED))

    def get_project_by_name(self, project_name: str) -> GetProjectsResponse:
        """ Query a project, its tasks, and associated datasets based on the project's name

        :param project_name: (Required) the name of the project
        :return: the details of the project along with its associated tasks and datasets
        """
        stub = self._connect_to_server()
        message = ApiService_pb2.GetProjectsRequest(project_name=project_name)
        response = stub.GetProjects.with_call(message)
        if (response is not None and
            response[0] is not None and
            response[0].projects is not None and
            response[0].projects[0] is not None):
            return response[0]

        return GetProjectsResponse(status=ResponseStatus(code=ApiCommon_pb2.FAILED))

    def create_project(self, project_name: str) -> CreateProjectResponse:
        """ Create a project

        :param `str` project_name: (Required) the name of the project to be created
        :return: the status of the request
        """
        stub = self._connect_to_server()
        message = ApiService_pb2.CreateProjectRequest(project_name=project_name)
        response = stub.CreateProject.with_call(message)
        if (response is not None and
                response[0] is not None and
                response[0]):
            return response[0]

        return ApiService_pb2.CreateProjectResponse(status=ApiCommon_pb2.ResponseStatus(code=ApiCommon_pb2.FAILED))

    def create_task(self,
                    project_name: str,
                    task_name: str,
                    task_type: TaskType,
                    data_type: DataType,
                    classes: List[str],
                    datasets,
                    task_description,
                    instructions,
                    can_annotator_add_classes):
        """ Create a task with optionally associated datasets and classes.

        :param project_name: (Required) the name of the project this dataset will be associated with
        :param task_name: (Required) the desired name of the task
        :param task_type: (Required) the type of annotation we are doing in this task (Classification, Object Detection, Segmentation, etc.)
        :param data_type: (Required) the type of data this task will be associated with (Image, Video, etc.)
        :param classes: (Optional) a list of classes that will be created with this task
        :param datasets: (Optional) a list of existing datasets from this project that will be assigned to this task to complete this task's work on
        :param task_description: (Optional) a description of this task
        :param instructions: (Optional) instructions for the annotators of this task
        :param can_annotator_add_classes: (Optional) whether or not annotators of this task should be allowed to add classes to it
        :return: the status of the request
        """
        stub = self._connect_to_server()
        if not classes:
            can_annotator_add_classes = True
        message = ApiService_pb2.CreateTaskRequest(project_name=project_name,
                                                   name=task_name,
                                                   description=task_description,
                                                   task_type=task_type,
                                                   data_type=data_type,
                                                   classes=classes,
                                                   dataset_names=datasets,
                                                   can_annotator_add_classes=can_annotator_add_classes
                                                   )
        response = stub.CreateTask.with_call(message)
        if (response is not None and
                response[0] is not None and
                response[0]):
            return response[0]

        return ApiService_pb2.CreateTaskResponse(status=ApiCommon_pb2.ResponseStatus(code=ApiCommon_pb2.FAILED))

    def assign_task_to_datasets(self, project_name, assignments):
        """ Assign datasets to tasks so that the task's work will be performed on these datasets

        :param project_name: (Required) the name of the project these datasets and tasks live within
        :param assignments: (Required) a list of dataset <-> task mappings that will be created
        :return: the status of the request
        """
        stub = self._connect_to_server()
        message = ApiService_pb2.AssignTaskToDatasetsRequest(project_name=project_name,
                                                             assignments=assignments,
                                                             )
        response = stub.AssignTaskToDatasets.with_call(message)
        if (response is not None and
                response[0] is not None and
                response[0]):
            return response[0]

        return ApiService_pb2.AssignTaskToDatasetsResponse(status=ApiCommon_pb2.ResponseStatus(code=ApiCommon_pb2.FAILED))

    def upload_data(self, project_name, dataset_name, file_paths,  data_type: DataType, storage_type: StorageType):
        """ Upload data to a new or pre-existing dataset

        :param project_name: the project name associated with the dataset being uploaded to
        :param dataset_name: the name of the dataset data is being uploaded to
        :param file_paths: a list of file paths intended to be uploaded
        :param data_type: the type of data this dataset will hold (Image, Video, etc.)
        :param storage_type: the source this data is coming from (e.g., Filesystem or URL)
        :return: the status of the request, an import id associated with this job, and the amount of storage in mb currently being used and currently allowed
        """
        pb_files = []
        request_files = []
        if storage_type is StorageType.FILE_SYSTEM:
            for f in file_paths:
                pb_file = FileDetails(name=os.path.basename(f), size=os.path.getsize(f))
                pb_files.append(pb_file)
        elif storage_type is StorageType.URL:
            for f in file_paths:
                with open(f, newline='') as csvfile:
                    csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                    for row in csv_reader:
                        pb_file = FileDetails(name=row[0], resource=row[1])
                        pb_files.append(pb_file)

        req = ApiService_pb2.UploadDataRequest(project_name=project_name,
                                               dataset_name=dataset_name,
                                               data_type=data_type,
                                               storage_type=storage_type,
                                               files=pb_files)
        serialized_req = req.SerializeToString()

        files = [eval(f'("{os.path.basename(file)}", open(r"{file}", "rb"))') for file in file_paths]

        response = requests.post(self.upload_url,
                                 headers={'Authorization': 'Bearer ' + self._token['access_token']},
                                 files=files,
                                 data={'request': serialized_req},
                                 verify=self.verify_ssl)
        if response is not None and response.content is not None:
            # class_ = getattr(import_module('innotescus.ApiService_pb2'), 'UploadDataResponse')
            # rv = class_()
            rv = UploadDataResponse()
            rv.ParseFromString(response.content)
            return rv

        return ApiService_pb2.UploadDataResponse(
            status=ApiCommon_pb2.ResponseStatus(code=ApiCommon_pb2.FAILED, message="Data failed to upload."))

    def upload_annotations(self,
                           project_name: str,
                           dataset_name: str,
                           task_type: TaskType,
                           data_type: DataType,
                           annotation_format: AnnotationFormat,
                           file_paths: List[str],
                           task_name: str,
                           task_description: str,
                           overwrite_existing_annotations: bool = False) -> UploadAnnotationsResponse:
        """ Upload annotations to a new or existing dataset

        :param `str` project_name: (Required) the project name associated with the dataset being uploaded to
        :param `str` dataset_name: (Required) the name of the dataset these annotations are being uploaded to
        :param `TaskType` task_type: (Required) the type of annotation that has been done to create these annotations (Classification, Object Detection, Segmentation, etc.)
        :param `DataType` data_type: (Required) the type of data this dataset will hold (Image, Video, etc.)
        :param `AnnotationFormat` annotation_format: (Required) The format in which these annotations are stored (Coco, Masks per class, Instance Masks, etc.)
        :param `List[str]` file_paths: (Required) a list of file paths containing the annotations to upload
        :param `str` task_name: (Required) the name of the task these annotations are being uploaded to (if it does not exist it will be created)
        :param `str` task_description: (Optional) an optional description for the task if it does not exist yet
        :param `bool` overwrite_existing_annotations: (Optional) if the task already exists, choose whether or not to overwrite existing annotations
        :return: the status of the request, an import id associated with this job, and the amount of storage in mb currently being used and currently allowed
        """
        pb_files = []
        request_files = []
        for f in file_paths:
            pb_file = FileDetails(name=os.path.basename(f), size=os.path.getsize(f))
            pb_files.append(pb_file)

        req = ApiService_pb2.UploadAnnotationsRequest(project_name=project_name,
                                                      dataset_name=dataset_name,
                                                      task_name=task_name,
                                                      task_type=task_type,
                                                      data_type=data_type,
                                                      annotation_format=annotation_format,
                                                      task_description=task_description,
                                                      overwrite_existing_annotations=overwrite_existing_annotations,
                                                      files=pb_files)
        serialized_req = req.SerializeToString()

        files = [eval(f'("{os.path.basename(file)}", open(r"{file}", "rb"))') for file in file_paths]

        response = requests.post(self.upload_annotations_url,
                                 headers={'Authorization': 'Bearer ' + self._token['access_token']},
                                 files=files,
                                 data={'request': serialized_req},
                                 verify=self.verify_ssl)
        if response is not None and response.content is not None:
            rv = UploadAnnotationsResponse()
            rv.ParseFromString(response.content)
            return rv

        return ApiService_pb2.UploadAnnotationsResponse(
            status=ApiCommon_pb2.ResponseStatus(code=ApiCommon_pb2.FAILED, message="Annotations failed to upload."))

    def export(self, export_name, project_name, annotation_format: AnnotationFormat, export_types, dataset_names, task_name):
        """ Start an export and return an associated job_id the associated job id can be used to query the status of
        the export job exports can be downloaded using the download_annotations() method when the export is complete

        :param export_name: (Required) a name to reference the export, used for
            downloading & viewing in the Innotescus web client
        :param project_name: (Required) the name of the project we're exporting from
        :param annotation_format: (Required) the format of the annotations we're exporting, e.g. coco,
            masks_semantic, etc.)
        :param export_types: (Required) the type of this export (e.g., Datasets, Annotations, Datasets with Annotations)
        :param dataset_names: (Required if task_name is empty) the name of the datasets we're exporting from
        :param task_name: (Required if dataset_name is empty) the name of the task we're exporting from
        :return: the status of the request and an export id associated with this job
        """
        stub = self._connect_to_server()
        message = ApiService_pb2.StartExportRequest(
                                                        export_name=export_name,
                                                        project_name=project_name,
                                                        dataset_names=dataset_names,
                                                        task_name=task_name,
                                                        annotation_format=annotation_format,
                                                        export_types=export_types)
        response = stub.StartExport.with_call(message)
        if (response is not None and
                response[0] is not None and
                response[0]):
            return response[0]

        return ApiService_pb2.StartExportResponse(status=ApiCommon_pb2.ResponseStatus(code=ApiCommon_pb2.FAILED))

    def download_export(self, job_id, download_path):
        """ Downloads the data associated with a completed export job

        :param job_id: (Required) the job id associated with this export
        :param download_path: (Required) the path to download the resulting export to
        :return: the status of the request after the files have been written to the requested download path
        """
        stub = self._connect_to_server()
        message = ApiService_pb2.DownloadExportRequest(job_id=job_id)
        response = stub.DownloadExport.with_call(message)
        if (response is not None and
                response[0] is not None and
                response[0]):
            response_to_return = {"response_status": response[0].status}
            if response[0].job_status == Constants_pb2.SUCCEEDED:
                r = requests.get(response[0].download_url, allow_redirects=True)
                open(download_path + "/" + response[0].export_name + ".zip", 'wb').write(r.content)

            return response[0]

        return ApiService_pb2.DownloadExportResponse(status=ApiCommon_pb2.ResponseStatus(code=ApiCommon_pb2.FAILED, message="Export download failed."))

    def get_in_progress_jobs(self):
        """ Request a list of all in progress jobs associated with your Innotescus account

        :return: A list of jobs containing their id, status, and type
        """
        stub = self._connect_to_server()
        message = ApiService_pb2.GetInProgressJobsRequest()
        response = stub.GetInProgressJobs.with_call(message)
        if (response is not None and
            response[0] is not None and
            response[0].jobs is not None and
            response[0].jobs[0] is not None):
            return response[0]

        return ApiService_pb2.GetInProgressJobsResponse(status=ApiCommon_pb2.ResponseStatus(code=ApiCommon_pb2.FAILED))

    def get_job_status(self, job_id):
        """ Request the status of a job

        :param job_id: (Required) the id of the job you would like to request the status for
        :return: the status of the request and the status of the job with the requested id
        """
        stub = self._connect_to_server()
        message = ApiService_pb2.GetJobStatusRequest(job_id=job_id)
        response = stub.GetJobStatus.with_call(message)
        if (response is not None and
            response[0] is not None):
            return response[0]

        return ApiService_pb2.GetJobStatusResponse(status=ApiCommon_pb2.ResponseStatus(code=ApiCommon_pb2.FAILED))

    def delete_project(self, project_name: str) -> DeleteProjectResponse:
        """ Delete a project

        :param project_name: (Required) the name of the project you wish to delete
        :return: the status of the request
        """
        stub = self._connect_to_server()
        message = ApiService_pb2.DeleteProjectRequest(project_name=project_name)
        response = stub.DeleteProject.with_call(message)
        if (response is not None and
            response[0] is not None):
            return response[0]

        return DeleteProjectResponse(status=ResponseStatus(code=ApiCommon_pb2.FAILED, message="Failed to delete project."))

    def delete_dataset(self, project_name: str, dataset_name: str) -> DeleteDatasetResponse:
        """ Delete a dataset

        :param project_name: (Required) the name of the project that contains the dataset you wish to delete
        :param dataset_name: (Required) the name the dataset you wish to delete
        :return: the status of the request
        """
        stub = self._connect_to_server()
        message = DeleteDatasetRequest(project_name=project_name, dataset_name=dataset_name)
        response = stub.DeleteDataset.with_call(message)
        if (response is not None and
            response[0] is not None):
            return response[0]

        return DeleteDatasetResponse(status=ResponseStatus(code=ResponseCode.FAILED, message="Failed to delete dataset."))

    def delete_task(self, project_name: str, dataset_name: str) -> DeleteTaskResponse:
        """ Delete a task

        :param project_name: (Required) the name of the project that contains the task you wish to delete
        :param dataset_name: (Required) the name the task you wish to delete
        :return: the status of the request
        """
        stub = self._connect_to_server()
        message = DeleteTaskRequest(project_name=project_name, dataset_name=dataset_name)
        response = stub.DeleteTask.with_call(message)
        if (response is not None and
            response[0] is not None):
            return response[0]

        return DeleteTaskResponse(status=ResponseStatus(code=ResponseCode.FAILED, message="Failed to delete task."))


def channel_factory(inno_config: configparser.SectionProxy, auth_client: InnoAuthClient) -> grpc.Channel:
    """ Constructs a new GRPC channel, based on the config and auth client data.

    :param inno_config:
    :param auth_client:
    :return:
    """
    token = auth_client.fetch_access_token()

    call_credentials = grpc.access_token_call_credentials(token['access_token'])

    channel_url = f'{inno_config.get("server_url")}:{inno_config.get("port")}'

    if inno_config.getboolean('force_insecure_channel'):
        log.warning('Initializing insecure GRPC channel')
        composite_credentials = grpc.composite_channel_credentials(
            grpc.local_channel_credentials(),
            call_credentials
        )
        channel = grpc.secure_channel(channel_url, composite_credentials)  # don't believe the name =)

    else:
        log.info('Initializing secure GRPC channel')
        channel_credentials = grpc.ssl_channel_credentials()
        composite_credentials = grpc.composite_channel_credentials(
            channel_credentials,
            call_credentials
        )
        channel = grpc.secure_channel(
            target=channel_url,
            credentials=composite_credentials,
            options=(
                ('grpc.ssl_target_name_override', 'innotescus.app'),
            )
        )

    intercepted_channel = grpc.intercept_channel(channel, MetadataClientInterceptor())
    return intercepted_channel


def client_factory(client_id=None, client_secret=None) -> InnoApiClient:
    """ Builds and configures a new `InnoApiClient`.

    :param `str` client_id: API credentials (create from web admin)
    :param `str` client_secret: API credentials (create from web admin)
    :return: A configured api client, ready for use
    """

    if not os.getenv('INNO_IS_TEST', '').lower() in ['1', 'yes', 'true']:
        check_for_yanked_release()  # make sure this client version is still supported.
        check_for_updates()  # issue warnings is app version it out-of-date

    cp = ConfigParser()
    _loaded_paths = cp.read([
        os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.ini')),
        os.path.expanduser('~/.innotescus/client.ini'),
        os.getenv('INNO_CONFIG', ''),
    ])
    env_conf = {
        'server_url': os.getenv('INNO_SERVER_URL'),
        'port': os.getenv('INNO_SERVER_PORT'),
        'auth_domain': os.getenv('INNO_AUTH_DOMAIN'),
        'audience': os.getenv('INNO_AUDIENCE'),
        'scope': os.getenv('INNO_SCOPE'),
        'ssl_verification': os.getenv('INNO_SSL_VERIFICATION'),
        'force_insecure_channel': os.getenv('INNO_FORCE_INSECURE_CHANNEL'),
        'client_id': client_id or os.getenv('INNO_CLIENT_ID'),
        'client_secret': client_secret or os.getenv('INNO_CLIENT_SECRET'),
    }
    env_conf = {k: v for k, v in env_conf.items() if v}  # strip null env vars

    cp.read_dict({'innotescus': env_conf})

    log.debug(
        'Loading app config from the following files: %s',
        ','.join(reversed(_loaded_paths))
    )

    inno_config = cp['innotescus']

    auth_client = InnoAuthClient(
        client_id=inno_config.get('client_id'),
        client_secret=inno_config.get('client_secret'),
        scope=inno_config.get('scope'),
        audience=inno_config.get('audience'),
        auth_domain=inno_config.get('auth_domain')
    )

    return InnoApiClient(
        channel_factory_=partial(channel_factory, inno_config=inno_config, auth_client=auth_client),
        auth_client=auth_client,
        api_base_url=f'https://{inno_config.get("server_url")}:{inno_config.get("port")}',
        verify_ssl=inno_config.getboolean('ssl_verification')
    )


# just alias ApiClient, so we can keep the api non-breaking with v0.0.1
ApiClient = deprecated('Please update imports to use InnoApiClient')(client_factory)


__all__ = [
    'ApiClient', 'InnoApiClient', 'client_factory', 'ResponseCode', 'JobStatus', 'ExportType',
    'TaskType', 'AnnotationFormat', 'DataType', 'StorageType',
]
