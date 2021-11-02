import unittest
from archive_ops.GetReadyWorksForStates import *


class GetDIPReadyTest(unittest.TestCase):
    def test_GetConnected(self):
        sys.argv.append('-a')
        sys.argv.append('SINGLE_ARCHIVE_REMOVED')
        sys.argv.append('-d')
        sys.argv.append('qa:~/.config/bdrc/db_apps.config')
        args = GetReadyWorksParser("mumble test", "").parsedArgs
        wl = GetReadyWorks(args.drsDbConfig, args.activity_type).get_works()

        # To pass, you have to go into DRSQA  and
        # update DIP_Config set DIP_CONFIG_VALUE= '2' where idDIP_CONFIG = 'PRUNE_ACT_LIMIT';
        self.assertTrue(len(wl) < 3)


if __name__ == '__main__':
    unittest.main()
