import unittest
from sknrf.view.desktop.device.propertybrowser.tests import test_propertybrowser_scalar
from sknrf.view.desktop.device.propertybrowser.tests import test_propertybrowser_array
from sknrf.view.desktop.device.propertybrowser.tests import test_propertybrowser_container
from sknrf.view.desktop.device.propertybrowser.tests import test_propertybrowser_pyobject


def desktop_view_test_suite():
    test_suite = unittest.TestSuite()
    for count in range(10):
        test_suite.addTest(unittest.makeSuite(test_propertybrowser_scalar.TestPropertyManagerScalar))
        test_suite.addTest(unittest.makeSuite(test_propertybrowser_scalar.TestPropertyEditorScalar))
        test_suite.addTest(unittest.makeSuite(test_propertybrowser_scalar.TestPropertyManagerMultiScalar))

        test_suite.addTest(unittest.makeSuite(test_propertybrowser_array.TestPropertyManagerArray))
        test_suite.addTest(unittest.makeSuite(test_propertybrowser_array.TestPropertyEditorArray))
        test_suite.addTest(unittest.makeSuite(test_propertybrowser_array.TestPropertyManagerMultiArray))
        test_suite.addTest(unittest.makeSuite(test_propertybrowser_array.TestPropertyManagerMultiArray))

        test_suite.addTest(unittest.makeSuite(test_propertybrowser_container.TestPropertyManagerContainer))
        test_suite.addTest(unittest.makeSuite(test_propertybrowser_container.TestPropertyManagerContainerMixins))
        test_suite.addTest(unittest.makeSuite(test_propertybrowser_container.TestPropertyEditorContainer))
        test_suite.addTest(unittest.makeSuite(test_propertybrowser_container.TestPropertyManagerMultiContainer))

        test_suite.addTest(unittest.makeSuite(test_propertybrowser_pyobject.TestPropertyManagerPyObject))
        test_suite.addTest(unittest.makeSuite(test_propertybrowser_pyobject.TestPropertyEditorPyObject))
        test_suite.addTest(unittest.makeSuite(test_propertybrowser_pyobject.TestPropertyManagerMultiPyObject))
    return test_suite


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)
    runner = unittest.TextTestRunner()
    runner.run(desktop_view_test_suite())
    sys.exit(0)
