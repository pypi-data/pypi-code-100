import unittest
from pyfonybundles.loader import pyfony_bundles_loader
from pyfonybundles.loader.pyfony_bundles_loader_mocks import EntryPointMocked, Bundle1, Bundle2


class pyfony_bundles_loader_test(unittest.TestCase):  # noqa: N801
    def test_basic(self):
        def get_entry_points_mocked():
            return [
                EntryPointMocked(Bundle1),
                EntryPointMocked(Bundle2),
            ]

        pyfony_bundles_loader.get_entry_points = get_entry_points_mocked

        bundles = pyfony_bundles_loader.load_bundles()

        self.assertIsInstance(bundles[0], Bundle1)
        self.assertIsInstance(bundles[1], Bundle2)

    def test_duplicate_check(self):
        with self.assertRaises(Exception) as error:

            def get_entry_points_mocked():
                return [
                    EntryPointMocked(Bundle1),
                    EntryPointMocked(Bundle2),
                    EntryPointMocked(Bundle2),
                ]

            pyfony_bundles_loader.get_entry_points = get_entry_points_mocked

            pyfony_bundles_loader.load_bundles()

        self.assertEqual(
            "Multiple installations of bundle pyfonybundles.loader.pyfony_bundles_loader_mocks.Bundle2 found in your environment",
            str(error.exception),
        )


if __name__ == "__main__":
    unittest.main()
