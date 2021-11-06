"""
    ===========================
    sknrf Core (:mod:`sknrf`)
    ===========================

    sknrf Core is an object-oriented, modular nonlinear circuit/system measurement framework. Modular instrument software
    drivers can be loaded into the following measurement system schematic.

    ..  figure:: ../_images/PNG/setup_type_ltf.png
            :width: 50 %
            :align: center

            A 2-Port Test-bench circuit representation.

    Example
    -------
    To launch sknrf Core from the command line:

        $ python sknrf.py

    See Also
    ----------
    sknrf.view.desktop.main
"""
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
    from sknrf.view.desktop.main import MainMenuView

    app = QApplication(sys.argv)
    sys.excepthook = unhandled_exception
    form = MainMenuView()
    form.showMaximized()
    try:
        app.exec_()
    except SystemExit:
        cleanup(form)
    sys.exit()

