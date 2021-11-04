from unittest import TestCase, skip

from libumccr.aws import libsm


class LibSmUnitTests(TestCase):
    # TODO https://github.com/umccr/libumccr/issues/2
    pass


class LibSmIntegrationTests(TestCase):

    @skip
    def test_get_secret(self):
        """
        python -m unittest tests.aws.test_libsm.LibSmIntegrationTests.test_get_secret
        """

        secret_name = "IcaSecretsPortal"

        secret = libsm.get_secret(secret_name=secret_name)

        self.assertIsNotNone(secret)
        self.assertIsInstance(secret, str)
        # print(secret)
