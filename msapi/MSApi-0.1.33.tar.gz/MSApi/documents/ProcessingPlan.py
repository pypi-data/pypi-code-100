from typing import Optional
from datetime import datetime

from MSApi.documents.DocumentMS import DocumentMS
from MSApi.MSLowApi import MSLowApi, error_handler, caching


class ProcessingPlan(DocumentMS):

    @classmethod
    @caching
    def generate(cls, **kwargs):
        return MSLowApi.gen_objects('entity/processingplan', ProcessingPlan, **kwargs)

    def __init__(self, json):
        super().__init__(json)

    def create(self, **kwargs):
        response = MSLowApi.auch_post(f'entity/demand', json=self.get_json(), **kwargs)
        error_handler(response)
        self._json = response.json()
