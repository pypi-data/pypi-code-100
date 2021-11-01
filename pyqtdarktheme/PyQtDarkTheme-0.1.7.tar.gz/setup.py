# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qdarktheme',
 'qdarktheme.dist',
 'qdarktheme.dist.dark',
 'qdarktheme.dist.light',
 'qdarktheme.qtpy',
 'qdarktheme.qtpy.QtCore',
 'qdarktheme.qtpy.QtGui',
 'qdarktheme.qtpy.QtSvg',
 'qdarktheme.qtpy.QtWidgets',
 'qdarktheme.widget_gallery',
 'qdarktheme.widget_gallery.ui']

package_data = \
{'': ['*'],
 'qdarktheme.dist.dark': ['svg/*'],
 'qdarktheme.dist.light': ['svg/*'],
 'qdarktheme.widget_gallery.ui': ['svg/*']}

setup_kwargs = {
    'name': 'pyqtdarktheme',
    'version': '0.1.7',
    'description': 'Flat dark theme for PySide, PyQt.',
    'long_description': 'PyQtDarkTheme\n=============\n\n## Project status\n[![PyPI Latest Release](https://img.shields.io/pypi/v/pyqtdarktheme.svg?color=orange)](https://pypi.org/project/pyqtdarktheme/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/pyqtdarktheme.svg?color=blue)](https://www.python.org/downloads/)\n[![Qt Versions](https://img.shields.io/badge/Qt-5%20|%206-blue.svg?&logo=Qt&logoWidth=18&logoColor=white)](https://www.qt.io/qt-for-python)\n[![License](https://img.shields.io/github/license/5yutan5/PyQtDarkTheme.svg?color=green)](https://github.com/5yutan5/PyQtDarkTheme/blob/main/LICENSE.txt/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/python/black)\n\n## Tests\n[![tests](https://github.com/5yutan5/PyQtDarkTheme/actions/workflows/test.yml/badge.svg)](https://github.com/5yutan5/PyQtDarkTheme/actions/workflows/test.yml)\n[![codeql](https://github.com/5yutan5/PyQtDarkTheme/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/5yutan5/PyQtDarkTheme/actions/workflows/codeql-analysis.yml)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/5yutan5/PyQtDarkTheme.svg?logo=lgtm&logoWidth=18&color=success)](https://lgtm.com/projects/g/5yutan5/PyQtDarkTheme/alerts/)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/5yutan5/PyQtDarkTheme.svg?logo=lgtm&logoWidth=18&color=success)](https://lgtm.com/projects/g/5yutan5/PyQtDarkTheme/context:python)\n[![CodeFactor](https://www.codefactor.io/repository/github/5yutan5/pyqtdarktheme/badge)](https://www.codefactor.io/repository/github/5yutan5/pyqtdarktheme)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/5yutan5/PyQtDarkTheme/main.svg)](https://results.pre-commit.ci/latest/github/5yutan5/PyQtDarkTheme/main)\n[![codecov](https://codecov.io/gh/5yutan5/PyQtDarkTheme/branch/main/graph/badge.svg?token=RTS8O0V6SF)](https://codecov.io/gh/5yutan5/PyQtDarkTheme)\n\nDark and Light theme for PySide and PyQt.\n\nPyQtDarkTheme applies a flat dark theme to PySide and PyQt. There\'s a light theme too. Color and style balanced from a dark theme for easy viewing in daylight.\n\n#### Features:\n\n- A modern Dark and Light theme\n- Support PySide and PyQt(Qt5, Qt6)\n- Support some freezing library(PyInstaller, cx_freeze, py2app and etc...)\n- Resolve the differences of style between Qt versions.\n- QPalette of dark and light theme\n\n\n### Dark Theme\n![widget_gallery_dark_theme](https://raw.githubusercontent.com/5yutan5/PyQtDarkTheme/main/images/widget_gallery_dark.png)\n\n### Light Theme\n![widget_gallery_light_them](https://raw.githubusercontent.com/5yutan5/PyQtDarkTheme/main/images/widget_gallery_light.png)\n\n## Requirements\n\n- [Python 3.7+](https://www.python.org/downloads/)\n- PySide6, PyQt6, PyQt5 or PySide2\n\n## Installation Method\n\n- Last released version\n   ```plaintext\n   pip install pyqtdarktheme\n   ```\n- Latest development version\n   ```plaintext\n   pip install git+https://github.com/5yutan5/PyQtDarkTheme\n   ```\n\n## Usage\n\n```Python\nimport sys\n\nfrom PySide6.QtWidgets import QApplication, QMainWindow, QPushButton\n\nimport qdarktheme\n\napp = QApplication(sys.argv)\nmain_win = QMainWindow()\npush_button = QPushButton("PyQtDarkTheme!!")\nmain_win.setCentralWidget(push_button)\n\n# Default is dark theme\napp.setStyleSheet(qdarktheme.load_stylesheet())\n# qdarktheme.load_stylesheet("dark")\n\nmain_win.show()\n\napp.exec()\n\n```\n\n> ⚠ The image quality may be lower on Qt5(PyQt5, PySide2) due to the use of svg. You can add the following attribute to improve the quality of images.\n> ```Python\n> app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)\n> ```\n\n### Light theme\n\n```Python\napp.setStyleSheet(qdarktheme.load_stylesheet("light"))\n```\n\n## QPalette of dark and light theme\n\nYou can get color of dark and light theme by loading QPalette.\nTo load palette, run:\n\n```Python\npalette = qdarktheme.load_palette()\n# qdarktheme.load_palette("dark")\n# qdarktheme.load_palette("light")\n```\n\nFor example, you can apply a link color to your application.\n\n```Python\nimport sys\n\nfrom PyQt6.QtGui import QPalette\nfrom PyQt6.QtWidgets import QApplication\n\nimport qdarktheme\n\napp = QApplication(sys.argv)\ndark_palette = qdarktheme.load_palette()\npalette = app.palette()\npalette.setColor(QPalette.ColorRole.Link, dark_palette.link().color())\napp.setPalette(palette)\n```\n\n## Example program\n\nTo check example program, run:\n\n```plaintext\npython -m qdarktheme.widget_gallery\n```\n\n## License\n\nThe svg file for the PyQtDarkTheme are derived [Material design icons](https://fonts.google.com/icons)(Apache License Version 2.0). Qt stylesheets are originally fork of [QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet)(MIT License). Other files are covered by PyQtDarkTheme\'s MIT license.\n',
    'author': 'Yunosuke Ohsugi',
    'author_email': '63651161+5yutan5@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/5yutan5/PyQtDarkTheme',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
