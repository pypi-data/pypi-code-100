__author__ = 'dtbespal'

import unittest
import cmath as ct

from sknrf.utilities.numeric import Info
from sknrf.utilities.numeric import num2str, num2str_re, num2str_re_im, num2str_lin_deg, num2str_log_deg
from sknrf.utilities.numeric import str2num, str2num_re, str2num_re_im, str2num_lin_deg, str2num_log_deg
from sknrf.utilities.rf import dBU2rU
from sknrf.widget.propertybrowser.view import PkAvg, Format


class TestNumericSimple(unittest.TestCase):
    def setUp(self):
        pass

    def test_num2str_re(self):
        info = Info("Test", format_=Format.RE)
        str_ = num2str_re(1.23, info)
        self.assertEqual(str_, "1.23")

    def test_num2str_re_im(self):
        info = Info("Test", format_=Format.RE_IM)
        str_ = num2str_re_im(1.23+1.23j, info)
        self.assertEqual(str_, "1.23 +1.23j")

    def test_num2str_lin_deg(self):
        info = Info("Test", format_=Format.LIN_DEG)
        str_ = num2str_lin_deg(1.23*ct.exp(1j*45.2*ct.pi/180), info)
        self.assertEqual(str_, "1.23 ∠ 45.2")

    def test_num2str_log_deg(self):
        info = Info("Test", format_=Format.LOG_DEG)
        str_ = num2str_log_deg(dBU2rU(1.23)*ct.exp(1j*45.2*ct.pi/180), info)
        self.assertEqual(str_, "1.23 ∠ 45.2")

    def test_num2str(self):
        info = Info("Test", format_=Format.RE_IM)
        str_ = num2str(1.23+1.23j, info)
        self.assertEqual(str_, "1.23 +1.23j")

    def test_str2num_re(self):
        info = Info("Test", format_=Format.RE)
        num = str2num_re("1.23", info)
        self.assertAlmostEqual(num, 1.23)

    def test_str2num_re_im_without_spaces(self):
        info = Info("Test", format_=Format.RE_IM)
        num = str2num_re_im("1.23+1.23j", info)
        self.assertAlmostEqual(num, 1.23+1.23j)

    def test_str2num_re_im_with_spaces(self):
        info = Info("Test", format_=Format.RE_IM)
        num = str2num_re_im("   1.23 + 1.23j ", info)
        self.assertAlmostEqual(num, 1.23+1.23j)

    def test_str2num_re_im_with_negative_values(self):
        info = Info("Test", format_=Format.RE_IM)
        num = str2num_re_im("-1.23-1.23j ", info)
        self.assertAlmostEqual(num, -1.23-1.23j)

    def test_str2num_re_im_real_only(self):
        info = Info("Test", format_=Format.RE_IM)
        num = str2num_re_im("1.23", info)
        self.assertAlmostEqual(num, 1.23)

    @unittest.expectedFailure
    def test_str2num_re_im_imag_only(self):
        info = Info("Test", format_=Format.RE_IM)
        num = str2num_re_im("1.23j", info)
        self.assertAlmostEqual(num, 1.23j)

    def test_str2num_re_im_missing_j_fail(self):
        info = Info("Test", format_=Format.RE_IM)
        num = str2num_re_im("1.23 +  1.23", info)
        self.assertAlmostEqual(num, 1.23+0j)

    def test_str2num_re_im_ignore_units(self):
        info = Info("Test", format_=Format.RE_IM)
        num = str2num_re_im("1.23+1.23j Units", info)
        self.assertAlmostEqual(num, 1.23+1.23j)

    def test_str2num_lin_deg_without_spaces(self):
        info = Info("Test", format_=Format.LIN_DEG)
        num = str2num_lin_deg("1.23<45.2", info)
        self.assertAlmostEqual(num, 1.23*ct.exp(1j*45.2*ct.pi/180))

    def test_str2num_lin_deg_with_spaces(self):
        info = Info("Test", format_=Format.LIN_DEG)
        num = str2num_lin_deg("   1.23 <     45.2 ", info)
        self.assertAlmostEqual(num, 1.23*ct.exp(1j*45.2*ct.pi/180))

    def test_str2num_lin_deg_without_negative_values(self):
        info = Info("Test", format_=Format.LIN_DEG)
        num = str2num_lin_deg("-1.23<-45.2", info)
        self.assertAlmostEqual(num, -1.23*ct.exp(1j*-45.2*ct.pi/180))

    def test_str2num_lin_deg_magnitude_only(self):
        info = Info("Test", format_=Format.LIN_DEG)
        num = str2num_lin_deg("1.23", info)
        self.assertAlmostEqual(num, 1.23)

    def test_str2num_lin_deg_phase_only_fail(self):
        info = Info("Test", format_=Format.LIN_DEG)
        num = str2num_lin_deg("1.23", info)
        self.assertAlmostEqual(num, 1.23)

    def test_str2num_lin_deg_negative_magnitude(self):
        info = Info("Test", format_=Format.LIN_DEG)
        num = str2num_lin_deg("-1.23<45.2", info)
        self.assertAlmostEqual(num, -1.23*ct.exp(1j*45.2*ct.pi/180))

    def test_str2num_lin_deg_ignore_units(self):
        info = Info("Test", format_=Format.LIN_DEG)
        num = str2num_lin_deg("1.23<45.2 Units", info)
        self.assertAlmostEqual(num, 1.23*ct.exp(1j*45.2*ct.pi/180))

    def test_str2num_log_deg_without_spaces(self):
        info = Info("Test", format_=Format.LOG_DEG)
        num = str2num_log_deg("1.23<45.2", info)
        self.assertAlmostEqual(num, dBU2rU(1.23)*ct.exp(1j*45.2*ct.pi/180))

    def test_str2num_log_deg_with_spaces(self):
        info = Info("Test", format_=Format.LOG_DEG)
        num = str2num_log_deg(" 1.23   <  45.2  ", info)
        self.assertAlmostEqual(num, dBU2rU(1.23)*ct.exp(1j*45.2*ct.pi/180))

    def test_str2num_log_deg_without_negative_values(self):
        info = Info("Test", format_=Format.LOG_DEG)
        num = str2num_log_deg("-1.23<-45.2", info)
        self.assertAlmostEqual(num, dBU2rU(-1.23)*ct.exp(1j*-45.2*ct.pi/180))

    def test_str2num_log_deg_magnitude_only(self):
        info = Info("Test", format_=Format.LOG_DEG)
        num = str2num_log_deg(" 1.23", info)
        self.assertAlmostEqual(num, dBU2rU(1.23))

    def test_str2num_log_deg_ignore_units(self):
        info = Info("Test", format_=Format.LOG_DEG)
        num = str2num_log_deg("1.23<45.2 Units", info)
        self.assertAlmostEqual(num, dBU2rU(1.23)*ct.exp(1j*45.2*ct.pi/180))

    def test_str2num(self):
        info = Info("Test", format_=Format.RE_IM)
        num = str2num("1.23+1.23j", info)
        self.assertEqual(num, 1.23 + 1.23j)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
