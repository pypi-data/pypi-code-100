"""Clients Package."""

from switchcraft.clients.alb import AlbClient
from switchcraft.clients.config import ComplianceType
from switchcraft.clients.config import ConfigClient
from switchcraft.clients.config import Evaluation
from switchcraft.clients.dynamodb import DynamoDBClient
from switchcraft.clients.ec2 import EC2Client
from switchcraft.clients.rds import RDSClient
from switchcraft.clients.sns import SNSClient
from switchcraft.clients.s3 import S3Client
from switchcraft.clients.sts import STSClient


# Overriding '__all__' to ensure that public access to classes are controlled.
__all__ = [
    AlbClient,
    ConfigClient,
    ComplianceType,
    DynamoDBClient,
    Evaluation,
    EC2Client,
    RDSClient,
    S3Client,
    SNSClient,
    STSClient
]
