import logging
from unittest import TestCase, skip

from libumccr.aws import libs3

# FIXME centralise test case logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LibS3UnitTests(TestCase):
    # TODO https://github.com/umccr/libumccr/issues/1
    pass


class LibS3IntegrationTests(TestCase):
    # integration test hit actual File or API endpoint, thus, manual run in most cases
    # required appropriate access mechanism setup such as active aws login session
    # uncomment @skip and hit the each test case!
    # and keep decorated @skip after tested

    @skip
    def test_get_s3_object_to_bytes(self):
        """
        python -m unittest tests.aws.test_libs3.LibS3IntegrationTests.test_get_s3_object_to_bytes
        """
        bucket = "umccr-temp-dev"
        key = "cancer_report_tables/hrd/SBJ00670__SBJ00670_MDX210005_L2100047_rerun-hrdetect.json.gz"
        result = libs3.get_s3_object_to_bytes(bucket, key)
        logger.info(f"Result type: {type(result)}, Body content: \n{result}")
        self.assertIsInstance(result, bytes)
