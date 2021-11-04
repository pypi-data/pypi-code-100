import uuid
from typing import Dict, List

from .athena_api_http_session import AthenaApiHttpSession


class AthenaApiClient:
    def __init__(
        self,
        session: AthenaApiHttpSession,
    ):
        self.__session = session

    def predict(self, model: str, data: List[Dict[str, List[float]]]):
        """
        Uses the specified model to create a prediction from the provided data.
        :param model: name of the model
        :param data: the raw input data as lists of float (numpy etc. not supported)
        """
        request_data = {
            "model_id": model,
            "prediction_requests": [
                {
                    "id": str(uuid.uuid4()),
                    "input_data": [
                        {"name": feature_name, "values": feature_value}
                        for feature_name, feature_value in prediction_request.items()
                    ],
                }
                for prediction_request in data
            ],
        }

        response_data = self.__session.authenticated_request(
            path="predict",
            version="v1",
            contains_sensitive_data=False,
            data=request_data,
            method="POST",
        )

        return response_data
