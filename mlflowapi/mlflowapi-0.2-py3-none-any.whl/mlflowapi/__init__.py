import json
from collections import defaultdict
from typing import Dict, List
import pandas as pd
from sklearn.metrics import confusion_matrix
import pickle
import mlflow
import mlflow.sklearn


class MlflowAPIs:
    """A mlflow client to:
    1. read, write artifacts from minio bucket
    2. get runs
    3. get metrics
    uses apis from : https://www.mlflow.org/docs/latest/python_api/index.html
    """    
    def __init__(self, tracking_uri, logger):
        mlflow.set_tracking_uri(tracking_uri)
        self.mlflow_client = mlflow.tracking.MlflowClient()
        self.logger = logger
        self.experiment = None

    def create_mlflow_run(self, name: str):
        """creates mlflow run for an experiment

        Parameters
        ----------
        name : str
            mlflow experiment name
        tracking_uri : str
            mlflow endpoint

        Returns
        -------
        int : str
            mlflow experiment id and run id
        """
        try:
            # mlflow.set_tracking_uri(tracking_uri)
            # mlflow_client = mlflow.tracking.MlflowClient()
            mlflow.set_experiment(name)
            ex_id = mlflow.get_experiment_by_name(name).experiment_id
            # ex_id = x.experiment_id
            experiment = dict(self.mlflow_client.create_run(ex_id))
            self.logger.info(f"Experiment : {experiment}")
            run_id = experiment['info'].run_id
            experiment_id = experiment['info'].experiment_id
            # artifacts_path = self.mlflow_client.get_run(run_id).info.artifact_uri
            return run_id, experiment_id
        except Exception as err:
            self.logger.error(err)

    def get_artifact(self, run_id: str, relative_path: str):
        """read artifact already saved in mlflow

        Parameters
        ----------
        run_id : str
            run id for an experiment performed
        relative_path : str
            path respect to artifact root uri

        Returns
        -------
        output : object
            data after reading artifact file as Union[dict, pd.DataFrame]
        """        
        local_path = self.mlflow_client.download_artifacts(
            run_id, relative_path)
        data = None
        if local_path.endswith('.json'):
            with open(local_path, 'r') as f:
                data = json.load(f)
        if local_path.endswith('.csv'):
            data = pd.read_csv(local_path)
        if local_path.endswith('.pkl'):
            with open(local_path, "rb") as f:
                data = pickle.load(f)
        return data

    def load_sklearn_artifact(self, s3_path):
        """load_sklearn_artifact
        This function will load sklearn artifact

        Parameters
        ----------
        s3_path : str
             Source bucket name of s3_path

        Returns
        -------
        mlflow : Object
             return mlflow.sklearn
        """
        self.logger.info(f"path: {s3_path}")
        s3_path = s3_path.replace('\\', '/')
        return mlflow.sklearn.load_model(s3_path)

    def get_experiment_id(self, name: str):
        """get experiment id by its name

        Parameters
        ----------
        name :str
            mlflow experiment name

        Returns
        -------
        experiment id : int
            mlflow experiment id
        """        
        mlflow.set_experiment(name)
        ex = mlflow.get_experiment_by_name(name)
        return ex.experiment_id

    def get_artifact_path(self, ex_name, run_id):
        """get artifacts from mlflow

        Parameters
        ----------
        ex_name : str
            experiment name
        run_id : str
            mlflow run id
        tracking_uri : str
            mlflow endpoint url

        Returns
        -------
         artifact_path : str
            local artifact path
        """
        # mlflow.set_tracking_uri(tracking_uri)
        # mlflow_client = mlflow.tracking.MlflowClient()
        mlflow.set_experiment(ex_name)
        artifact_path = self.mlflow_client.get_run(run_id).info.artifact_uri
        return artifact_path

    def get_metrics(self, ex_name, run_id):
        """get metrics from mlflow

        Parameters
        ----------
        ex_name : str
            experiment name
        run_id : str
            mlflow run id
        tracking_uri : str
            mlflow endpoint url

        Returns
        -------
        str
            local artifact path
        """
        # mlflow.set_tracking_uri(tracking_uri)
        # mlflow_client = mlflow.tracking.MlflowClient()
        mlflow.set_experiment(ex_name)
        metrics = self.mlflow_client.get_run(run_id).data.metrics
        return metrics

    def get_latest_run_id(self, exp_name):
        """get metrics from mlflow

        Parameters
        ----------
        ex_name : str
            experiment name
        run_id : str
            mlflow run id
        tracking_uri : str
            mlflow endpoint url

        Returns
        -------
        str
            local artifact path
        """
        experiemnts = self.mlflow_client.list_experiments()
        print(experiemnts)
        for exp in experiemnts:
            if exp.name == exp_name:
                exp_id = exp.experiment_id
                break
        else:
            return None
        try:
            run_id = self.mlflow_client.search_runs([exp_id])[0].info.run_id
        except Exception as e:
            return None
        return run_id


    def get_runs(self, name: str):
        """get all the runs with given experiment name

        Parameters
        ----------
        name : str
            experiment name

        Returns
        -------
        run_ids : List
            all the run ids
        """        
        ex_id = self.get_experiment_id(name)
        run_infos = self.mlflow_client.list_run_infos(experiment_id=ex_id)
        run_ids = [run_info.run_id for run_info in run_infos]
        return run_ids

    def _change_pred(self, predictions: pd.DataFrame, label_mapping: Dict):
        """_change_pred
        This function will change pred

        Parameters
        ----------
        predictions : dataframe
             dataframe of predictions
        label_mapping : dict
             A dictionary of label maping

        Returns
        -------
        predictions : Object
             return predictions
        """
        for dim in label_mapping.keys():
            reverse_dict = {v:k for k,v in label_mapping[dim].items()}
            predictions.replace({dim: reverse_dict}, inplace=True)
        return predictions

    def get_cm(self, y_true: List[str], y_pred: List[str], labels: List[str]):
        """get confusion matrix

        Parameters
        ----------
        y_true : List[str]
            true label
        y_pred : List[str]
            predicted label
        labels : List[str]
            labels during training

        Returns
        -------
        cm_int : List
            confusion matrix
        """        
        cm_array = confusion_matrix(y_true, y_pred, labels=labels)
        cm = [list(row) for row in cm_array]
        cm_int = [[int(s) for s in sublist] for sublist in cm]
        return cm_int


def nested_dict():
    """ Function to define a nested dictionary

    Returns
    -------
    output : dict
        a dictionary with collections.defaultdict
    """    
    return defaultdict(nested_dict)

