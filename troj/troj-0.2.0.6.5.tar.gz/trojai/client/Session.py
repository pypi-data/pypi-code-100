from trojai import client
import numpy as np
import json
from trojai.logger import logger
from trojai.client.client_utils import save_dataframe_to_disk


class TrojSession:
    def __init__(self):
        super().__init__()
        self.client = None
        self.logger = logger.Logger()
        self.graphs = None

    def run_name(self, name):
        self.log({"run_name": name})

    def log_graph(self, html):
        self.log({"graphs": html})

    def log(self, in_dict):
        self.logger.log(in_dict)

    def create_project(self, project_name: str):
        return self.client.create_project(project_name)

    def create_dataset(self, project_name: str, dataset_name: str):
        return self.client.create_dataset(project_name, dataset_name)

    def reorient_df(self, dataframe):
        dataframe = json.loads(dataframe.to_json(orient="index"))
        return dataframe

    def _check_df_storage(self):
        # Check user/teams datapoint limit and actual storage
        datapoints_left = self.client.check_storage()
        logger_dict = self.logger.get_logger()

        if "dataframe" in logger_dict:
            return len(logger_dict["dataframe"]) <= datapoints_left
        # Raise exception here instead if "dataframe" isn't in dict?
        return True

    """
    Drops rows with a null value in a column from the dataframe then reorients the dataframe to be returned
    :param dataframe: the dataframe
    :param drop_na: nulls should be dropped bool
    """

    def drop_empty_rows(self, dataframe, drop_na):
        if drop_na == True:
            dataframe = dataframe.dropna()

        json_processed_out = self.reorient_df(dataframe)

        return json_processed_out

    """
    Uploads the logs collected by the logger

    :param project_name: string name of project that exusts on the platform
    :param dataset_name: a dataset that exists under the project  
    """

    def upload_logs(self, project_name: str, dataset_name: str, drop_na=True):
        logger_dict = self.logger.get_logger()
        processed_df = logger_dict

        if "metadata" in processed_df:
            processed_df["metadata"] = processed_df["metadata"][0]
        if "dataframe" in processed_df:
            processed_df["dataframe"] = self.drop_empty_rows(
                logger_dict["dataframe"][0], drop_na
            )
        jsonified_df = processed_df

        # Save dataframe to disk before uploading to s3
        # save_dataframe_to_disk(dataset_name, jsonified_df)

        # Check if dataframe will be able to be uploaded based on current storage usage
        if not self._check_df_storage():
            raise Exception(
                "This upload will exceed datapoint limit. Delete existing datasets or upgrade your subscription to gain access to more datapoint storage."
            )

        return self.client.upload_df_results(project_name, dataset_name, jsonified_df)

    def add_latent(self, np_latent, dataframe):
        dataframe["latent"] = np_latent
        return dataframe



    """
    Takes in the troj dataframe we've built over the attack loop as well as optionally the classifier, evaluator and dataloader
    for metadata collection. This function must be run before the upload_logs function for proper formatting.

    :param dataframe: the dataframe used to track the experiments and data
    :param classifier: the TrojClassifier object
    :param evaluator: The RobustnessEvaluator object
    :param dataloader: the dataloader object  
    :param tags: array of strings to tage the run 
    :return: dictionary of metadata
    """

    def log_metadata(
        self, dataframe, classifier=None, evaluator=None, dataloader=None, tags=[]
    ):
        # also need to pull the log_dict from logger
        classifier_meta = {}
        evaluator_meta = {}
        dataloader_meta = {}

        if classifier is not None:
            classifier_meta = classifier.get_classifier_meta()
        if evaluator is not None:
            evaluator_meta = evaluator.atk_meta
        if dataloader is not None:
            dataloader_meta = dataloader.dataset_meta
        if "prediction" in dataframe:
            dataframe["prediction"].replace("", np.nan, inplace=True)
        dataframe.dropna(inplace=True)
        out_dict = {
            "metadata": {
                "classifier_metadata": classifier_meta,
                "evaluator_metadata": evaluator_meta,
                "dataloader_metadata": dataloader_meta,
                "tags": str(tags),
            },
            "dataframe": dataframe,
        }
        self.log(out_dict)

        return out_dict
