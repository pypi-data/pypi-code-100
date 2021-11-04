from unittest import TestCase, skip

from libumccr.aws import libssm


class LibSsmUnitTests(TestCase):
    # TODO https://github.com/umccr/libumccr/issues/4
    pass


class LibSsmIntegrationTests(TestCase):

    @skip
    def test_get_secret(self):
        """
        python -m unittest tests.aws.test_libssm.LibSsmIntegrationTests.test_get_secret
        """

        key = "/iap/jwt-token"

        value = libssm.get_secret(key=key)

        self.assertIsNotNone(value)
        self.assertIsInstance(value, str)
        # print(value)
