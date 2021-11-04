import datetime
import uuid

from domino_data_capture import utils
from domino_data_capture.logger import PredictionLoggerManager
from domino_data_capture.utils import handle_error

ERROR_MESSAGE_PREFIX = "ERROR domino_data_capture::capturePrediction:"


class DataCaptureClient:
    def __init__(self, feature_names, predict_names, metadata_names=None):
        self.feature_names = feature_names
        self.predict_names = predict_names
        self.metadata_names = metadata_names

        model_version_id = utils.get_model_version()

        self.is_dev_mode = True if utils.get_model_version() is None else False
        self.instance_id = model_version_id

    def capturePrediction(
        self,
        feature_values,
        prediction_values,
        metadata_values=None,
        event_id=None,
        timestamp=None,
        prediction_probability=None,
        sample_weight=None,
    ):
        # preconditions
        if len(self.feature_names) != len(feature_values):
            handle_error(
                self.is_dev_mode,
                f"{ERROR_MESSAGE_PREFIX}feature_names and feature_values should be of same length",
            )
            return None
        if len(self.predict_names) != len(prediction_values):
            handle_error(
                self.is_dev_mode,
                f"{ERROR_MESSAGE_PREFIX}predict_names and prediction_values should be of same length",
            )
            return None
        if self.metadata_names is None and metadata_values is not None:
            handle_error(
                self.is_dev_mode,
                f"{ERROR_MESSAGE_PREFIX}metadata_names is not present, but metedata values present",
            )
            return None
        if self.metadata_names is not None and metadata_values is None:
            handle_error(
                self.is_dev_mode,
                f"{ERROR_MESSAGE_PREFIX}metadata_names is  present, but metedata values is not present, ",
            )
            return None
        if metadata_values is not None and len(self.metadata_names) != len(metadata_values):
            handle_error(
                self.is_dev_mode,
                f"{ERROR_MESSAGE_PREFIX}metadata_names and metadata_values should be of same length",
            )
            return None

        event_id = event_id if event_id else uuid.uuid4()
        domino_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

        prediction_dict = {k: v for k, v in zip(self.predict_names, prediction_values)}
        feature_dict = {k: v for k, v in zip(self.feature_names, feature_values)}

        if self.metadata_names is not None:
            metadata_dict = {k: v for k, v in zip(self.metadata_names, metadata_values)}
        else:
            metadata_dict = None

        message = {
            "predictions": prediction_dict,
            "features": feature_dict,
            "metadata": metadata_dict,
            "timestamp": timestamp if timestamp else domino_timestamp,
            "__domino_timestamp": domino_timestamp,
            "event_id": str(event_id),
            "prediction_probability": prediction_probability,
            "sample_weight": sample_weight,
            "instance_id": self.instance_id,
        }

        custom_logger = PredictionLoggerManager(utils.get_scrape_location(), self.is_dev_mode)

        custom_logger.record(message)

        return message
