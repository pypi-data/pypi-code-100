import unittest

from path_analysis_toolbox import PathAnalyser


class TestPathAnalyser(unittest.TestCase):
    def test_directory_filename_extension(self):
        self.assertEqual(PathAnalyser.directory_filename_extension(
            "C:\\QuickTranslator Data\\temp\\qt_temp_mp3_file.mp3"),
            ("C:\\QuickTranslator Data\\temp", "qt_temp_mp3_file", "mp3"))
        self.assertEqual(PathAnalyser.directory_filename_extension("C:\\temp\\foldername"),
                         ("C:\\temp", "foldername", ""))
        self.assertEqual(PathAnalyser.directory_filename_extension("C:"),
                         ("", "C:", ""))

    def test_get_subsequent_directories(self):
        self.assertEqual(PathAnalyser.get_subsequent_directories("C:\\QuickTranslator Data\\temp\\qt_temp_mp3_file.mp3"),
                         ['C:', 'C:\\QuickTranslator Data', 'C:\\QuickTranslator Data\\temp'])
        self.assertEqual(PathAnalyser.get_subsequent_directories("C:\\QuickTranslator Data\\temp"),
                         ['C:', 'C:\\QuickTranslator Data', 'C:\\QuickTranslator Data\\temp'])

    def test_create_directory(self):
        PathAnalyser.create_directories('Test\\Another\\And\\Another')
