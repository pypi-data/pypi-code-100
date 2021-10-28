#!/usr/bin/env python3
import json

from pydm import Display
from qtpy.QtCore import QUrl
from qtpy.QtGui import QDesktopServices

from siriushlacon.mks937b.consts import DEVICE_MENU_UI, INFO_UI, PRESSURE, SETTINGS
from siriushlacon.tools.consts import VIEWER_URL
from siriushlacon.widgets.images import CNPEM_PIXMAP, LNLS_PIXMAP


def get_json_macro(macros):
    return json.dumps(macros)


class DeviceMenu(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(DeviceMenu, self).__init__(parent=parent, args=args, macros=macros)
        json_macro = get_json_macro(macros)

        self.btnMON.filenames = [PRESSURE]
        self.btnMON.macros = json_macro

        self.btnSettings.filenames = [SETTINGS]
        self.btnSettings.macros = json_macro

        self.btnInfo.filenames = [INFO_UI]
        self.btnInfo.macros = json_macro

        self.label_cnpem.setPixmap(CNPEM_PIXMAP)
        self.label_lnls.setPixmap(LNLS_PIXMAP)

    def open_archiver(self):
        QDesktopServices.openUrl(QUrl(VIEWER_URL))

    def ui_filename(self):
        return DEVICE_MENU_UI

    def ui_filepath(self):
        return DEVICE_MENU_UI
