#############################################################################
##
## Copyright (C) 2021 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


import os

from PyQt6.QtCore import QFile, QIODevice, QMimeData, QPoint, Qt, QTextStream
from PyQt6.QtGui import QDrag, QPalette, QPixmap
from PyQt6.QtWidgets import QApplication, QFrame, QLabel, QWidget


class DragLabel(QLabel):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self.setAutoFillBackground(True)
        self.setFrameShape(QFrame.Shape.Panel)
        self.setFrameShadow(QFrame.Shadow.Raised)

    def mousePressEvent(self, event):
        hotSpot = event.position().toPoint()

        mimeData = QMimeData()
        mimeData.setText(self.text())
        mimeData.setData('application/x-hotspot',
                b'%d %d' % (hotSpot.x(), hotSpot.y()))

        pixmap = QPixmap(self.size())
        self.render(pixmap)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(hotSpot)

        dropAction = drag.exec(Qt.DropAction.CopyAction | Qt.DropAction.MoveAction, Qt.DropAction.CopyAction)

        if dropAction == Qt.DropAction.MoveAction:
            self.close()
            self.update()


class DragWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        dictionaryFile = QFile(
                os.path.join(os.path.dirname(__file__), 'words.txt'))
        dictionaryFile.open(QIODevice.OpenModeFlag.ReadOnly)

        x = 5
        y = 5

        for word in QTextStream(dictionaryFile).readAll().split():
            wordLabel = DragLabel(word, self)
            wordLabel.move(x, y)
            wordLabel.show()
            x += wordLabel.width() + 2
            if x >= 195:
                x = 5
                y += wordLabel.height() + 2

        newPalette = self.palette()
        newPalette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.white)
        self.setPalette(newPalette)

        self.setAcceptDrops(True)
        self.setMinimumSize(400, max(200, y))
        self.setWindowTitle("Draggable Text")

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            if event.source() in self.children():
                event.setDropAction(Qt.DropAction.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            mime = event.mimeData()
            pieces = mime.text().split()
            position = event.position().toPoint()
            hotSpot = QPoint()

            hotSpotPos = mime.data('application/x-hotspot').split(b' ')
            if len(hotSpotPos) == 2:
               hotSpot.setX(hotSpotPos[0].toInt()[0])
               hotSpot.setY(hotSpotPos[1].toInt()[0])

            for piece in pieces:
                newLabel = DragLabel(piece, self)
                newLabel.move(position - hotSpot)
                newLabel.show()

                position += QPoint(newLabel.width(), 0)

            if event.source() in self.children():
                event.setDropAction(Qt.DropAction.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = DragWidget()
    window.show()
    sys.exit(app.exec())
