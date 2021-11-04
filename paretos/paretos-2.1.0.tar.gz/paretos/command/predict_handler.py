from logging import Logger
from typing import Dict, List

from paretos.athena.athena_api_client import AthenaApiClient


class PredictHandler:
    def __init__(self, logger: Logger, api_client: AthenaApiClient):
        self.__logger = logger
        self.__api_client = api_client

    def predict(self, model: str, data: List[Dict[str, List[float]]]):
        response = self.__api_client.predict(model, data)
        return response.get("predictions").get("result")
