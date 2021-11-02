import unittest
from unittest.mock import MagicMock

from archive_ops.SaveWorkFacts import SaveWorkFacts


class TestSaveWorkFacts(unittest.TestCase):
    """
    Test that save_work_facts calls the db argument
    """

    def test_save(self) -> None:
        """
        Tests that the SaveWorkFacts method save_work_facts calls the
        CallAnySproc argument with the "UpdateWorkFacts" argument
        :return:
        """

        tdb = SaveWorkFacts("qa:~/.config/bdrc/db_apps.config")
        tdb.CallAnySproc = MagicMock()

        tdb.save_work_facts("FakeWorkName", (11, 12, 13, 14))
        tdb.CallAnySproc.assert_called_once_with("UpdateWorkFacts", "FakeWorkName", 11, 12, 13, 14)

    @unittest.skip("Do not perturb live data unless manually debugging")
    def test_save_live(self) -> None:
        """
        Tests that the SaveWorkFacts method save_work_facts calls the
        CallAnySproc argument with the "UpdateWorkFacts" argument
        :return:
        """

        tdb = SaveWorkFacts("qa:~/.config/bdrc/db_apps.config")

        tdb.save_work_facts("FakeWorkName", (11, 12, 13, 14))

        rl = tdb.ExecQuery("Select * from Works where WorkName = 'FakeWorkName' ")
        self.assertIsNotNone(rl)
        self.assertEqual(len(rl), 1)
        self.assertEqual(len(rl[0]), 1)
        ret_row = rl[0][0]
        self.assertEqual(ret_row['WorkName'],"FakeWorkName")
        self.assertEqual(ret_row['WorkSize'], 24)
        self.assertEqual(ret_row['WorkFileCount'], 26)
        self.assertEqual(ret_row['WorkImageFileCount'], 14)
        self.assertEqual(ret_row['WorkImageTotalFileSize'], 13)
        # 'WorkNonImageFileCount': 12)
        # 'WorkNonImageTotalFileSize': 11)
        # Expected return row (workId will vary)
        # {'workId': 51933,
        # 'WorkName': 'FakeWorkName',
        # 'HOLLIS': None,
        # 'create_time': datetime.datetime(2021, 11, 1, 12, 46, 20),
        # 'update_time': datetime.datetime(2021, 11, 1, 12, 46, 20),
        # 'WorkSize': 24,
        # 'WorkFileCount': 26,
        # 'WorkImageFileCount': 14,
        # 'WorkImageTotalFileSize': 13,
        # 'WorkNonImageFileCount': 12,
        # 'WorkNonImageTotalFileSize': 11}



