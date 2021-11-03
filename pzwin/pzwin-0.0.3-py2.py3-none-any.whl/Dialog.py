from collections.abc import Callable

import pygame
from pygame.rect import Rect

from pzwin.Constants import *
from pzwin.WinBase import WinBase
from pzwin.WinFrame import WinFrame
from pzwin.Button import Button
class Dialog(WinFrame):
    DEFAULT_BTN_SIZE = (50, 20) # (width, height)
    DEFAULT_BTN_BUF = 10
    def __init__(self, parent:WinBase, rect:Rect):
        super().__init__(parent, rect)
        
        self._caption = 'pzwin dialog'
        
        self.__onCancel:Callable[[WinBase], bool]|None = None
        self.__onConfirm:Callable[[WinBase], bool]|None = None

        #对于Dialog的窗体，点了右上角的关闭，相当于取消
        self.onClose = self.onDialogClosed

        # Create confirm button
        self.__confirmBtn: Button = self.addButton(Rect(rect.width - 2 * self.DEFAULT_BTN_BUF - 2 *self.DEFAULT_BTN_SIZE[0],
                                                      rect.height - self.DEFAULT_BTN_BUF - self.DEFAULT_BTN_SIZE[1],
                                                      self.DEFAULT_BTN_SIZE[0], self.DEFAULT_BTN_SIZE[1]))
        self.__confirmBtn.setText('Confirm')\
            .setTextSize(10)\
            .setTextHorizontalCenter(True)\
            .setClickCallBack(self.onDialogConfirm)

        # Create cancel button
        self.__cancelBtn: Button = self.addButton(Rect(rect.width - self.DEFAULT_BTN_BUF - self.DEFAULT_BTN_SIZE[0],
                                                      rect.height - self.DEFAULT_BTN_BUF - self.DEFAULT_BTN_SIZE[1],
                                                      self.DEFAULT_BTN_SIZE[0], self.DEFAULT_BTN_SIZE[1]))
        self.__cancelBtn.setText('Cancel')\
            .setTextSize(10)\
            .setTextHorizontalCenter(True)\
            .setClickCallBack(self.onDialogClosed)
        
    #每个自定义回调函数的派生类都要实现该方法，并确保调用父类的该方法，以减少内存引用数量
    def clearCallBack(self):
        super().clearCallBack()
        self.__onCancel:Callable[[WinBase], bool]|None = None
        self.__onConfirm:Callable[[WinBase], bool]|None = None

    def drawForm(self):
        if self._isShow == False:
            return
        
        self._surface.fill(self._formBGColor)
        
        for childWin in self._zBuffer:
            if childWin == self:
                continue
            childWin.drawForm()        

        self.drawBorder()

        #所有都画完后，将surface贴到父窗体的surface上
        parentSurface = self.getParentSurface()
        parentSurface.blit(self._surface, self._pos)

    def onDialogClosed(self):
        self.hide()
        if self.__onCancel != None:
            self.__onCancel()
    def onDialogConfirm(self):
        self.hide()
        if self.__onConfirm != None:
            self.__onConfirm()

    def setCancelCallback(self, fn:Callable[[WinBase], bool]|None)->WinBase:
        self.__onCancel = fn
        return self
    def setConfirmCallback(self, fn:Callable[[WinBase], bool]|None)->WinBase:
        self.__onConfirm = fn
        return self