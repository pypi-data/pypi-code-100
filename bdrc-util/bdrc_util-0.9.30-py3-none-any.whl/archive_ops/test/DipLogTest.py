import datetime
import unittest
from pathlib import Path

import sys

import DBAppParser
from DBApps.DbApp import DbApp

from archive_ops.DipLog import DipLog, DipLogParser


class MyTestCase(unittest.TestCase):
    def test_DipLogInQA(self):
        expect_activity_type = 'GOOGLE_BOOKS'
        expect_begin_time = '2000-01-01 12:34:56'
        expect_work_name = 'W123456'
        sys.argv = ["DipLogParserTest.py", '--activity_type', expect_activity_type, '--work_name', expect_work_name,
                    "--begin_time", expect_begin_time]
        dlp = DipLogParser("usage", "desc")

        dla: DBAppParser.DbArgNamespace = dlp.parsedArgs
        dl: DipLog = DipLog(dla.drsDbConfig)

        dip_uid: str = dl.set_dip(dla.activity_type, dla.begin_time, dla.end_time, dla.dip_source_path,
                                  dla.dip_dest_path,
                                  dla.work_name, dla.dip_id, dla.activity_return_code, dla.comment)

        self.assertIsNotNone(dip_uid)


if __name__ == '__main__':
    unittest.main()
