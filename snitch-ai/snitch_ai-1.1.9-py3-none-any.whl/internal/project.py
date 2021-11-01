import os
import joblib
import tempfile
import shutil
import datetime
import time
import math
import mimetypes
from typing import Union
from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests.exceptions import ConnectionError

from snitch_ai.internal.guid import GUID
from snitch_ai.internal.api_client import ApiClient
from snitch_ai.internal.quality_analysis import QualityAnalysis
from snitch_ai.internal.drift_analysis import DriftAnalysis
from snitch_ai.internal.analysis_status import AnalysisState


def _save_tf_model(model, path):
    path += ".h5"
    model.save(path, save_format="h5")
    return path


def _save_sklearn_model(model, path):
    path += ".joblib"
    joblib.dump(model, path)
    return path


def _save_xgboost_model(model, path):
    path += ".json"
    model.save_model(path)
    return path


def _save_model_to_path(model, path):
    model_type = str(type(model))

    if "tensorflow." in model_type or "keras." in model_type:
        return _save_tf_model(model, path)

    if "xgboost." in model_type:
        return _save_xgboost_model(model, path)

    if "sklearn." in model_type:
        return _save_sklearn_model(model, path)

    raise Exception(f"Unsupported model type: {model_type}")


def _save_dataset_to_path(dataset, path):
    path += ".joblib"
    joblib.dump(dataset, path, compress=3)
    return path


def _upload_quality_analysis_file(project_id, quality_id, client, file_name, file_path):
    with open(file_path, "rb") as f:
        data = _prepare_multipart_file_upload(f, file_name, file_path)
        try:
            resp = client.patch(f"project/{project_id}/quality/{quality_id}", data=data, headers={'Content-Type': data.content_type})
        except ConnectionError:
            if (os.path.getsize(file_path) > 2147483648):
                raise Exception(f"Error while uploading files to remote host. Please try uploading files lower than 2GB (current file size: {os.path.getsize(file_path)} bytes).");
            else:
                raise Exception("Error while uploading files to remote host. Please try again later.");

        if resp.status_code != 200:
            raise Exception(f"Error uploading file: {resp.text}")


def _upload_drift_analysis_file(project_id, drift_id, client, file_name, file_path):
    with open(file_path, "rb") as f:
        data = _prepare_multipart_file_upload(f, file_name, file_path)
        try: 
            resp = client.patch(f"project/{project_id}/drift/{drift_id}", data=data, headers={'Content-Type': data.content_type})
        except ConnectionError:
            if (os.path.getsize(file_path) > 2147483648):
                raise Exception(f"Error while uploading files to remote host. Please try uploading files lower than 2GB (current file size: {os.path.getsize(file_path)} bytes).");
            else:
                raise Exception("Error while uploading files to remote host. Please try again later.");

        if resp.status_code != 200:
            raise Exception(f"Error uploading file: {resp.text}")


def _prepare_multipart_file_upload(file_handle, file_name, file_path) -> MultipartEncoder:
    mime_type, encoding = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "binary/octet-stream"

    return MultipartEncoder(
        fields={
            file_name: (os.path.basename(file_path), file_handle, mime_type)
        }
    )


def _wait_on_analysis_completion(analysis: Union[QualityAnalysis, DriftAnalysis]):
    # wait for analysis to complete
    count = 1
    waiting_on_completion = True
    while waiting_on_completion:
        # wait for 2, 4, 8, 16, 32, 32, 32, ... seconds before re-checking
        delay = math.pow(2, min(count, 5))
        count += 1
        time.sleep(delay)

        status = analysis.get_status()

        if status.state == AnalysisState.COMPLETED:
            waiting_on_completion = False
        elif status.state == AnalysisState.ERROR:
            raise Exception(f"The analysis failed due to an error: {status.error}")
        elif status.state == AnalysisState.UNKNOWN:
            raise Exception(
                "Error while waiting on analysis: analysis hasn't been started yet."
            )


class Project:
    def __init__(self, project_id: GUID, name: str):
        self.project_id = project_id
        self.name = name

    def get_quality_analysis(self, quality_id) -> QualityAnalysis:
        """
        Recovers a quality analysis by ID.
        :param quality_id: The ID of the analysis to recover.
        :return: The recovered analysis.
        """
        client = ApiClient()

        resp = client.get(f"/project/{self.project_id}/quality/{quality_id}")
        if resp.status_code != 200:
            raise Exception(f"Error fetching quality analysis: {resp.text}")

        quality_obj = resp.json()

        return QualityAnalysis(self.project_id, GUID(quality_obj["id"]))

    def run_quality_analysis(
        self,
        model,
        train_x,
        train_y,
        test_x,
        test_y,
        label: str = None,
        no_wait: bool = False,
    ) -> QualityAnalysis:
        """
        Runs a Quality analysis using the specified parameters.
        :param model: The model file. Supported types are Tensorflow, SciKit-Learn and XGBoost.
        :param train_x: The training feature dataset in array format.
        :param train_y: The training target dataset in array format.
        :param test_x: The testing feature dataset in array format.
        :param test_y: The testing target dataset in array format.
        :param label: The label for the quality analysis. If empty, will be given a default value.
        :param no_wait: If TRUE, do not wait for the analysis to complete.
        :return: A QualityAnalysis object that can be used to obtain status information as well as results of the Quality analysis.
        """
        client = ApiClient()

        if not label:
            label = (
                f"Quality Analysis {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )

        # create quality analysis
        resp = client.post(f"/project/{self.project_id}/quality", data={"label": label})
        if resp.status_code != 201:
            raise Exception(f"Error creating quality analysis: {resp.text}")

        quality_obj = resp.json()
        quality_id = quality_obj["id"]

        # upload files
        temp_dir = tempfile.mkdtemp(prefix="snitch_ai_")
        try:
            if not model is None:
                path = _save_model_to_path(model, os.path.join(temp_dir, "model"))
                _upload_quality_analysis_file(
                    self.project_id, quality_id, client, "model", path
                )

            if not train_x is None:
                path = _save_dataset_to_path(train_x, os.path.join(temp_dir, "train_x"))
                _upload_quality_analysis_file(
                    self.project_id, quality_id, client, "train_x", path
                )

            if not train_y is None:
                path = _save_dataset_to_path(train_y, os.path.join(temp_dir, "train_y"))
                _upload_quality_analysis_file(
                    self.project_id, quality_id, client, "train_y", path
                )

            if not test_x is None:
                path = _save_dataset_to_path(test_x, os.path.join(temp_dir, "test_x"))
                _upload_quality_analysis_file(
                    self.project_id, quality_id, client, "test_x", path
                )

            if not test_y is None:
                path = _save_dataset_to_path(test_y, os.path.join(temp_dir, "test_y"))
                _upload_quality_analysis_file(
                    self.project_id, quality_id, client, "test_y", path
                )
        finally:
            shutil.rmtree(temp_dir)

        # start analysis
        resp = client.post(f"project/{self.project_id}/quality/{quality_id}/start")
        if resp.status_code != 200:
            raise Exception(f"Error starting quality analysis: {resp.text}")

        quality_analysis = QualityAnalysis(self.project_id, quality_id)

        if not no_wait:
            _wait_on_analysis_completion(quality_analysis)

        return quality_analysis

    def get_drift_analysis(self, drift_id) -> DriftAnalysis:
        """
        Recovers a drift analysis by ID.
        :param drift_id: The ID of the analysis to recover.
        :return: The recovered analysis.
        """
        client = ApiClient()

        resp = client.get(f"/project/{self.project_id}/drift/{drift_id}")
        if resp.status_code != 200:
            raise Exception(f"Error fetching drift analysis: {resp.text}")

        drift_obj = resp.json()

        return DriftAnalysis(self.project_id, GUID(drift_obj["id"]))

    def run_drift_analysis(
        self, train_x, updated_x, label: str = None, no_wait: bool = False
    ) -> DriftAnalysis:
        """
        Runs a Drift analysis using the specified parameters.
        :param train_x: The training feature dataset in array format.
        :param updated_x: The updated feature dataset in array format.
        :param label: The label for the drift analysis. If empty, will be given a default value.
        :param no_wait: If TRUE, do not wait for the analysis to complete.
        :return: A DriftAnalysis object that can be used to obtain status information as well as results of the Drift analysis.
        """
        client = ApiClient()

        if not label:
            label = (
                f"Drift Analysis {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )

        # create drift analysis
        resp = client.post(f"/project/{self.project_id}/drift", data={"label": label})
        if resp.status_code != 201:
            raise Exception(f"Error creating drift analysis: {resp.text}")

        drift_obj = resp.json()
        drift_id = drift_obj["id"]

        # upload files
        temp_dir = tempfile.mkdtemp(prefix="snitch_ai_")
        try:
            if not train_x is None:
                path = _save_dataset_to_path(train_x, os.path.join(temp_dir, "train_x"))
                _upload_drift_analysis_file(
                    self.project_id, drift_id, client, "train_x", path
                )

            if not updated_x is None:
                path = _save_dataset_to_path(
                    updated_x, os.path.join(temp_dir, "updated_x")
                )
                _upload_drift_analysis_file(
                    self.project_id, drift_id, client, "updated_x", path
                )
        finally:
            shutil.rmtree(temp_dir)

        # start analysis
        resp = client.post(f"project/{self.project_id}/drift/{drift_id}/start")
        if resp.status_code != 200:
            raise Exception(f"Error starting drift analysis: {resp.text}")

        drift_analysis = DriftAnalysis(self.project_id, GUID(drift_id))

        if not no_wait:
            _wait_on_analysis_completion(drift_analysis)

        return drift_analysis

    def __str__(self):
        return f"Project {self.project_id}: {self.name}"


def select_project(project_name: str) -> Project:
    """
    Selects the specified project. If it does not already exist, it will be created.
    :param project_name: The name of the project.
    :return: The requested project.
    """
    client = ApiClient()

    resp = client.post("project/select", data={"name": project_name})
    if resp.status_code != 200 and resp.status_code != 201:
        raise Exception(f"Could not select project: {resp.text}")

    json = resp.json()

    return Project(GUID(json["id"]), json["name"])


def create_project(project_name: str) -> Project:
    """
    Create a project with the specified name.
    :param project_name: The name of the project to create. Must be unique within the entire system.
    :return: The created project.
    """
    client = ApiClient()

    resp = client.post("project", data={"name": project_name})
    if resp.status_code != 201:
        raise Exception(f"Could not create project: {resp.text}")

    json = resp.json()

    return Project(GUID(json["id"]), json["name"])


def get_project(target: Union[str, GUID]) -> Project:
    """
    Get a project by ID or project name.
    :param target: The ID of the project or project name.
    :return: The requested project.
    """
    client = ApiClient()

    json = None
    if isinstance(target, str):
        resp = client.get("project", params={"name": target})
        if resp.status_code != 200:
            raise Exception(f"Could not find project: {resp.text}")
        json = resp.json()
    else:
        resp = client.get(f"project/{target}")
        if resp.status_code != 200:
            raise Exception(f"Could not find project: {resp.text}")
        json = resp.json()

    return Project(GUID(json["id"]), json["name"])
