"""
Client for modep API, Swagger docs are at https://modep.ai/v1/api-docs
"""
import io
import os
import copy
import time
import logging
import tempfile
import zipfile
import requests
import pandas as pd
from requests_toolbelt import MultipartEncoder

INCOMPLETE_STATES = set(["CREATED", "STARTING", "RUNNING"])

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


class ModepClient:
    def __init__(self, api_key, url="https://modep.ai/v1/", ensure_https=True):

        if ensure_https and not url.startswith("https://"):
            raise Exception("The url should start with https://")

        # ensure trailing "/"
        url = url if url[-1] == "/" else url + "/"

        self.url = url
        self.api_key = api_key

        self.login()

    def response_exception(self, resp):
        raise Exception(
            f"status_code: {resp.status_code}, reason: {resp.reason}, text: {resp.text}"
        )

    def login(self):
        url = self.url + "login"

        # this is the JWT header required for protected endpoints
        self._auth_header = None

        # start a new session
        self.sess = requests.Session()

        # make login request
        resp = self.sess.post(url, json=dict(api_key=self.api_key))
        if resp.ok:
            access_token = resp.json()["access_token"]
            self._auth_header = {"Authorization": f"Bearer {access_token}"}
            logger.debug(self._auth_header)
        else:
            self.response_exception(resp)

    def auth_header(self):
        url = self.url + "ping"
        resp = self.sess.get(url, headers=self._auth_header)
        if resp.ok:
            return self._auth_header

        if resp.status_code in (401, 500):
            # auth token has expired, so get a new one
            self.login()
            return self._auth_header

    def upload_dataset(self, dset, name):
        """
        Upload a tabular dataset.
        Inputs:
           dest: either a string path or a pd.DataFrame.
        """

        if isinstance(dset, str):
            path = dset
            if not os.path.exists(path):
                raise Exception(f"Path does not exist: '{path}'")
        elif isinstance(dset, pd.DataFrame):
            path = tempfile.NamedTemporaryFile(suffix="-df-upload").name + ".csv"
            logger.info("Writing DataFrame to %s", path)
            dset.to_csv(path, index=False)
        else:
            raise ValueError(
                "Unknown type for dataset, "
                "must be either string path or pd.DataFrame"
            )
        logger.info("Uploading from %s", path)

        url = self.url + "datasets/tabular"
        # deepcopy since we update headers below
        headers = copy.deepcopy(self.auth_header())

        with open(path, "rb") as f:
            data = MultipartEncoder(
                {
                    "path": os.path.abspath(path),
                    "name": name,
                    "file": (path, f, "text/csv/h5"),
                }
            )
            headers.update(
                {"Prefer": "respond-async", "Content-Type": data.content_type}
            )
            resp = self.sess.post(url, data=data, headers=headers)
        if resp.ok:
            return resp.json()
        else:
            self.response_exception(resp)

    def upload_dataset_from_df(self, df, name):
        """
        Upload a tabular dataset from a DataFrame.
        """
        url = self.url + "datasets/tabular"

        # extra data to include
        data = {
            "path": None,
            "name": name,
            "ext": ".csv",
        }

        # Bearer auth dict
        headers = self.auth_header()

        # write to CSV in memory
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        stream.seek(0)
        files = {"file": stream}

        resp = self.sess.post(url, files=files, data=data, headers=headers)
        if resp.ok:
            return resp.json()
        else:
            self.response_exception(resp)

    def get_dataset(self, id):
        url = self.url + "datasets/tabular/" + str(id)
        resp = self.sess.get(url, headers=self.auth_header())
        if resp.ok:
            return resp.json()
        else:
            self.response_exception(resp)

    def list_datasets(self):
        url = self.url + "datasets/tabular"
        resp = self.sess.get(url, headers=self.auth_header())
        if resp.ok:
            js = resp.json()
            df = pd.DataFrame(js)
            if len(df) > 0:
                # keep column order same as json
                df = df[list(js[0].keys())].set_index("id")
                df = df.sort_values(by="created", ascending=False)
            return df
        else:
            self.response_exception(resp)

    def delete_dataset(self, id):
        url = self.url + "datasets/tabular/" + str(id)
        resp = self.sess.delete(url, headers=self.auth_header())
        if resp.ok:
            return resp.json()
        else:
            self.response_exception(resp)

    def list_framework_runs(self):
        url = self.url + "frameworks/tabular"
        resp = self.sess.get(url, headers=self.auth_header())
        if resp.ok:
            js = resp.json()
            df = pd.DataFrame(js)
            if len(df) > 0:
                # keep column order same as json
                df = df[list(js[0].keys())].set_index("id")
                df = df.sort_values(by="created", ascending=False)
            return df
        else:
            self.response_exception(resp)

    def automl_train(
        self,
        framework_name,
        train_ids,
        test_ids,
        target,
        max_runtime_seconds,
        experiment_id="",
    ):

        url = self.url + "frameworks/tabular"

        train_ids = [train_ids] if isinstance(train_ids, str) else train_ids
        test_ids = [test_ids] if isinstance(test_ids, str) else test_ids

        data = dict(
            framework_name=framework_name,
            train_ids=train_ids,
            test_ids=test_ids,
            target=target,
            max_runtime_seconds=max_runtime_seconds,
            experiment_id=experiment_id,
        )
        logger.info(data)

        resp = self.sess.post(url, json=data, headers=self.auth_header())
        if resp.ok:
            return TrainTask(self, resp.json())
        else:
            self.response_exception(resp)

    def get_framework_run(self, id):
        url = self.url + "frameworks/tabular/" + str(id)
        resp = self.sess.get(url, headers=self.auth_header())
        if resp.ok:
            return resp.json()
        else:
            self.response_exception(resp)

    def stop_framework_run(self, id):
        url = self.url + f"frameworks/tabular/{id}/stop"
        resp = self.sess.get(url, headers=self.auth_header())
        if resp.ok:
            return resp.json()
        else:
            self.response_exception(resp)

    def delete_framework_run(self, id):
        url = self.url + "frameworks/tabular/" + str(id)
        resp = self.sess.delete(url, headers=self.auth_header())
        if resp.ok:
            return resp.json()
        else:
            self.response_exception(resp)

    def automl_predict(self, framework_id, dataset_id):
        url = self.url + "frameworks/tabular/predict"

        data = dict(
            framework_id=framework_id,
            dataset_id=dataset_id,
        )

        resp = self.sess.post(url, json=data, headers=self.auth_header())
        if resp.ok:
            return PredictTask(self, resp.json())
        else:
            self.response_exception(resp)

    def get_framework_predictions(self, predictions_id):
        url = self.url + f"frameworks/tabular/predictions/{predictions_id}"
        resp = self.sess.get(url, headers=self.auth_header())
        if resp.ok:
            return resp.json()
        else:
            self.response_exception(resp)

    def get_framework_output(self, id, target_dir):
        url = self.url + f"frameworks/tabular/{id}/output"
        resp = self.sess.get(url, headers=self.auth_header())
        if resp.ok:
            # download contents to directory
            z = zipfile.ZipFile(io.BytesIO(resp.content))
            z.extractall(path=target_dir)
            return resp
        else:
            self.response_exception(resp)

    def list_framework_info(self):
        url = self.url + "frameworks/tabular/info"
        resp = self.sess.get(url, headers=self.auth_header())
        if resp.ok:
            js = resp.json()
            df = pd.DataFrame(js)
            if len(df) > 0:
                # keep column order same as json
                df = df[list(js[0].keys())].set_index("framework_name")
            return df
        else:
            self.response_exception(resp)

    def automl_flight(
        self,
        framework_names,
        train_ids,
        test_ids,
        target,
        max_runtime_seconds,
        experiment_id="",
    ):

        url = self.url + "frameworks/tabular/flight"

        train_ids = [train_ids] if isinstance(train_ids, str) else train_ids
        test_ids = [test_ids] if isinstance(test_ids, str) else test_ids

        data = dict(
            framework_names=framework_names,
            train_ids=train_ids,
            test_ids=test_ids,
            target=target,
            max_runtime_seconds=max_runtime_seconds,
        )

        resp = self.sess.post(url, json=data, headers=self.auth_header())
        if resp.ok:
            return FlightTask(self, resp.json())
        else:
            self.response_exception(resp)

    def list_flights(self):
        url = self.url + "frameworks/tabular/flight"
        resp = self.sess.get(url, headers=self.auth_header())
        if resp.ok:
            js = resp.json()
            df = pd.DataFrame(js)
            if len(df) > 0:
                # keep column order same as json
                df = df[list(js[0].keys())].set_index("id")
                df = df.sort_values(by="created", ascending=False)
            return df
        else:
            self.response_exception(resp)

    def get_flight(self, id):
        url = self.url + "frameworks/tabular/flight/" + str(id)
        resp = self.sess.get(url, headers=self.auth_header())
        if resp.ok:
            return resp.json()
        else:
            self.response_exception(resp)

    def delete_flight(self, id):
        url = self.url + "frameworks/tabular/flight/" + str(id)
        resp = self.sess.delete(url, headers=self.auth_header())
        if resp.ok:
            return resp.json()
        else:
            self.response_exception(resp)

    def stop_flight(self, id):
        url = self.url + f"frameworks/tabular/flight/{id}/stop"
        resp = self.sess.get(url, headers=self.auth_header())
        if resp.ok:
            return resp.json()
        else:
            self.response_exception(resp)

    def wait_for_flight(self, id):
        from IPython.display import display, HTML, clear_output

        while True:
            flight = self.get_flight(id)

            # make a DataFrame for the individual AutoML frameworks for this flight
            frameworks = pd.DataFrame(flight.pop("frameworks", []))

            # drop some columns for optimal viewing
            frameworks = frameworks.drop(
                ["fold_results", "fold_leaderboard", "fold_model_txt"], 1
            )

            print(f"flight status: {flight['status']}")
            print("flight members:")
            display(HTML(frameworks.to_html()))

            if flight["status"] not in INCOMPLETE_STATES:
                break

            time.sleep(5)
            clear_output(wait=True)

    def print_framework_log(self, id):
        import glob

        framework = self.get_framework_run(id)

        # download logs
        outdir = tempfile.NamedTemporaryFile(suffix=f"-modep-run").name
        self.get_framework_output(framework["id"], outdir)

        logfile = glob.glob(outdir + "/*/logs/*.full.log")
        if len(logfile) == 1:
            with open(logfile[0], "r") as f:
                logtxt = f.read()
            print(logtxt)
        return logfile

    def download_openml_task(self, task_id=168909, max_folds=None):
        """
        https://openml.github.io/openml-python/develop/examples/30_extended/task_manual_iteration_tutorial.html
        """
        import openml as oml

        task = oml.tasks.get_task(task_id, download_qualities=False)
        dataset = oml.datasets.get_dataset(task.dataset_id, download_qualities=False)

        n_repeats, n_folds, n_samples = task.get_split_dimensions()

        if n_repeats != 1 or n_samples != 1:
            raise NotImplementedError(f"n_samples: {n_samples}, n_repeats: {n_repeats}")

        if hasattr(task, "class_labels"):
            is_class = True
        else:
            is_class = False

        X, y = task.get_X_and_y(dataset_format="dataframe")

        target = task.target_name
        assert y.name == target
        df = pd.concat((X, y), 1)

        train_files, test_files = [], []
        n_train, n_test = [], []

        if max_folds is None:
            max_folds = n_folds

        for fold in range(max_folds):

            train_indices, test_indices = task.get_train_test_split_indices(
                repeat=0, fold=fold, sample=0
            )

            df_train = df.iloc[train_indices]
            df_test = df.iloc[test_indices]

            f_train = (
                tempfile.NamedTemporaryFile().name
                + f"-openml-task-{task_id}-train-%02d.csv'" % fold
            )
            f_test = (
                tempfile.NamedTemporaryFile().name
                + f"-openml-task-{task_id}-test-%02d.csv'" % fold
            )

            df_train.to_csv(f_train, index=False)
            df_test.to_csv(f_test, index=False)

            train_files.append(f_train)
            test_files.append(f_test)

            n_train.append(len(train_indices))
            n_test.append(len(test_indices))

        return dict(
            dataset=dataset,
            task=task,
            train_files=train_files,
            test_files=test_files,
            n_train=n_train,
            n_test=n_test,
            is_class=is_class,
            target=target,
            n_folds=n_folds,
            max_folds=max_folds,
        )


class TrainTask:
    def __init__(self, client, response):
        self.client = client
        self.response = response

    def result(self):
        while self.response["status"] in INCOMPLETE_STATES:
            self.response = self.client.get_framework_run(self.response["id"])
            time.sleep(5)
        return self.response


class PredictTask:
    def __init__(self, client, response):
        self.client = client
        self.response = response

    def result(self):
        while self.response["status"] in INCOMPLETE_STATES:
            self.response = self.client.get_framework_predictions(self.response["id"])
            time.sleep(5)
        return self.response


class FlightTask:
    def __init__(self, client, response):
        self.client = client
        self.response = response

    def result(self):
        while self.response["status"] in INCOMPLETE_STATES:
            self.response = self.client.get_flight(self.response["id"])
            time.sleep(5)
        return self.response
