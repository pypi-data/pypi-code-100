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
    from collections import OrderedDict

    from sknrf.model.base import AbstractModel
    from sknrf.model.sequencer.base import SequencerSideModel
    from sknrf.view.desktop.sequencer.menu import SequencerView

    from sknrf.model import sequencer as core

    app = QApplication(sys.argv)
    sys.excepthook = unhandled_exception
    AbstractModel.init()
    package_map = OrderedDict((("Core", [core]),))
    side_model = SequencerSideModel(package_map)
    form = SequencerView(AbstractModel.device_model(), AbstractModel.datagroup_model(), side_model)
    form.showMaximized()
    try:
        app.exec_()
    except SystemExit:
        cleanup(form)
    sys.exit()
