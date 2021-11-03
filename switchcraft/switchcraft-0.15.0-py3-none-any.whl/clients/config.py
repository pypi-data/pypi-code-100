"""AWS Config Client.

A light-weight client for the AWS Config API.
"""

from datetime import datetime
import logging
from typing import List, Literal

import boto3
from botocore.exceptions import ClientError
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

log = logging.getLogger(__name__)


class ConfigClient:

    def __init__(self) -> None:
        self.config = boto3.client('config')

    def put_evaluations(
        self,
        evaluations: List[dict],
        result_token: str,
        test_mode: bool = False
    ):
        try:
            resp = self.config.put_evaluations(
                Evaluations=evaluations,
                ResultToken=result_token,
                TestMode=test_mode
            )
            return resp
        except ClientError as err:
            log.error(
                f'Error occurred while sending evaluations to '
                f'AWS Config: {err}'
            )
            raise err


class Evaluation(BaseModel):
    ComplianceResourceType: str
    ComplianceResourceId: str
    ComplianceType: Literal[
        'COMPLIANT',
        'NON_COMPLIANT',
        'NOT_APPLICABLE',
        'INSUFFICIENT_DATA'
    ]
    Annotation: str
    OrderingTimestamp: datetime

    def __post_init__(self):
        self.Annotation = self.build_annotation(self.Annotation)

    @staticmethod
    def build_annotation(annotation_string):
        if len(annotation_string) > 256:
            return f'{annotation_string[:244]} [truncated]'
        return annotation_string


@dataclass
class ComplianceType():
    compliant: str = 'COMPLIANT'
    non_compliant: str = 'NON_COMPLIANT'
    not_applicable: str = 'NOT_APPLICABLE'
    insufficient_data: str = 'INSUFFICIENT_DATA'
