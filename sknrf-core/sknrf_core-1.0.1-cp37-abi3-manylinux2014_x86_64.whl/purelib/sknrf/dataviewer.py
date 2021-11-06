import os
import sys
import logging

from PySide2.QtWidgets import QApplication

from sknrf.settings import Settings
from sknrf.view.desktop.base import desktop_logger, unhandled_exception, cleanup

# Initialize Settings/Logging
Settings(os.sep.join((os.environ["SKNRF_DIR"], "sknrf.yml")))
logger = desktop_logger(logging.getLogger(__name__))

if __name__ == "__main__":
    from sknrf.app.dataviewer.view.dataviewer import DataViewer

    app = QApplication(sys.argv)
    sys.excepthook = unhandled_exception
    form = DataViewer()
    form.showMaximized()
    try:
        app.exec_()
    except SystemExit:
        cleanup(form)
    sys.exit()
