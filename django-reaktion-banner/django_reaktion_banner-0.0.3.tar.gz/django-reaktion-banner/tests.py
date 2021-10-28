from django.test import TestCase
from model_bakery import baker
from banner.models import Banner


class BannerTest(TestCase):

    # Modals
    def test_banner_modal(self):
        """Tests banner model"""
        banner_test = baker.make(Banner)
        self.assertTrue(isinstance(banner_test, Banner))
        self.assertEqual(banner_test.__unicode__(), banner_test.title)

    # Clicks
    def test_save_impression(self):
        self.fail()

    def test_save_click(self):
        self.fail()
